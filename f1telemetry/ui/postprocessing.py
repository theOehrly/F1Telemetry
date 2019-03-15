from PyQt5.QtWidgets import QFileDialog

from ui.postprocessing_ui import PostProcessingUI
from ui.treewidgets.widgets import BaseWidget, SmoothingSavgolWidget, SpikesByChangeWidget

from datastruct import InteractiveDataSet
import postprocessing2
from csvparser import read_csv_file, write_csv_file

import pyqtgraph as qtgraph


class PostProcessing(PostProcessingUI):
    def __init__(self):
        super().__init__()

        self.dataset = None  # interactive dataset used for plotting/data processing

        self.auxPlotItems = list()  # references to the current plots (Plot.plot, not the PlotWidget itself)
        self.mainPlotItems = list()

        self.auxPlotViewRegion = qtgraph.LinearRegionItem()  # colored region on the auxPlot
        self.auxPlot.addItem(self.auxPlotViewRegion)
        self.auxPlot.setMouseEnabled(x=False, y=False)  # disable moving auxPlot completely
        self.mainPlot.setMouseEnabled(y=False)  # disable moving mainPlot along y-axis

        # interconnect mainPlot and the displayed region on the auxPlot so changing one updates the other
        self.auxPlotViewRegion.sigRegionChanged.connect(self.update_main_plot_region)
        self.mainPlot.sigXRangeChanged.connect(self.update_aux_plot_view_region)

        # connect functions to buttons
        self.openBtn.clicked.connect(self.open_file)
        self.saveBtn.clicked.connect(self.save_file)

        self.spikesRateBtn.clicked.connect(self.tool_spike_rate)
        self.smoothingSavgolBtn.clicked.connect(self.tool_smoothing)

        self.showOriginalBox.toggled.connect(self.toggle_show_original)
        self.show_original = False  # boolean value; defines whether original data is plotted addionally to newest

        # open sample file, for testing only
        # self.read_csv_file('../testruns/new_file_format.csv')

    def reload_all(self):
        """Redraws the plot AND UPDATES ALL OTHER UI ELEMENTS that can change."""

        self.tree.removeAll()  # clear the tree first

        # add all items of the selected tree to the tree widget
        for element in self.dataset.active.elements:
            self.tree.addItem(element.widget, element.name)

        self.redraw_plot()

    def redraw_plot(self):
        """(Only) Redraws the PLOT from the currently selected dataset tree."""

        # remove all old plot items first
        for item in self.mainPlotItems:
            self.mainPlot.removeItem(item)
        for item in self.auxPlotItems:
            self.auxPlot.removeItem(item)

        x, y = self.dataset.active.getNewest().getData()  # get the newest data from selected tree

        xmaximum = max(x)  # calculate x scaling factor

        # plot new data
        self.auxPlotItems.append(self.auxPlot.plot(x, y))
        self.auxPlot.setLimits(xMin=0, xMax=xmaximum, yMin=0, yMax=400)
        self.auxPlotViewRegion.setBounds((0, xmaximum))

        self.mainPlotItems.append(self.mainPlot.plot(x, y))
        self.mainPlot.enableAutoRange(enable=False)
        self.mainPlot.setLimits(xMin=0, xMax=xmaximum, yMin=0, yMax=400)

        if self.show_original:
            xo, yo = self.dataset.active.elements[0].getData()
            self.mainPlotItems.append(self.mainPlot.plot(xo, yo, yMin=0, yMax=400, pen=qtgraph.mkPen('#3c9af7')))

        self.update_main_plot_region()  # new plot is set to the previously selected region

    def update_aux_plot_view_region(self):
        """Updates linear region on aux plot, if main plot region changed."""
        self.auxPlotViewRegion.setRegion(self.mainPlot.getViewBox().viewRange()[0])

    def update_main_plot_region(self):
        """Updates diplay region of main plot, if linear region on aux plot changed."""
        self.mainPlot.setXRange(*self.auxPlotViewRegion.getRegion(), padding=0)

    def toggle_show_original(self, checked):
        self.show_original = checked
        self.redraw_plot()

    #####################################
    # Button functions
    ######

    def open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV files (*.csv)")
        if filepath:
            headers, x, ysets = read_csv_file(filepath)
            self.dataset = InteractiveDataSet(self, x, ysets, headers[0], headers[1:], filepath, BaseWidget)
            self.dataset.activeTreeChanged.connect(self.reload_all)  # reload everytzhing if user changes the tree
            self.dataset.dataChanged.connect(self.redraw_plot)  # update the plot if data was modified
            self.reload_all()  # create plot off the active tree

    def save_file(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save as", "", "CSV files (*.csv)")
        if filepath:
            write_csv_file(self.dataset, filepath)

    def tool_spike_rate(self):
        element = self.dataset.active.newElementFromNewest('Spikes by Change')
        element.connectWidget(SpikesByChangeWidget)
        element.setProcessingFunction(postprocessing2.spikes_by_change)
        self.tree.addItem(element.widget, 'SPIKES: Rate')

    def tool_smoothing(self):
        element = self.dataset.active.newElementFromNewest('Smoothing')
        element.connectWidget(SmoothingSavgolWidget)
        element.setProcessingFunction(postprocessing2.smoothing)
        self.tree.addItem(element.widget, 'SMOOTHING: Savgol')
