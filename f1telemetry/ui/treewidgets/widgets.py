from PyQt5.QtCore import Qt

from ui.treewidgets import widgetsui


class BaseWidget(widgetsui.BaseWidgetUI):
    def __init__(self, treeelement):
        super().__init__()
        self.treeelement = treeelement
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


class SpikesByChangeWidget(widgetsui.SpikesByChangeWidgetUI):
    def __init__(self, treeelement):
        super().__init__()
        self.treeelement = treeelement

        self.ratePosBox.valueChanged.connect(self.valueChanged)
        self.rateNegBox.valueChanged.connect(self.valueChanged)

    def valueChanged(self):
        self.treeelement.processDataThreaded(self.ratePosBox.value(), self.rateNegBox.value())


class SmoothingSavgolWidget(widgetsui.SmoothingSavgolWidgetUI):
    def __init__(self, treeelement):
        super().__init__()
        self.treeelement = treeelement
        # self.setupUi(self)

        self.minNegRateBox.valueChanged.connect(self.valueChanged)
        self.splitCheckBox.stateChanged.connect(self.valueChanged)

    def valueChanged(self):
        if self.splitCheckBox.checkState() == Qt.Checked:
            segmented = True
            min_neg_change = self.minNegRateBox.value()
        else:
            segmented = False
            min_neg_change = 0
        self.treeelement.processDataThreaded(segmented, min_neg_change)
