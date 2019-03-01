from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from f1telemetry.ui.treewidgets import spikesbychange, base, smoothing


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

    def valueChanged(self):
        self.treeelement.processDataThreaded(self.ratePosBox.value(), self.rateNegBox.value())


class SmoothingWidget(QWidget, smoothing.Ui_Smoothing):
    def __init__(self, treeelement):
        super().__init__()
        self.treeelement = treeelement
        self.setupUi(self)

        self.minDecelBox.valueChanged.connect(self.valueChanged)
        self.splitCheckBox.stateChanged.connect(self.valueChanged)

    def valueChanged(self):
        if self.splitCheckBox.checkState() == Qt.Checked:
            segmented = True
            min_neg_change = self.minDecelBox.value()
        else:
            segmented = False
            min_neg_change = 0
        self.treeelement.processDataThreaded(segmented, min_neg_change)
