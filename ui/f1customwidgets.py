from pyqtgraph import PlotWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from ui import ui_treebasewidget, ui_treespikesbychangewidget
from postprocessing2 import SpikesByChange


class CustomPlotWidget(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseReleaseEvent(self, _event):
        # suppress right clicks
        if _event.button() == Qt.RightButton:
            _event.accept()
        else:
            super().mouseReleaseEvent(_event)


class TreeBaseWidget(QWidget, ui_treebasewidget.Ui_TreeBaseWidget):
    def __init__(self, treeelement):
        super().__init__()
        self.treeelement = treeelement
        self.setupUi(self)
        self.treeelement.dataset.initFinished.connect(self.finishInit)
        self.datasetDropdown.currentTextChanged.connect(self.treeelement.dataset.setActiveTree)

    def finishInit(self):
        self.fileNameLabel.setText(self.treeelement.options['filename'])

        for tree in self.treeelement.dataset.getTrees():
            self.datasetDropdown.addItem(tree)

        self.treeelement.parent.treeChangeFinished.connect(self.updateContent)

    def updateContent(self):
        print(self.treeelement.dataset.getActiveTreeName(), self)
        self.datasetDropdown.setCurrentText(self.treeelement.dataset.getActiveTreeName())


class SpikesByChangeWidget(QWidget, ui_treespikesbychangewidget.Ui_Widget):
    def __init__(self, treeelement):
        super().__init__()
        self.treeelement = treeelement
        self.setupUi(self)

        self.ratePosBox.valueChanged.connect(self.valueChanged)
        self.rateNegBox.valueChanged.connect(self.valueChanged)

        self.worker = None

    def valueChanged(self):
        self.worker = SpikesByChange(self.treeelement, self.ratePosBox.value(), self.rateNegBox.value())
        self.worker.processingFinished.connect(self.finished)
        self.worker.start()

    def finished(self):
        self.treeelement.dataChanged.emit()

