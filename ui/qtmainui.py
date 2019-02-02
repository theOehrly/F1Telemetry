from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QResizeEvent

from ui.ui_mainwindow import Ui_MainWindow
from ui.videoplayerwidget import VideoPlayerWidget


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, selection_data, videofile):
        super().__init__()

        self.setupUi(self)
        self.videoplayer = VideoPlayerWidget(self.tab_video, selection_data, videofile)
        self.init_ui()

    def init_ui(self):
        self.tab_video.installEventFilter(self)
        self.show()

    def eventFilter(self, _object, _event):
        if _event.type() == QResizeEvent.Resize:
            self.videoplayer.resize(_event.size())
        return False
