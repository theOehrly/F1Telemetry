from PyQt5.QtCore import Qt
from PyQt5.Qt import QInputEvent

from ui.treewidgets import widgetsui
import pyqtgraph as qtgraph


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


class SpikesManualWidget(widgetsui.SpikesManualWidgetUI):
    def __init__(self, treeelement):
        super().__init__()
        self.treeelement = treeelement

        self.tempPlotDataItem = None  # temporary plolt data item for previewing cut paths
        self.leftButtonPressed = False
        self.cpathx = list()  # x coordinates of current cut path
        self.cpathy = list()
        self.cutpaths = list()  # list of [ ([x1, x2, ...], [y1, y2, ...]), ([], []), ...]

        self.cutPathsList.itemClicked.connect(self.selected_item_changed)
        self.addBtn.clicked.connect(self.addCut)
        self.delBtn.clicked.connect(self.deleteCut)

    def addCut(self):
        # start mouse tracking and mouse event interception; both are disabled again one mouse button release
        self.window().postprocessing.mainPlot.setMouseInterceptor(self)
        self.window().postprocessing.mainPlot.setMouseTracking(True)
        self.window().application.setOverrideCursor(Qt.CrossCursor)

    def deleteCut(self):
        # delete the currently selected item (if any) and have the treeelement calcualted the plot again
        if self.cutPathsList.selectedItems():
            item = self.cutPathsList.selectedItems()[0]
            index = self.cutPathsList.row(item)
            self.cutpaths.pop(index)
            self.cutPathsList.takeItem(index)
            if self.tempPlotDataItem:
                self.window().postprocessing.mainPlot.removeItem(self.tempPlotDataItem)

        self.treeelement.processDataThreaded(self.cutpaths)

    def mapToData(self, pos):
        # map position value in pixels to position value on data axis
        return self.window().postprocessing.mainPlot.plotItem.vb.mapSceneToView(pos)

    def plotMouseEvent(self, _event):
        if _event.type() == QInputEvent.MouseMove and self.leftButtonPressed:
            # click and drag with left mouse button; record coordinates and draw path
            pos = self.mapToData(_event.pos())
            self.cpathx.append(pos.x())
            self.cpathy.append(pos.y())
            self.tempPlotDataItem.setData(self.cpathx, self.cpathy)  # update plot of cut path

        elif _event.type() == QInputEvent.MouseButtonPress:
            # mouse drag starts; create temp plot to preview cut path
            self.leftButtonPressed = True
            self.cpathx = list()
            self.cpathy = list()
            if self.tempPlotDataItem:
                self.window().postprocessing.mainPlot.removeItem(self.tempPlotDataItem)

            pos = self.mapToData(_event.pos())
            self.tempPlotDataItem = self.window().postprocessing.mainPlot.plot((pos.x(), ), (pos.y(), ),
                                                                               pen=qtgraph.mkPen('r'))
            self.cpathx.append(pos.x())
            self.cpathy.append(pos.y())

        elif _event.type() == QInputEvent.MouseButtonRelease:
            #  mouse button is released, end of mouse drag; save path to self.cutpaths; recalculate tree element
            self.leftButtonPressed = False
            self.window().postprocessing.mainPlot.removeMouseInterceptor()
            self.window().postprocessing.mainPlot.setMouseTracking(False)
            self.window().application.restoreOverrideCursor()
            self.cutpaths.append((self.cpathx, self.cpathy))
            rangestr = str(round(self.cpathx[0], 1)) + ' - ' + str(round(self.cpathx[-1], 1))  # string: "first - last"
            self.cutPathsList.addItem(rangestr)

            self.treeelement.processDataThreaded(self.cutpaths)

    def selected_item_changed(self):
        if self.tempPlotDataItem:  # clear cut preview if anything is shown
            self.window().postprocessing.mainPlot.removeItem(self.tempPlotDataItem)

        if not self.cutPathsList.selectedItems():
            return

        index = self.cutPathsList.row(self.cutPathsList.selectedItems()[0])  # only one can be selected
        print(index)

        # plot the corresponding cut path for the currently selected item
        try:
            self.tempPlotDataItem = self.window().postprocessing.mainPlot.plot(self.cutpaths[index][0],
                                                                               self.cutpaths[index][1],
                                                                               pen=qtgraph.mkPen('r'))
        except IndexError:
            return


class SmoothingSavgolWidget(widgetsui.SmoothingSavgolWidgetUI):
    def __init__(self, treeelement):
        super().__init__()
        self.treeelement = treeelement

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


class DatapointsRemovePeriodicWidget(widgetsui.DatapointsRemovePeriodicWidgetUI):
    def __init__(self, treeelement):
        super().__init__()

        self.treeelement = treeelement

        self.intervalBox.valueChanged.connect(self.valueChanged)
        self.offsetBox.valueChanged.connect(self.valueChanged)

    def valueChanged(self):
        self.treeelement.processDataThreaded(self.intervalBox.value(), self.offsetBox.value())
