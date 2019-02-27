from pyqtgraph import PlotWidget
from PyQt5.QtCore import Qt


class CustomPlotWidget(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseReleaseEvent(self, _event):
        # suppress right clicks
        if _event.button() == Qt.RightButton:
            _event.accept()
        else:
            super().mouseReleaseEvent(_event)


