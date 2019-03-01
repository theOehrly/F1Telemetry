# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/treewidgets/smoothing.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Smoothing(object):
    def setupUi(self, Smoothing):
        Smoothing.setObjectName("Smoothing")
        Smoothing.resize(391, 129)
        self.verticalLayout = QtWidgets.QVBoxLayout(Smoothing)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Smoothing)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.splitCheckBox = QtWidgets.QCheckBox(Smoothing)
        self.splitCheckBox.setObjectName("splitCheckBox")
        self.verticalLayout.addWidget(self.splitCheckBox)
        self.horizontalWidget = QtWidgets.QWidget(Smoothing)
        self.horizontalWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.horizontalWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.minDecelBox = QtWidgets.QSpinBox(self.horizontalWidget)
        self.minDecelBox.setMinimum(-9999999)
        self.minDecelBox.setMaximum(0)
        self.minDecelBox.setProperty("value", -10)
        self.minDecelBox.setObjectName("minDecelBox")
        self.horizontalLayout.addWidget(self.minDecelBox)
        self.label_3 = QtWidgets.QLabel(self.horizontalWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)
        self.verticalLayout.addWidget(self.horizontalWidget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Smoothing)
        QtCore.QMetaObject.connectSlotsByName(Smoothing)

    def retranslateUi(self, Smoothing):
        _translate = QtCore.QCoreApplication.translate
        Smoothing.setWindowTitle(_translate("Smoothing", "Form"))
        self.label.setText(_translate("Smoothing", "Smoothing (Savitzky-Golay Filter)"))
        self.splitCheckBox.setText(_translate("Smoothing", "Split by Breaking Point"))
        self.label_2.setText(_translate("Smoothing", "Minimum negative change"))
        self.label_3.setText(_translate("Smoothing", " [km/h per second]"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Smoothing = QtWidgets.QWidget()
    ui = Ui_Smoothing()
    ui.setupUi(Smoothing)
    Smoothing.show()
    sys.exit(app.exec_())

