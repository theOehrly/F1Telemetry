# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/treewidgets/spikesbychange.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(437, 600)
        Widget.setMinimumSize(QtCore.QSize(0, 600))
        Widget.setSizeIncrement(QtCore.QSize(0, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(Widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Widget)
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
        self.label_2 = QtWidgets.QLabel(Widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.ratePosBox = QtWidgets.QSpinBox(Widget)
        self.ratePosBox.setMaximum(9999)
        self.ratePosBox.setProperty("value", 100)
        self.ratePosBox.setObjectName("ratePosBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ratePosBox)
        self.label_3 = QtWidgets.QLabel(Widget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.rateNegBox = QtWidgets.QSpinBox(Widget)
        self.rateNegBox.setMinimum(-9999)
        self.rateNegBox.setMaximum(0)
        self.rateNegBox.setProperty("value", -50)
        self.rateNegBox.setObjectName("rateNegBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rateNegBox)
        self.horizontalLayout.addLayout(self.formLayout)
        self.label_4 = QtWidgets.QLabel(Widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Form"))
        self.label.setText(_translate("Widget", "Maximum rate of change "))
        self.label_2.setText(_translate("Widget", "Positive"))
        self.label_3.setText(_translate("Widget", "Negative"))
        self.label_4.setText(_translate("Widget", " [km/h per second]"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())

