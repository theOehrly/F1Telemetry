import sys

from PyQt5.Qt import QApplication, QWidget, QStackedLayout, QProxyStyle, QStyle

from ui.postprocessing import PostProcessing
from ui.videorecognition import VideoRecognition


class F1TProxyStyle(QProxyStyle):
    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):
        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return 60
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


class Window(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.windowlayout = QStackedLayout(self)
        self.windowlayout.setSpacing(0)
        self.windowlayout.setContentsMargins(0, 0, 0, 0)
        self.windowlayout.addWidget(PostProcessing())
        self.windowlayout.addWidget(VideoRecognition())

        self.windowlayout.setCurrentIndex(0)

    def switch_environment(self, new_index):
        self.windowlayout.setCurrentIndex(new_index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    f1tstyle = F1TProxyStyle('Windows')
    app.setStyle(f1tstyle)
    window = Window()
    window.setWindowTitle('F1Telemetry')
    window.show()
    app.exec()
