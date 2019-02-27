from PyQt5.QtWidgets import QWidget

from f1telemetry.ui.treewidgets import spikesbychange, base, smoothing
from f1telemetry.postprocessing2 import SpikesByChange


class BaseWidget(QWidget, base.Ui_BaseWidget):
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


class SpikesByChangeWidget(QWidget, spikesbychange.Ui_SpikesByChange):
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

