import sys
import cv2
import copy

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap, QResizeEvent, QInputEvent
from PyQt5 import QtCore

from ui_mainwindow import Ui_MainWindow
from videosource import VideoSource
from datastruct import SelectionData


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self, selection_data, videofile):
        super().__init__()

        self.videosource = VideoSource(videofile)
        self.selection = selection_data
        self.videores = [self.videosource.capture.get(cv2.CAP_PROP_FRAME_WIDTH),
                         self.videosource.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)]
        self.videoaspectratio = self.videores[0]/self.videores[1]

        # self.ui = ui_mainwindow.Ui_MainWindow()
        self.setupUi(self)
        self.playing = False
        self.was_playing = False
        self.frame = None
        self.frame_pos = 0

        self.frame_timer = QtCore.QTimer()
        self.frame_timer.timeout.connect(self.load_next_frame)

        self.init_ui()

    def closeEvent(self, *args, **kwargs):
        self.videosource.release()
        super().closeEvent(*args, **kwargs)

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

        # set selection to something sane
        self.selection.set_x(self.videores[0] / 2)
        self.selection.set_y(self.videores[1] / 2)
        self.selection.set_radius(self.videores[1] / 6)

        # set bind to frame start/zero/end selection buttons
        self.btn_markstart.clicked.connect(self.set_start_frame)
        self.btn_markend.clicked.connect(self.set_end_frame)
        self.btn_markzero.clicked.connect(self.set_zero_frame)

        self.load_next_frame()
        self.show()

    def eventFilter(self, _object, _event):
        if _event.type() == QInputEvent.MouseMove and _event.buttons() == QtCore.Qt.LeftButton:
            _event.accept()
            self.mouse_drag(_event)
            return True
        elif _event.type() == QInputEvent.Wheel:
            _event.accept()
            self.mouse_scroll(_event)
            return True
        elif _event.type() == QResizeEvent.Resize:
            _event.accept()
            self.update_lbldisplay_margins()
            return True
        return False

    def update_lbldisplay_margins(self):
        lblaspectratio = self.lbl_display.width()/self.lbl_display.height()
        if lblaspectratio > self.videoaspectratio:
            # too wide
            m = int((self.lbl_display.width() - self.lbl_display.height() * self.videoaspectratio) / 2)
            self.lbl_display.setContentsMargins(m, 0, m, 0)

        elif lblaspectratio < self.videoaspectratio:
            # too tall
            m = int((self.lbl_display.height() - self.lbl_display.width() / self.videoaspectratio) / 2)
            self.lbl_display.setContentsMargins(0, m, 0, m)

    def load_next_frame(self, set_slider=True):
        # get next frame and draw it on label
        ret_val = self.videosource.get_frame()
        if not ret_val:
            return
        self.frame, self.frame_pos, frame_duration = ret_val
        self.draw_frame()

        # update progressbar and text
        str_current = self.format_frame_time(self.frame_pos, self.frame_pos / self.videosource.source_fps)
        self.lbl_playbackpos.setText(str_current)
        # set slider (is not set when seeking by dragging slider)
        if set_slider:
            self.slider_videopos.setValue(self.frame_pos)

    def draw_frame(self):
        # draw the current frame on th label and
        # first the currently selected region is marked using opencv
        frame = cv2.circle(copy.copy(self.frame), (self.selection.x, self.selection.y), self.selection.radius,
                           (255, 0, 0, 255), 1, cv2.LINE_AA)  # outer circle

        cv2.circle(frame, (self.selection.x, self.selection.y), 3, (255, 0, 0, 255), -1, cv2.LINE_AA)  # center point

        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        self.lbl_display.setPixmap(QPixmap(img))

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

    def mouse_drag(self, _event):
        # move selection when dragging mouse in video
        size = self.lbl_display.contentsRect()

        # because of padding mouse coordinates in label may not be the same as the coordinates of the mouse in the
        # actual video frame; proper coordinates need to be calculated based on pixmap padding and scaling
        selection_x = int((_event.x() - size.x()) * self.videores[0] / size.width())
        selection_y = int((_event.y() - size.y()) * self.videores[1] / size.height())

        if selection_x >= 0:
            self.selection.set_x(selection_x)
        if selection_y >= 0:
            self.selection.set_y(selection_y)

        # only redraw frame when not playing to save unnecessary pixmap updates
        if not self.playing:
            self.draw_frame()

    def mouse_scroll(self, _event):
        # increase or decrease selection size by scrolling
        if _event.angleDelta().y() > 0:
            self.selection.set_radius_delta(1)
        elif _event.angleDelta().y() < 0 and self.selection.radius > 0:
            self.selection.set_radius_delta(-1)

        # only redraw frame when not playing to save unnecessary pixmap updates
        if not self.playing:
            self.draw_frame()

    def set_start_frame(self):
        self.selection.set_start_frame(self.frame_pos)
        self.lbl_markstart.setText(self.format_frame_time(self.frame_pos,
                                                          self.frame_pos/self.videosource.source_fps))

    def set_end_frame(self):
        self.selection.set_end_frame(self.frame_pos)
        self.lbl_markend.setText(self.format_frame_time(self.frame_pos,
                                                        self.frame_pos/self.videosource.source_fps))

    def set_zero_frame(self):
        self.selection.set_zero_frame(self.frame_pos)
        self.lbl_markzero.setText(self.format_frame_time(self.frame_pos,
                                                         self.frame_pos/self.videosource.source_fps))

    @staticmethod
    def format_frame_time(frames, seconds):
        return "{:d}f / {:.2f}s".format(int(frames), seconds)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainui = MainUI()
    sys.exit(app.exec())
