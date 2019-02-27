# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'treebasewidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TreeBaseWidget(object):
    def setupUi(self, TreeBaseWidget):
        TreeBaseWidget.setObjectName("TreeBaseWidget")
        TreeBaseWidget.resize(463, 80)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TreeBaseWidget.sizePolicy().hasHeightForWidth())
        TreeBaseWidget.setSizePolicy(sizePolicy)
        TreeBaseWidget.setMinimumSize(QtCore.QSize(0, 0))
        TreeBaseWidget.setMaximumSize(QtCore.QSize(16777215, 80))
        self.verticalLayout = QtWidgets.QVBoxLayout(TreeBaseWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(TreeBaseWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.fileNameLabel = QtWidgets.QLabel(TreeBaseWidget)
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fileNameLabel)
        self.label_3 = QtWidgets.QLabel(TreeBaseWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.datasetDropdown = QtWidgets.QComboBox(TreeBaseWidget)
        self.datasetDropdown.setObjectName("datasetDropdown")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.datasetDropdown)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(TreeBaseWidget)
        QtCore.QMetaObject.connectSlotsByName(TreeBaseWidget)

    def retranslateUi(self, TreeBaseWidget):
        _translate = QtCore.QCoreApplication.translate
        TreeBaseWidget.setWindowTitle(_translate("TreeBaseWidget", "Form"))
        self.label.setText(_translate("TreeBaseWidget", "File"))
        self.fileNameLabel.setText(_translate("TreeBaseWidget", "Some/File/Path"))
        self.label_3.setText(_translate("TreeBaseWidget", "Dataset"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TreeBaseWidget = QtWidgets.QWidget()
    ui = Ui_TreeBaseWidget()
    ui.setupUi(TreeBaseWidget)
    TreeBaseWidget.show()
    sys.exit(app.exec_())

