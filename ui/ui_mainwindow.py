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
        MainWindow.resize(1145, 820)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        self.container = QtWidgets.QWidget(self.tab_video)
        self.container.setObjectName("container")
        self.verticalLayout.addWidget(self.container)
        self.TabView.addTab(self.tab_video, "")
        self.tab_data = QtWidgets.QWidget()
        self.tab_data.setObjectName("tab_data")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_data)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.TabView.addTab(self.tab_data, "")
        self.verticalLayout_2.addWidget(self.TabView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1145, 25))
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
        self.TabView.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TabView.setTabText(self.TabView.indexOf(self.tab_video), _translate("MainWindow", "Video"))
        self.TabView.setTabText(self.TabView.indexOf(self.tab_data), _translate("MainWindow", "Data"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

