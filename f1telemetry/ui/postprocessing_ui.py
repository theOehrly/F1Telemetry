from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QMenu, QSplitter, QScrollArea)
from PyQt5.Qt import QIcon, QSizePolicy, QFont, QColor
from PyQt5.QtCore import Qt
import pyqtgraph as qtgraph

from ui.customwidgets import F1ToolBarButton, F1PlotWidget, F1Tree, F1CheckBox
from ui.uibaseelements import create_toolbar_divider, create_toolbar_category, create_toolbar_spacer


FONT = QFont('Bahnschrift')


class PostProcessingUI(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)

        #######################
        # ##### TOOLBAR ###########################################################################################
        #######################
        toolbar = QWidget()
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        mainlayout.addWidget(toolbar)
        mainlayout.setSpacing(0)
        mainlayout.setContentsMargins(0, 0, 0, 0)

        toolbarlayout = QHBoxLayout(toolbar)
        toolbarlayout.setContentsMargins(0, 0, 0, 0)
        toolbarlayout.setSpacing(0)

        ########################
        # ########### create first category (file) and add it to the toolbar
        # category widget is created in seperate function (title, buttonvars, icons, texts)
        category_file, btns = create_toolbar_category('FILE',
                                                      ('open.png', 'save.png'),
                                                      ('Open', 'Save'))
        self.openBtn, self.saveBtn = btns
        toolbarlayout.addWidget(category_file)  # add category to toolbar

        # add a vertical line between categories; divider is create in seperate function
        toolbarlayout.addWidget(create_toolbar_divider())

        ##########################
        # ######### second category (spikes)
        category_spikes, btns = create_toolbar_category('SPIKES',
                                                        ('spikesrate.png', 'spikeslength.png', 'spikesmanual.png'),
                                                        ('Rate', 'Length', 'Manual'))
        self.spikesRateBtn, self.spikesLengthBtn, self.spikesManualBtn = btns
        toolbarlayout.addWidget(category_spikes)
        toolbarlayout.addWidget(create_toolbar_divider())

        ###############################
        # ############ third category (smoothing)
        self.smoothingSavgolBtn = None
        category_smoothing, btns = create_toolbar_category('SMOOTHING', ('smoothingsavgol.png',), ('Savgol',),
                                                           buttonsize=('double',))
        self.smoothingSavgolBtn, = btns
        toolbarlayout.addWidget(category_smoothing)
        toolbarlayout.addWidget(create_toolbar_divider())

        ################################
        # ############ fourth category (datapoints)
        self.datapointsRemovePeriodicBtn = None
        category_datapoints, btns = create_toolbar_category('DATAPOINTS', ('datapointsremoveperiodic.png',),
                                                            ('Remove Periodic',), buttonsize=('double',))
        self.datapointsRemovePeriodicBtn, = btns
        toolbarlayout.addWidget(category_datapoints)
        toolbarlayout.addWidget(create_toolbar_divider())

        # ##############################
        # ############## add expanding spacer with background
        toolbarspacer = create_toolbar_spacer()
        toolbarlayout.addWidget(toolbarspacer)

        #############################
        # ############ last toolbar button; switch environment
        self.category_env, btns = create_toolbar_category('ENVIRONMENT', ('envpostprocessing.png',),
                                                          ('Postprocessing',), buttonsize=('double+menu',))
        self.changeEnvBtn, = btns
        self.changeEnvBtn.setPopupMode(F1ToolBarButton.InstantPopup)
        changeenvmenu = QMenu()
        changeenvmenu.setFont(FONT)
        changeenvmenu.setStyleSheet('''QMenu { 
                                            background-color: #e8e8e9;
                                            color: #373a3e;
                                            padding: 0px;
                                            margin: 0px;
                                            }        
                                        QMenu::item {
                                            padding: 0px 5px 0px 60px;
                                            background-color: #e8e8e9;
                                            height: 40px;
                                            margin: 0px;
                                            border: None;
                                            }
                                        QMenu::icon''')
        menubtnvideorec = changeenvmenu.addAction(QIcon('./ui/images/envvideorecognition.png'), 'Videorecognition')
        menubtnvideorec.triggered.connect(lambda: self.window().switch_environment(1))  # switch to index 1 / video

        self.changeEnvBtn.setMenu(changeenvmenu)
        toolbarlayout.addWidget(create_toolbar_divider())
        toolbarlayout.addWidget(self.category_env)

        ##############################################
        # ########### Content ########################
        ##############################################

        content = QSplitter()
        content.setChildrenCollapsible(False)
        content.setStyleSheet('''QSplitter {
                                        background-color: #e8e8e9;
                                        padding: 10px;
                                        }
                                    QSplitter::handle {
                                        background-color: #9ea0a2;
                                        border-radius: 2px;
                                        }
                                    QSplitter::handle:vertical {
                                        height: 4px;
                                        }''')
        mainlayout.addWidget(content)

        ###############################
        # Tree Column
        treecolumn = QWidget()
        treecolumn.setMinimumWidth(200)
        treecolumn.setMinimumHeight(400)
        content.addWidget(treecolumn)

        treecolumnlayout = QVBoxLayout(treecolumn)
        treecolumnlayout.setSpacing(0)
        treecolumnlayout.setContentsMargins(10, 15, 0, 0)

        treecolumnheader = QLabel()
        treecolumnheader.setText('Tree')
        treecolumnheader.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        treecolumnheader.setFont(FONT)
        treecolumnheader.setStyleSheet('''QLabel {
                                                font: bold 20pt;
                                                color: #1a1c1f;
                                                padding: 0px 0px 0px 15px;
                                                }''')

        treecolumnlayout.addWidget(treecolumnheader)

        tcdividerline = QFrame()  # horizontal line below header
        tcdividerline.setFixedHeight(2)
        tcdividerline.setLineWidth(2)
        tcdividerline.setFrameShape(QFrame.HLine)
        tcdividerline.setStyleSheet('''QFrame[frameShape="4"] {color: #9ea0a2;
                                                                margin: 25px;}''')  # frame shape 4 is HLine

        treecolumnlayout.addWidget(tcdividerline)
        treecolumnlayout.setContentsMargins(0, 0, 10, 10)

        treecontainer = QScrollArea()
        treecontainer.setStyleSheet('''QScrollArea {background: transparent;
                                        border: None;
                                        padding: 0px;
                                        margin: 0px;
                                        }''')
        treecontainer.setWidgetResizable(True)
        treecontainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        treecolumnlayout.addWidget(treecontainer)
        treecolumnlayout.setStretchFactor(treecontainer, 1)

        self.tree = F1Tree()
        treecontainer.setWidget(self.tree)

        ############################################
        # ############## Plotting Area
        plotarea = QWidget()
        plotarea.setMinimumWidth(900)
        content.addWidget(plotarea)

        plotarealayout = QVBoxLayout(plotarea)
        plotarealayout.setContentsMargins(25, 25, 25, 25)
        plotarealayout.setSpacing(25)

        qtgraph.setConfigOption('background', QColor('#5a5d60'))
        qtgraph.setConfigOption('foreground', QColor('#000000'))

        self.mainPlot = F1PlotWidget()
        plotarealayout.addWidget(self.mainPlot)
        plotarealayout.setStretchFactor(self.mainPlot, 5)
        self.auxPlot = F1PlotWidget()
        plotarealayout.addWidget(self.auxPlot)
        plotarealayout.setStretchFactor(self.auxPlot, 1)

        ##############################################
        # ########### Bottom Info Bar ################
        ##############################################

        bottombar = QWidget()
        bottombar.setFixedHeight(30)
        bottombar.setStyleSheet("""QWidget {background-color: #9ea0a2;
                                            border-top: 1px solid #373a3e;}""")

        mainlayout.addWidget(bottombar)

        bottombarlayout = QHBoxLayout(bottombar)
        # bottombarlayout.setDirection(QHBoxLayout.RightToLeft)
        bottombarlayout.setContentsMargins(0, 0, 20, 0)

        self.showOriginalBox = F1CheckBox()
        self.showOriginalBox.setText("Show Original")
        bottombarlayout.addWidget(self.showOriginalBox, Qt.AlignCenter, Qt.AlignRight)

