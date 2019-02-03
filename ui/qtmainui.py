from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QResizeEvent

from ui.ui_mainwindow import Ui_MainWindow
from ui.videoplayerwidget import VideoPlayerWidget


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, selection_data, videofile):
        super().__init__()

        self.setupUi(self)

        # add videoplayer widget into prepared placeholder
        self.videoplayer = VideoPlayerWidget(self.playercontainer, selection_data, videofile)
        self.playercontainer.setMinimumSize(self.videoplayer.minimumSize())

        self.init_ui()

    def init_ui(self):
        # install eventfilter on playercontainer
        self.playercontainer.installEventFilter(self)
        self.show()

    def eventFilter(self, _object, _event):
        if _event.type() == QResizeEvent.Resize:
            # resize videoplayer widget
            self.videoplayer.resize(_event.size())
        return False
