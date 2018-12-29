import sys
import cv2

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent, QResizeEvent
from PyQt5 import QtCore

from ui_mainwindow import Ui_MainWindow
from videosource import VideoSource


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.selection = [81, 359, 42]
        self.videores = [640, 360]
        self.videoaspectratio = self.videores[0]/self.videores[1]

        # self.ui = ui_mainwindow.Ui_MainWindow()
        self.setupUi(self)
        self.playing = False
        self.was_playing = False

        self.frame_timer = QtCore.QTimer()
        self.frame_timer.timeout.connect(self.load_next_frame)

        self.videosource = VideoSource('D:\\Dateien\\Projekte\\F1Telemetry\\Races\\2018\\Brasilien\\vettelq3.mp4')

        self.init_ui()

    def init_ui(self):
        # playpause button
        self.btn_playpause.clicked.connect(self.playpause)

        # playback speed slider
        self.slider_speed.valueChanged.connect(lambda: self.change_playback_speed(self.slider_speed.value()))

        # video progress slider
        str_total = self.format_frame_time(self.videosource.total_frames, self.videosource.duration)
        self.lbl_markend.setText(str_total)
        self.lbl_playbacktotal.setText(str_total)

        self.slider_videopos.setMaximum(self.videosource.total_frames)
        self.slider_videopos.sliderPressed.connect(self.slider_videopos_pressed)
        self.slider_videopos.sliderReleased.connect(self.slider_videopos_released)
        self.slider_videopos.sliderMoved.connect(self.slider_videopos_value_changed)

        # frame by frame buttons
        self.btn_previousframe.clicked.connect(self.previous_frame)
        self.btn_nextframe.clicked.connect(self.next_frame)

        # mouse tracking for manipulating selection
        self.lbl_display.setScaledContents(True)
        self.lbl_display.setMouseTracking(True)
        self.lbl_display.installEventFilter(self)

        self.load_next_frame()
        self.show()

    def eventFilter(self, _object, _event):
        if _event.type() == QMouseEvent.MouseMove and _event.buttons() == QtCore.Qt.LeftButton:
            _event.accept()
            print('move', _event.x(), _event.y())
            return True
        if _event.type() == QResizeEvent.Resize:
            _event.accept()
            self.update_displaylbl_margins()
            return True
        return False

    def update_displaylbl_margins(self):
        lblaspectratio = self.lbl_display.width()/self.lbl_display.height()
        if lblaspectratio > self.videoaspectratio:
            # too wide
            m = int(self.lbl_display.width() - self.lbl_display.height() * self.videoaspectratio)
            self.lbl_display.setContentsMargins(m/2, 0, m/2, 0)

        elif lblaspectratio < self.videoaspectratio:
            # too tall
            m = int(self.lbl_display.height() - self.lbl_display.width() / self.videoaspectratio)
            self.lbl_display.setContentsMargins(0, m/2, 0, m/2)

    def load_next_frame(self, set_slider=True):
        frame, frame_pos, frame_duration = self.videosource.get_frame()
        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1]*3, QImage.Format_RGB888)
        self.lbl_display.setPixmap(QPixmap(img))

        str_current = self.format_frame_time(frame_pos, frame_pos/self.videosource.source_fps)
        self.lbl_playbackpos.setText(str_current)
        if set_slider:
            self.slider_videopos.setValue(frame_pos)

    def slider_videopos_pressed(self):
        self.was_playing = self.playing
        self.stop_playback()

    def slider_videopos_released(self):
        if self.was_playing:
            self.start_playback()

    def slider_videopos_value_changed(self):
        self.seek_to(self.slider_videopos.value())

    def start_playback(self):
        self.frame_timer.start(self.videosource.playback_frame_duration)
        self.playing = True

    def stop_playback(self):
        self.frame_timer.stop()
        self.playing = False

    def playpause(self):
        if self.playing:
            self.stop_playback()
            self.enable_frame_by_frame()
        else:
            self.change_playback_speed(self.slider_speed.value())
            self.start_playback()
            self.disable_frame_by_frame()

    def enable_frame_by_frame(self):
        self.btn_previousframe.setDisabled(0)
        self.btn_nextframe.setDisabled(0)
        self.btn_markstart.setDisabled(0)
        self.btn_markend.setDisabled(0)
        self.btn_markzero.setDisabled(0)

    def disable_frame_by_frame(self):
        self.btn_previousframe.setDisabled(1)
        self.btn_nextframe.setDisabled(1)
        self.btn_markstart.setDisabled(1)
        self.btn_markend.setDisabled(1)
        self.btn_markzero.setDisabled(1)

    def change_playback_speed(self, speed):
        speed /= 10
        self.lbl_playbackspeed.setText(str(speed))
        if speed == 0:
            self.stop_playback()
            # self.videosource.playback_direction = 1
            self.enable_frame_by_frame()
        elif speed != 0 and not self.playing:
            self.disable_frame_by_frame()
            self.videosource.set_playback_speed(speed)
            # start playback
            self.start_playback()
        else:
            self.videosource.set_playback_speed(speed)
            self.frame_timer.setInterval(self.videosource.playback_frame_duration)

    def seek_to(self, frame):
        self.videosource.seek_to(int(frame))
        self.load_next_frame(set_slider=False)

    def next_frame(self):
        self.videosource.set_playback_speed(1)
        self.load_next_frame()

    def previous_frame(self):
        self.videosource.set_playback_speed(-1)
        self.load_next_frame()

    @staticmethod
    def format_frame_time(frames, seconds):
        return "{:d}f / {:.2f}s".format(int(frames), seconds)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainui = MainUI()
    sys.exit(app.exec())
