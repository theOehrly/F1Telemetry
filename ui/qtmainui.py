import sys

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressDialog
from PyQt5.QtGui import QResizeEvent, QMouseEvent
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from ui.ui_mainwindow import Ui_MainWindow
from ui.videoplayerwidget import VideoPlayerWidget

from datastruct import SelectionData
import recognition


class OCRWorker(QThread):
    progressUpdate = pyqtSignal(int)
    finished = pyqtSignal(bool)
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
        self.finished.emit(True)

    def quit(self):
        self.STOP = True
        super().quit()


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.selection_data = SelectionData()

        self.error = None

        # add videoplayer widget into prepared placeholder
        self.videoplayer = VideoPlayerWidget(self.playercontainer, self.selection_data)
        self.playercontainer.setMinimumSize(self.videoplayer.minimumSize())

        self.ocr_progress_dialog = None
        self.ocr_worker = None

        self.init_ui()

    def init_ui(self):
        # install eventfilter on playercontainer
        self.playercontainer.installEventFilter(self)

        # file dialogs and run button
        self.btn_openin_video.clicked.connect(self.open_infile_video)
        self.lineedit_infile.returnPressed.connect(self.open_infile_video_from_lineedit)

        self.btn_chooseout_video.clicked.connect(self.set_outfile_video)

        self.lineedit_uid.installEventFilter(self)

        self.btn_run_ocr.clicked.connect(self.run_ocr)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainui = MainUI()
    app.exec()
