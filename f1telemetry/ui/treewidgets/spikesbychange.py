# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/treewidgets/spikesbychange.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SpikesByChange(object):
    def setupUi(self, SpikesByChange):
        SpikesByChange.setObjectName("SpikesByChange")
        SpikesByChange.resize(316, 600)
        SpikesByChange.setMinimumSize(QtCore.QSize(0, 600))
        SpikesByChange.setSizeIncrement(QtCore.QSize(0, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(SpikesByChange)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(SpikesByChange)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(SpikesByChange)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.ratePosBox = QtWidgets.QSpinBox(SpikesByChange)
        self.ratePosBox.setMaximum(9999)
        self.ratePosBox.setProperty("value", 100)
        self.ratePosBox.setObjectName("ratePosBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ratePosBox)
        self.label_3 = QtWidgets.QLabel(SpikesByChange)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.rateNegBox = QtWidgets.QSpinBox(SpikesByChange)
        self.rateNegBox.setMinimum(-9999)
        self.rateNegBox.setMaximum(0)
        self.rateNegBox.setProperty("value", -50)
        self.rateNegBox.setObjectName("rateNegBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rateNegBox)
        self.horizontalLayout.addLayout(self.formLayout)
        self.label_4 = QtWidgets.QLabel(SpikesByChange)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(SpikesByChange)
        QtCore.QMetaObject.connectSlotsByName(SpikesByChange)

    def retranslateUi(self, SpikesByChange):
        _translate = QtCore.QCoreApplication.translate
        SpikesByChange.setWindowTitle(_translate("SpikesByChange", "Form"))
        self.label.setText(_translate("SpikesByChange", "Maximum rate of change "))
        self.label_2.setText(_translate("SpikesByChange", "Positive"))
        self.label_3.setText(_translate("SpikesByChange", "Negative"))
        self.label_4.setText(_translate("SpikesByChange", " [km/h per second]"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SpikesByChange = QtWidgets.QWidget()
    ui = Ui_SpikesByChange()
    ui.setupUi(SpikesByChange)
    SpikesByChange.show()
    sys.exit(app.exec_())

