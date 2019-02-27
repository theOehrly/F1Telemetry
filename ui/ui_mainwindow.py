# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1383, 901)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TabView = QtWidgets.QTabWidget(self.centralwidget)
        self.TabView.setTabPosition(QtWidgets.QTabWidget.North)
        self.TabView.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.TabView.setTabsClosable(False)
        self.TabView.setMovable(False)
        self.TabView.setTabBarAutoHide(False)
        self.TabView.setObjectName("TabView")
        self.tab_video = QtWidgets.QWidget()
        self.tab_video.setObjectName("tab_video")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_video)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inout_controls = QtWidgets.QHBoxLayout()
        self.inout_controls.setObjectName("inout_controls")
        self.lbl_infile = QtWidgets.QLabel(self.tab_video)
        self.lbl_infile.setObjectName("lbl_infile")
        self.inout_controls.addWidget(self.lbl_infile)
        self.lineedit_infile = QtWidgets.QLineEdit(self.tab_video)
        self.lineedit_infile.setObjectName("lineedit_infile")
        self.inout_controls.addWidget(self.lineedit_infile)
        self.btn_openin_video = QtWidgets.QPushButton(self.tab_video)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_openin_video.sizePolicy().hasHeightForWidth())
        self.btn_openin_video.setSizePolicy(sizePolicy)
        self.btn_openin_video.setMinimumSize(QtCore.QSize(30, 0))
        self.btn_openin_video.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btn_openin_video.setObjectName("btn_openin_video")
        self.inout_controls.addWidget(self.btn_openin_video)
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.inout_controls.addItem(spacerItem)
        self.lbl_output = QtWidgets.QLabel(self.tab_video)
        self.lbl_output.setObjectName("lbl_output")
        self.inout_controls.addWidget(self.lbl_output)
        self.lineedit_output = QtWidgets.QLineEdit(self.tab_video)
        self.lineedit_output.setObjectName("lineedit_output")
        self.inout_controls.addWidget(self.lineedit_output)
        self.btn_chooseout_video = QtWidgets.QPushButton(self.tab_video)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_chooseout_video.sizePolicy().hasHeightForWidth())
        self.btn_chooseout_video.setSizePolicy(sizePolicy)
        self.btn_chooseout_video.setMinimumSize(QtCore.QSize(30, 0))
        self.btn_chooseout_video.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btn_chooseout_video.setObjectName("btn_chooseout_video")
        self.inout_controls.addWidget(self.btn_chooseout_video)
        spacerItem1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.inout_controls.addItem(spacerItem1)
        self.label_uid = QtWidgets.QLabel(self.tab_video)
        self.label_uid.setObjectName("label_uid")
        self.inout_controls.addWidget(self.label_uid)
        self.lineedit_uid = QtWidgets.QLineEdit(self.tab_video)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_uid.sizePolicy().hasHeightForWidth())
        self.lineedit_uid.setSizePolicy(sizePolicy)
        self.lineedit_uid.setInputMask("")
        self.lineedit_uid.setText("")
        self.lineedit_uid.setMaxLength(32767)
        self.lineedit_uid.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineedit_uid.setObjectName("lineedit_uid")
        self.inout_controls.addWidget(self.lineedit_uid)
        spacerItem2 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.inout_controls.addItem(spacerItem2)
        self.btn_run_ocr = QtWidgets.QPushButton(self.tab_video)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btn_run_ocr.setFont(font)
        self.btn_run_ocr.setFlat(False)
        self.btn_run_ocr.setObjectName("btn_run_ocr")
        self.inout_controls.addWidget(self.btn_run_ocr)
        self.verticalLayout.addLayout(self.inout_controls)
        self.playercontainer = QtWidgets.QWidget(self.tab_video)
        self.playercontainer.setMinimumSize(QtCore.QSize(0, 0))
        self.playercontainer.setObjectName("playercontainer")
        self.verticalLayout.addWidget(self.playercontainer)
        self.TabView.addTab(self.tab_video, "")
        self.dataTab = QtWidgets.QWidget()
        self.dataTab.setObjectName("dataTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dataTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.toolbar = QtWidgets.QHBoxLayout()
        self.toolbar.setObjectName("toolbar")
        self.toolSpikeRateButton = QtWidgets.QPushButton(self.dataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolSpikeRateButton.sizePolicy().hasHeightForWidth())
        self.toolSpikeRateButton.setSizePolicy(sizePolicy)
        self.toolSpikeRateButton.setMinimumSize(QtCore.QSize(50, 50))
        self.toolSpikeRateButton.setMaximumSize(QtCore.QSize(60, 60))
        self.toolSpikeRateButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.toolSpikeRateButton.setObjectName("toolSpikeRateButton")
        self.toolbar.addWidget(self.toolSpikeRateButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.toolbar.addItem(spacerItem3)
        self.pushButton = QtWidgets.QPushButton(self.dataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton.setMaximumSize(QtCore.QSize(60, 60))
        self.pushButton.setSizeIncrement(QtCore.QSize(0, 0))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.toolbar.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.toolbar)
        self.line_2 = QtWidgets.QFrame(self.dataTab)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.opwin = QtWidgets.QHBoxLayout()
        self.opwin.setObjectName("opwin")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.treeHeaderLabel = QtWidgets.QLabel(self.dataTab)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.treeHeaderLabel.setFont(font)
        self.treeHeaderLabel.setObjectName("treeHeaderLabel")
        self.verticalLayout_4.addWidget(self.treeHeaderLabel)
        self.line = QtWidgets.QFrame(self.dataTab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.treeToolBox = QtWidgets.QToolBox(self.dataTab)
        self.treeToolBox.setObjectName("treeToolBox")
        self.original = QtWidgets.QWidget()
        self.original.setGeometry(QtCore.QRect(0, 0, 264, 585))
        self.original.setObjectName("original")
        self.treeToolBox.addItem(self.original, "")
        self.op1 = QtWidgets.QWidget()
        self.op1.setGeometry(QtCore.QRect(0, 0, 264, 262))
        self.op1.setObjectName("op1")
        self.treeToolBox.addItem(self.op1, "")
        self.verticalLayout_4.addWidget(self.treeToolBox)
        self.opwin.addLayout(self.verticalLayout_4)
        self.plots = QtWidgets.QVBoxLayout()
        self.plots.setObjectName("plots")
        self.mainPlotWidget = CustomPlotWidget(self.dataTab)
        self.mainPlotWidget.setObjectName("mainPlotWidget")
        self.plots.addWidget(self.mainPlotWidget)
        self.auxPlotWidget = CustomPlotWidget(self.dataTab)
        self.auxPlotWidget.setObjectName("auxPlotWidget")
        self.plots.addWidget(self.auxPlotWidget)
        self.plots.setStretch(0, 10)
        self.plots.setStretch(1, 2)
        self.opwin.addLayout(self.plots)
        self.opwin.setStretch(0, 1)
        self.opwin.setStretch(1, 4)
        self.verticalLayout_3.addLayout(self.opwin)
        self.line_3 = QtWidgets.QFrame(self.dataTab)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.statusLabel = QtWidgets.QLabel(self.dataTab)
        self.statusLabel.setObjectName("statusLabel")
        self.horizontalLayout.addWidget(self.statusLabel)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.showOriginalCheckbox = QtWidgets.QCheckBox(self.dataTab)
        self.showOriginalCheckbox.setObjectName("showOriginalCheckbox")
        self.horizontalLayout.addWidget(self.showOriginalCheckbox)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.TabView.addTab(self.dataTab, "")
        self.verticalLayout_2.addWidget(self.TabView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1383, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.TabView.setCurrentIndex(1)
        self.treeToolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_infile.setText(_translate("MainWindow", "Input File"))
        self.btn_openin_video.setText(_translate("MainWindow", "..."))
        self.lbl_output.setText(_translate("MainWindow", "Output File"))
        self.btn_chooseout_video.setText(_translate("MainWindow", "..."))
        self.label_uid.setText(_translate("MainWindow", "UID"))
        self.btn_run_ocr.setText(_translate("MainWindow", "Run"))
        self.TabView.setTabText(self.TabView.indexOf(self.tab_video), _translate("MainWindow", "Video"))
        self.toolSpikeRateButton.setText(_translate("MainWindow", "De-Spike"))
        self.treeHeaderLabel.setText(_translate("MainWindow", "Tree"))
        self.treeToolBox.setItemText(self.treeToolBox.indexOf(self.original), _translate("MainWindow", "Input File"))
        self.treeToolBox.setItemText(self.treeToolBox.indexOf(self.op1), _translate("MainWindow", "New Operation"))
        self.statusLabel.setText(_translate("MainWindow", "Info"))
        self.showOriginalCheckbox.setText(_translate("MainWindow", "Show Original"))
        self.TabView.setTabText(self.TabView.indexOf(self.dataTab), _translate("MainWindow", "Data"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))

from f1customwidgets import CustomPlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

