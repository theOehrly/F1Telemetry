import csv

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressDialog
from PyQt5.QtGui import QResizeEvent, QMouseEvent
from PyQt5.QtCore import QThread, pyqtSignal

import pyqtgraph as qtg

from f1telemetry.ui.mainwindow import Ui_MainWindow
from f1telemetry.ui.videoplayerwidget import VideoPlayerWidget
from f1telemetry.ui.treewidgets.customwidgets import BaseWidget, SpikesByChangeWidget, SmoothingWidget

from f1telemetry.datastruct import SelectionData, InteractiveDataSet
from f1telemetry import recognition


class OCRWorker(QThread):
    progressUpdate = pyqtSignal(int)
    finished = pyqtSignal()
    STOP = False

    def __init__(self, fname, ofile, uid, selection):
        super().__init__()

        self.filename = fname
        self.outfile = ofile
        self.uid = uid
        self.selection = selection

    def run(self):
        recognition.recognize(self.filename, self.outfile, self.uid, self.selection, self)

    def update_progress(self, frame):
        self.progressUpdate.emit(frame)

    def set_finished(self):
        self.finished.emit()

    def quit(self):
        self.STOP = True
        super().quit()


class F1MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.selection_data = SelectionData()  # holds information about region of interest and start/end/zero time
        self.dataset = None  # interactive dataset used for plotting/data processing

        self.error = None

        # add videoplayer widget into prepared placeholder
        self.videoplayer = VideoPlayerWidget(self.playercontainer, self.selection_data)
        self.playercontainer.setMinimumSize(self.videoplayer.minimumSize())

        self.ocr_progress_dialog = None
        self.ocr_worker = None

        self.data_processing_worker = None

        self.auxPlotViewRegion = qtg.LinearRegionItem()
        self.auxPlotItem = None
        self.mainPlotItem = None

        self.init_ui()

        self.open_csv_file()

    def init_ui(self):
        # ## VIDEO PLAYER ## #
        # ####################

        # install eventfilter on playercontainer
        self.playercontainer.installEventFilter(self)

        # file dialogs and run button
        self.btn_openin_video.clicked.connect(self.open_infile_video)
        self.lineedit_infile.returnPressed.connect(self.open_infile_video_from_lineedit)

        self.btn_chooseout_video.clicked.connect(self.set_outfile_video)

        self.lineedit_uid.installEventFilter(self)

        self.btn_run_ocr.clicked.connect(self.run_ocr)

        # ## DATA PROCESSING ## #
        # #######################

        self.auxPlotWidget.addItem(self.auxPlotViewRegion)
        self.auxPlotWidget.setMouseEnabled(x=False, y=False)
        self.mainPlotWidget.setMouseEnabled(y=False)

        self.auxPlotViewRegion.sigRegionChanged.connect(self.update_main_plot)
        self.mainPlotWidget.sigXRangeChanged.connect(self.update_aux_plot_view_region)

        self.toolSpikeRateButton.clicked.connect(self.tool_spike_rate)
        self.toolSmoothingButton.clicked.connect(self.tool_smoothing)

        self.show()

    def eventFilter(self, _object, _event):
        if _event.type() == QResizeEvent.Resize and _object is self.playercontainer:
            # resize videoplayer widget
            self.videoplayer.resize(_event.size())
        elif _event.type() == QMouseEvent.MouseButtonRelease and _object is self.lineedit_uid:
            self.reset_ocr_uid_warning()
            return True
        return False

    def closeEvent(self, *args, **kwargs):
        self.videoplayer.videosource.release()
        super().closeEvent(*args, **kwargs)

    # ###### VIDEO PLAYER ######## #

    def open_infile_video_from_lineedit(self):
        self.videoplayer.open_file(self.lineedit_infile.text())
        self.reset_ocr_vid_warning()

    def open_infile_video(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Videofile", "", "Video files (*.*)")
        if filepath:
            self.lineedit_infile.setText(str(filepath))
            self.videoplayer.open_file(filepath)
            self.reset_ocr_vid_warning()

    def set_outfile_video(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Output as", "", "*.csv")
        if filepath:
            self.lineedit_output.setText(str(filepath))
            self.reset_ocr_outfile_error()

    def run_ocr(self):
            # check if we have all necessary info
            if not self.videoplayer.videosource.capture:
                self.btn_openin_video.setStyleSheet("QPushButton{background:red;}")
                self.error = "OCR_NOVID"
                return
            filename = self.lineedit_infile.text()

            outfile = self.lineedit_output.text()
            if not outfile:
                self.btn_chooseout_video.setStyleSheet("QPushButton{background:red;}")
                self.error = "OCR_NOOUT"
                return

            uid = self.lineedit_uid.text()
            if not uid:
                self.lineedit_uid.setText('Enter UID!')
                self.lineedit_uid.setStyleSheet("QLineEdit{background:red;}")
                self.error = 'OCR_NOUID'
                return

            # show progress bar
            n_frames = self.selection_data.end_frame - self.selection_data.start_frame
            self.ocr_progress_dialog = QProgressDialog('Processing Frames...', 'Cancel', 0, n_frames, self)
            self.ocr_progress_dialog.setMinimumWidth(400)
            self.ocr_progress_dialog.setWindowTitle('OCR Running')
            self.ocr_progress_dialog.canceled.connect(self.cancel_ocr)
            self.ocr_progress_dialog.show()

            # run ocr in seperate QThread
            self.ocr_worker = OCRWorker(filename, outfile, uid, self.selection_data)
            self.ocr_worker.progressUpdate.connect(self.update_ocr_progress)
            self.ocr_worker.finished.connect(self.update_ocr_finished)
            self.ocr_worker.start()

    def reset_ocr_uid_warning(self):
        if self.error == 'OCR_NOUID':
            self.lineedit_uid.setStyleSheet("")
            self.lineedit_uid.setText("")
            self.error = None

    def reset_ocr_vid_warning(self):
        if self.error == 'OCR_NOVID':
            self.btn_openin_video.setStyleSheet("")
            self.error = None

    def reset_ocr_outfile_error(self):
        if self.error == "OCR_NOOUT":
            self.btn_chooseout_video.setStyleSheet("")
            self.error = None

    def update_ocr_progress(self, frame):
        self.ocr_progress_dialog.setValue(frame)

    def update_ocr_finished(self):
        self.ocr_progress_dialog.reset()
        self.ocr_progress_dialog = None

    def cancel_ocr(self):
        self.ocr_worker.quit()
        self.ocr_worker.wait()

    # ###### DATA PROCESSING ######## #

    def open_csv_file(self):
        filename = '../testruns/new_file_format.csv'

        x = list()
        ysets = list()

        with open(filename, 'r') as csv_in:
            reader = csv.reader(csv_in, delimiter=';')
            headers = reader.__next__()  # first line are column names
            num_datasets = len(headers) - 1  # minus one because one column is the "x axis"

            for _ in range(num_datasets):  # add the required number of sublists to ysets (one per dataset)
                ysets.append(list())

            for row in reader:
                x.append(float(row[0]))  # copy the x value into it's list

                for i in range(num_datasets):
                    ysets[i].append(float(row[i+1]))  # copy each y value into it's respective list

            csv_in.close()

        self.dataset = InteractiveDataSet(self, x, ysets, headers[1:], filename, BaseWidget)
        self.dataset.activeTreeChanged.connect(self.reload_all)
        self.reload_all()

    def reload_all(self):
        # remove all items that are currently shown in the tree tool box
        for _ in range(self.treeToolBox.count()):
            self.treeToolBox.removeItem(0)

        # add al items of the newly selected tree
        for element in self.dataset.active.elements:
            self.treeToolBox.addItem(element.widget, element.name)

        self.redraw_plot()

    def redraw_plot(self):
        if self.mainPlotItem and self.auxPlotItem:
            self.mainPlotWidget.removeItem(self.mainPlotItem)
            self.auxPlotWidget.removeItem(self.auxPlotItem)

        x, y = self.dataset.active.getNewest().getData()

        ymaximum = max(y) * 1.1
        xmaximum = max(x)
        self.auxPlotItem = self.auxPlotWidget.plot(x, y)
        self.auxPlotWidget.setLimits(xMin=0, xMax=xmaximum, yMin=0, yMax=ymaximum)
        self.auxPlotViewRegion.setBounds((0, xmaximum))

        self.mainPlotItem = self.mainPlotWidget.plot(x, y)
        self.mainPlotWidget.setLimits(xMin=0, xMax=xmaximum, yMin=0, yMax=ymaximum)

        self.update_main_plot()

    def update_aux_plot_view_region(self):
        self.auxPlotViewRegion.setRegion(self.mainPlotWidget.getViewBox().viewRange()[0])

    def update_main_plot(self):
        self.mainPlotWidget.setXRange(*self.auxPlotViewRegion.getRegion(), padding=0)

    def tool_spike_rate(self):
        element = self.dataset.active.newElementFromNewest('Spikes by Change')
        element.connectWidget(SpikesByChangeWidget)
        element.dataChanged.connect(self.redraw_plot)

        self.treeToolBox.addItem(element.widget, 'Spikes by Change')
        self.treeToolBox.setCurrentWidget(element.widget)

    def tool_smoothing(self):
        element = self.dataset.active.newElementFromNewest('Smoothing')
        element.connectWidget(SmoothingWidget)
        element.dataChanged.connect(self.redraw_plot)

        self.treeToolBox.addItem(element.widget, 'Smoothing')
        self.treeToolBox.setCurrentWidget(element.widget)
