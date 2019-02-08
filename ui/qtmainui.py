import sys

from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QResizeEvent, QMouseEvent
from PyQt5.Qt import QApplication

from ui.ui_mainwindow import Ui_MainWindow
from ui.videoplayerwidget import VideoPlayerWidget

from datastruct import SelectionData


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.selection_data = SelectionData()

        self.error = None

        # add videoplayer widget into prepared placeholder
        self.videoplayer = VideoPlayerWidget(self.playercontainer, self.selection_data)
        self.playercontainer.setMinimumSize(self.videoplayer.minimumSize())

        self.init_ui()

    def init_ui(self):
        # install eventfilter on playercontainer
        self.playercontainer.installEventFilter(self)

        # file dialogs and run button
        self.btn_openin_video.clicked.connect(self.open_infile_video)
        self.lineedit_infile.returnPressed.connect(self.open_infile_video_from_lineedit)

        self.btn_chooseout_video.clicked.connect(self.set_outfile_video)

        self.lineedi_uid.installEventFilter(self)

        self.btn_run_ocr.clicked.connect(self.run_ocr)

        self.show()

    def eventFilter(self, _object, _event):
        if _event.type() == QResizeEvent.Resize and _object is self.playercontainer:
            # resize videoplayer widget
            self.videoplayer.resize(_event.size())
        elif _event.type() == QMouseEvent.MouseButtonRelease and _object is self.lineedi_uid:
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

            if not self.lineedit_output.text():
                self.btn_chooseout_video.setStyleSheet("QPushButton{background:red;}")
                self.error = "OCR_NOOUT"
                return

            elif not self.lineedi_uid.text():
                self.lineedi_uid.setText('Enter UID!')
                self.lineedi_uid.setStyleSheet("QLineEdit{background:red;}")
                self.error = 'OCR_NOUID'
                return

    def reset_ocr_uid_warning(self):
        if self.error == 'OCR_NOUID':
            self.lineedi_uid.setStyleSheet("")
            self.lineedi_uid.setText("")
            self.error = None

    def reset_ocr_vid_warning(self):
        if self.error == 'OCR_NOVID':
            self.btn_openin_video.setStyleSheet("")
            self.error = None

    def reset_ocr_outfile_error(self):
        if self.error == "OCR_NOOUT":
            self.btn_chooseout_video.setStyleSheet("")
            self.error = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainui = MainUI()
    app.exec()
