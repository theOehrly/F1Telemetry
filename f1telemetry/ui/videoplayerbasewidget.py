# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/videoplayerbasewidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VideoPlayer(object):
    def setupUi(self, VideoPlayer):
        VideoPlayer.setObjectName("VideoPlayer")
        VideoPlayer.resize(1021, 709)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VideoPlayer.sizePolicy().hasHeightForWidth())
        VideoPlayer.setSizePolicy(sizePolicy)
        VideoPlayer.setMinimumSize(QtCore.QSize(1000, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(VideoPlayer)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_display = QtWidgets.QLabel(VideoPlayer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_display.sizePolicy().hasHeightForWidth())
        self.lbl_display.setSizePolicy(sizePolicy)
        self.lbl_display.setMinimumSize(QtCore.QSize(0, 0))
        self.lbl_display.setText("")
        self.lbl_display.setPixmap(QtGui.QPixmap("example.png"))
        self.lbl_display.setScaledContents(True)
        self.lbl_display.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_display.setObjectName("lbl_display")
        self.verticalLayout.addWidget(self.lbl_display)
        self.line = QtWidgets.QFrame(VideoPlayer)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.control_elements = QtWidgets.QWidget(VideoPlayer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.control_elements.sizePolicy().hasHeightForWidth())
        self.control_elements.setSizePolicy(sizePolicy)
        self.control_elements.setMinimumSize(QtCore.QSize(0, 0))
        self.control_elements.setObjectName("control_elements")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.control_elements)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Control1 = QtWidgets.QHBoxLayout()
        self.Control1.setObjectName("Control1")
        self.lbl_playbackpos = QtWidgets.QLabel(self.control_elements)
        self.lbl_playbackpos.setObjectName("lbl_playbackpos")
        self.Control1.addWidget(self.lbl_playbackpos)
        self.slider_videopos = QtWidgets.QSlider(self.control_elements)
        self.slider_videopos.setPageStep(10)
        self.slider_videopos.setTracking(True)
        self.slider_videopos.setOrientation(QtCore.Qt.Horizontal)
        self.slider_videopos.setObjectName("slider_videopos")
        self.Control1.addWidget(self.slider_videopos)
        self.lbl_playbacktotal = QtWidgets.QLabel(self.control_elements)
        self.lbl_playbacktotal.setMinimumSize(QtCore.QSize(100, 0))
        self.lbl_playbacktotal.setObjectName("lbl_playbacktotal")
        self.Control1.addWidget(self.lbl_playbacktotal)
        self.verticalLayout_3.addLayout(self.Control1)
        self.Control2 = QtWidgets.QHBoxLayout()
        self.Control2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.Control2.setObjectName("Control2")
        self.PlaybackControls = QtWidgets.QWidget(self.control_elements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlaybackControls.sizePolicy().hasHeightForWidth())
        self.PlaybackControls.setSizePolicy(sizePolicy)
        self.PlaybackControls.setMinimumSize(QtCore.QSize(0, 0))
        self.PlaybackControls.setMaximumSize(QtCore.QSize(170, 16777215))
        self.PlaybackControls.setObjectName("PlaybackControls")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.PlaybackControls)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_previousframe = QtWidgets.QPushButton(self.PlaybackControls)
        self.btn_previousframe.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_previousframe.sizePolicy().hasHeightForWidth())
        self.btn_previousframe.setSizePolicy(sizePolicy)
        self.btn_previousframe.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btn_previousframe.setObjectName("btn_previousframe")
        self.horizontalLayout.addWidget(self.btn_previousframe)
        self.btn_playpause = QtWidgets.QPushButton(self.PlaybackControls)
        self.btn_playpause.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_playpause.setObjectName("btn_playpause")
        self.horizontalLayout.addWidget(self.btn_playpause)
        self.btn_nextframe = QtWidgets.QPushButton(self.PlaybackControls)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_nextframe.sizePolicy().hasHeightForWidth())
        self.btn_nextframe.setSizePolicy(sizePolicy)
        self.btn_nextframe.setMaximumSize(QtCore.QSize(30, 16777215))
        self.btn_nextframe.setObjectName("btn_nextframe")
        self.horizontalLayout.addWidget(self.btn_nextframe)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout.setStretch(2, 1)
        self.Control2.addWidget(self.PlaybackControls)
        self.lbl_playbackspeed = QtWidgets.QLabel(self.control_elements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_playbackspeed.sizePolicy().hasHeightForWidth())
        self.lbl_playbackspeed.setSizePolicy(sizePolicy)
        self.lbl_playbackspeed.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lbl_playbackspeed.setObjectName("lbl_playbackspeed")
        self.Control2.addWidget(self.lbl_playbackspeed)
        self.slider_speed = QtWidgets.QSlider(self.control_elements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slider_speed.sizePolicy().hasHeightForWidth())
        self.slider_speed.setSizePolicy(sizePolicy)
        self.slider_speed.setMaximumSize(QtCore.QSize(300, 16777215))
        self.slider_speed.setMinimum(-50)
        self.slider_speed.setMaximum(50)
        self.slider_speed.setSingleStep(1)
        self.slider_speed.setPageStep(2)
        self.slider_speed.setProperty("value", 10)
        self.slider_speed.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_speed.setTickInterval(10)
        self.slider_speed.setObjectName("slider_speed")
        self.Control2.addWidget(self.slider_speed)
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Control2.addItem(spacerItem)
        self.MarkButtons = QtWidgets.QWidget(self.control_elements)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MarkButtons.sizePolicy().hasHeightForWidth())
        self.MarkButtons.setSizePolicy(sizePolicy)
        self.MarkButtons.setMinimumSize(QtCore.QSize(0, 0))
        self.MarkButtons.setObjectName("MarkButtons")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.MarkButtons)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_markstart = QtWidgets.QPushButton(self.MarkButtons)
        self.btn_markstart.setMinimumSize(QtCore.QSize(100, 0))
        self.btn_markstart.setObjectName("btn_markstart")
        self.horizontalLayout_5.addWidget(self.btn_markstart)
        spacerItem1 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.lbl_markstart = QtWidgets.QLabel(self.MarkButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_markstart.sizePolicy().hasHeightForWidth())
        self.lbl_markstart.setSizePolicy(sizePolicy)
        self.lbl_markstart.setMinimumSize(QtCore.QSize(100, 0))
        self.lbl_markstart.setObjectName("lbl_markstart")
        self.horizontalLayout_5.addWidget(self.lbl_markstart)
        self.btn_markzero = QtWidgets.QPushButton(self.MarkButtons)
        self.btn_markzero.setMinimumSize(QtCore.QSize(100, 0))
        self.btn_markzero.setObjectName("btn_markzero")
        self.horizontalLayout_5.addWidget(self.btn_markzero)
        spacerItem2 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.lbl_markzero = QtWidgets.QLabel(self.MarkButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_markzero.sizePolicy().hasHeightForWidth())
        self.lbl_markzero.setSizePolicy(sizePolicy)
        self.lbl_markzero.setMinimumSize(QtCore.QSize(100, 0))
        self.lbl_markzero.setObjectName("lbl_markzero")
        self.horizontalLayout_5.addWidget(self.lbl_markzero)
        self.btn_markend = QtWidgets.QPushButton(self.MarkButtons)
        self.btn_markend.setMinimumSize(QtCore.QSize(100, 0))
        self.btn_markend.setObjectName("btn_markend")
        self.horizontalLayout_5.addWidget(self.btn_markend)
        spacerItem3 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.lbl_markend = QtWidgets.QLabel(self.MarkButtons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_markend.sizePolicy().hasHeightForWidth())
        self.lbl_markend.setSizePolicy(sizePolicy)
        self.lbl_markend.setMinimumSize(QtCore.QSize(100, 0))
        self.lbl_markend.setObjectName("lbl_markend")
        self.horizontalLayout_5.addWidget(self.lbl_markend)
        self.Control2.addWidget(self.MarkButtons)
        self.verticalLayout_3.addLayout(self.Control2)
        self.verticalLayout.addWidget(self.control_elements)

        self.retranslateUi(VideoPlayer)
        QtCore.QMetaObject.connectSlotsByName(VideoPlayer)

    def retranslateUi(self, VideoPlayer):
        _translate = QtCore.QCoreApplication.translate
        VideoPlayer.setWindowTitle(_translate("VideoPlayer", "Form"))
        self.lbl_playbackpos.setText(_translate("VideoPlayer", "93f / 2.63s"))
        self.lbl_playbacktotal.setText(_translate("VideoPlayer", "2808f / 93.78s"))
        self.btn_previousframe.setText(_translate("VideoPlayer", "<"))
        self.btn_playpause.setText(_translate("VideoPlayer", "Play"))
        self.btn_nextframe.setText(_translate("VideoPlayer", ">"))
        self.lbl_playbackspeed.setText(_translate("VideoPlayer", "1.0"))
        self.btn_markstart.setText(_translate("VideoPlayer", "Mark Start"))
        self.lbl_markstart.setText(_translate("VideoPlayer", "0f / 0s"))
        self.btn_markzero.setText(_translate("VideoPlayer", "Mark Zero"))
        self.lbl_markzero.setText(_translate("VideoPlayer", "0f / 0s"))
        self.btn_markend.setText(_translate("VideoPlayer", "Mark End"))
        self.lbl_markend.setText(_translate("VideoPlayer", "2000f / 125.3s"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VideoPlayer = QtWidgets.QWidget()
    ui = Ui_VideoPlayer()
    ui.setupUi(VideoPlayer)
    VideoPlayer.show()
    sys.exit(app.exec_())

