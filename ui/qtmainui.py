from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QResizeEvent

from ui.ui_mainwindow import Ui_MainWindow
from ui.videoplayerwidget import VideoPlayerWidget


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, selection_data):
        super().__init__()

        self.setupUi(self)

        # add videoplayer widget into prepared placeholder
        self.videoplayer = VideoPlayerWidget(self.playercontainer, selection_data)
        self.playercontainer.setMinimumSize(self.videoplayer.minimumSize())

        self.init_ui()

    def init_ui(self):
        # install eventfilter on playercontainer
        self.playercontainer.installEventFilter(self)

        # file dialogs and run button
        self.btn_openin_video.clicked.connect(self.open_infile_video)
        self.lineedit_infile.returnPressed.connect(self.open_infile_video_from_enter)
        self.show()

    def eventFilter(self, _object, _event):
        if _event.type() == QResizeEvent.Resize:
            # resize videoplayer widget
            self.videoplayer.resize(_event.size())
        return False

    def closeEvent(self, *args, **kwargs):
        self.videoplayer.videosource.release()
        super().closeEvent(*args, **kwargs)

    def open_infile_video_from_enter(self):
        self.videoplayer.open_file(self.lineedit_infile.text())

    def open_infile_video(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Videofile", "", "Video files (*.*)")
        if filepath:
            self.lineedit_infile.setText(str(filepath))
            self.videoplayer.open_file(filepath)
