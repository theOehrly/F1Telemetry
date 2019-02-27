# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/treewidgets/base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BaseWidget(object):
    def setupUi(self, BaseWidget):
        BaseWidget.setObjectName("BaseWidget")
        BaseWidget.resize(463, 80)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BaseWidget.sizePolicy().hasHeightForWidth())
        BaseWidget.setSizePolicy(sizePolicy)
        BaseWidget.setMinimumSize(QtCore.QSize(0, 0))
        BaseWidget.setMaximumSize(QtCore.QSize(16777215, 80))
        self.verticalLayout = QtWidgets.QVBoxLayout(BaseWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(BaseWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.fileNameLabel = QtWidgets.QLabel(BaseWidget)
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fileNameLabel)
        self.label_3 = QtWidgets.QLabel(BaseWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.datasetDropdown = QtWidgets.QComboBox(BaseWidget)
        self.datasetDropdown.setObjectName("datasetDropdown")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.datasetDropdown)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(BaseWidget)
        QtCore.QMetaObject.connectSlotsByName(BaseWidget)

    def retranslateUi(self, BaseWidget):
        _translate = QtCore.QCoreApplication.translate
        BaseWidget.setWindowTitle(_translate("BaseWidget", "Form"))
        self.label.setText(_translate("BaseWidget", "File"))
        self.fileNameLabel.setText(_translate("BaseWidget", "Some/File/Path"))
        self.label_3.setText(_translate("BaseWidget", "Dataset"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BaseWidget = QtWidgets.QWidget()
    ui = Ui_BaseWidget()
    ui.setupUi(BaseWidget)
    BaseWidget.show()
    sys.exit(app.exec_())

