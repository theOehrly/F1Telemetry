import cv2

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QResizeEvent, QInputEvent, QPainter, QPen, QPalette
from PyQt5 import QtCore

from ui.ui_videoplayerwidget import Ui_VideoPlayer
from videosource import VideoSource


class Overlay(QWidget):
    """Overlay for drawing selection ontop of display widget """
    def __init__(self, parent):
        super().__init__(parent.lbl_display)

        self.parent = parent

        palette = QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)
        self.setPalette(palette)

        self.hide()

    def paintEvent(self, event):
        x = ((self.parent.selection.x + 1) * self.parent.videoscale) + self.parent.display_margins[0]
        y = ((self.parent.selection.y + 1) * self.parent.videoscale) + self.parent.display_margins[1]
        r = self.parent.selection.radius * self.parent.videoscale

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(QtCore.Qt.red, 1.0))
        painter.drawEllipse(x - r, y - r, 2*r, 2*r)

        painter.setPen(QPen(QtCore.Qt.red, 4.0))
        painter.drawPoint(x, y)

        painter.setPen(QPen(QtCore.Qt.NoPen))


class VideoPlayerWidget(QWidget, Ui_VideoPlayer):
    """A Videoplayer that features variable playback speed, frame by frame and a draggable timeline slider."""
    def __init__(self, parentwidget, selection_data):
        super().__init__(parentwidget)

        # the videosource handles reading and delivering frames as well as seeking, playbackspeed,...
        self.videosource = VideoSource()

        self.selection = selection_data  # selected region of interest and timeframe for OCR

        self.setupUi(self)

        self.videores = [0, 0]
        self.videoaspectratio = float()
        self.videoscale = float()  # scaling factor; display video size / original video size
        self.display_margins = (0, 0)  # (right/left, top/bottom); margins added around label pixmap

        self.playing = False
        self.was_playing = False
        self.singleframe = False
        self.frame = None
        self.frame_pos = 0
        self.frame_duration = 0

        # a new frame is drawn every time the timer times out
        # the timer interval is set depending on the frame duration calculated for each frame by the videosource
        self.frame_timer = QtCore.QTimer()
        self.frame_timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.frame_timer.timeout.connect(self.draw_next_frame)

        self.overlay = Overlay(self)

        self.init_ui()
        self.show()

    def init_ui(self):
        """Called once when started to connect functions to all buttons and setup mouse tracking on display lable."""
        # playpause button
        self.btn_playpause.clicked.connect(self.playpause)

        # playback speed slider
        self.slider_speed.valueChanged.connect(lambda: self.change_playback_speed(self.slider_speed.value()))

        # frame by frame buttons
        self.btn_previousframe.clicked.connect(self.previous_frame)
        self.btn_nextframe.clicked.connect(self.next_frame)

        # mouse tracking for manipulating selection
        self.lbl_display.setScaledContents(True)
        self.lbl_display.setMouseTracking(True)
        self.lbl_display.installEventFilter(self)

        # set bind to frame start/zero/end selection buttons
        self.btn_markstart.clicked.connect(self.set_start_frame)
        self.btn_markend.clicked.connect(self.set_end_frame)
        self.btn_markzero.clicked.connect(self.set_zero_frame)

    def open_file(self, filepath):
        """Opens a videofile; currently fails silent if the file can not be opened."""
        self.videosource.open_file(filepath)
        # videosource discards any files that don't seem to be videofiles
        # in that case videosource.capture will be None
        self.load_video()
        self.overlay.show()

    def load_video(self):
        """Initalize UI elements and internal variables for current videofile, i.e. set duration,... """
        if self.videosource.capture:
            self.videores = [self.videosource.capture.get(cv2.CAP_PROP_FRAME_WIDTH),
                             self.videosource.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)]
            self.videoaspectratio = self.videores[0]/self.videores[1]

            # video progress slider
            str_total = self.format_frame_time(self.videosource.total_frames, self.videosource.duration)
            self.lbl_markend.setText(str_total)
            self.lbl_playbacktotal.setText(str_total)

            self.slider_videopos.setMaximum(self.videosource.total_frames)
            self.slider_videopos.sliderPressed.connect(self.slider_videopos_pressed)
            self.slider_videopos.sliderReleased.connect(self.slider_videopos_released)
            self.slider_videopos.sliderMoved.connect(self.slider_videopos_value_changed)

            # set selection to something sane
            self.selection.set_x(self.videores[0] / 2)
            self.selection.set_y(self.videores[1] / 2)
            self.selection.set_radius(self.videores[1] / 6)

            # draw first frame, scale it properly and enable control buttons
            self.singleframe = True
            self.draw_next_frame()
            self.update_display_margins()
            self.enable_vidctrl_btns()

        else:
            self.disable_vidctrl_btns()

    def eventFilter(self, _object, _event):
        """Custom Filter for intercepting mouse and scrollwheel for selection manipulation as well as rescaling."""
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
            self.update_display_margins()
            self.calculate_videoscale()
            self.overlay.resize(_event.size())
            return True
        return False

    def calculate_videoscale(self):
        """Calculates the current scaling factor of the video (current size / original size)"""
        try:
            self.videoscale = self.lbl_display.contentsRect().width() / self.videores[0]
        except ZeroDivisionError:
            # happens if no video file is loaded
            self.videoscale = 1

    def update_display_margins(self):
        """Adds margins to the display labels content so that the video is always as large as possible
        without beeing distorted."""
        try:
            lblaspectratio = self.lbl_display.width()/self.lbl_display.height()
        except ZeroDivisionError:
            return  # Zero Divison Error may happen when initializing widget, there is now image shown yet, do nothing

        if lblaspectratio > self.videoaspectratio:
            # too wide
            m = int((self.lbl_display.width() - self.lbl_display.height() * self.videoaspectratio) / 2)
            self.display_margins = (m, 0)

        elif lblaspectratio < self.videoaspectratio:
            # too tall
            m = int((self.lbl_display.height() - self.lbl_display.width() / self.videoaspectratio) / 2)
            self.display_margins = (0, m)

        self.lbl_display.setContentsMargins(self.display_margins[0], self.display_margins[1],
                                            self.display_margins[0], self.display_margins[1])

    def draw_next_frame(self, set_slider=True):
        """Fetches the next frame from the videosource, call for a pixmap update and updates playback progress."""
        if self.singleframe:
            # function may need to briefly wait for the videosource to fill up its buffer after a change of direction
            # only wait when the user requests a singel frame
            while not self.videosource.frame_buffer:
                continue
            self.singleframe = False

        ret = self.videosource.get_frame()
        if not ret:
            return  # no frame, do nothing

        self.frame, self.frame_pos, frame_duration = ret
        if frame_duration != self.frame_duration:
            self.frame_timer.setInterval(int(frame_duration))
            self.frame_duration = frame_duration
        self.update_pixmap()

        # update progressbar and text
        str_current = self.format_frame_time(self.frame_pos, self.frame_pos / self.videosource.source_fps)
        self.lbl_playbackpos.setText(str_current)
        # set slider (is not set when seeking by dragging slider)
        if set_slider:
            self.slider_videopos.setValue(self.frame_pos)

    def update_pixmap(self):
        """Draws the current self.frame on the display label."""
        self.lbl_display.setPixmap(self.frame)

    def slider_videopos_pressed(self):
        """Is called when the slider is clicked. The current playback state is saved and playback is stopped."""
        self.was_playing = self.playing
        self.stop_playback()

    def slider_videopos_released(self):
        """Is called when the progess slider is released. Resumes playback if video was plaing before."""
        if self.was_playing:
            self.start_playback()

    def slider_videopos_value_changed(self):
        """Is called when the slider is dragged by the user.
        Tells the videosource to seek to the new position. The new frame is also drawn immediatly."""
        self.videosource.set_seek_target(int(self.slider_videopos.value()))
        self.draw_next_frame(set_slider=False)

    def start_playback(self):
        """Starts frame timer and updates playback state."""
        self.frame_timer.start(self.videosource.playback_frame_duration)
        self.playing = True

    def stop_playback(self):
        """Stops frame timer and updates playback state."""
        self.frame_timer.stop()
        self.playing = False

    def playpause(self):
        """Pauses or resumes playback depending on current state and enables/disables advanced functions accordingly"""
        if self.playing:
            self.stop_playback()
            self.enable_frame_by_frame()
            self.overlay.show()
        elif self.videosource.capture:
            self.change_playback_speed(self.slider_speed.value())
            self.start_playback()
            self.disable_frame_by_frame()
            self.overlay.hide()

    def enable_frame_by_frame(self):
        """Enables buttons for Frame by Frame control as well as timing marker buttons."""
        self.btn_previousframe.setDisabled(0)
        self.btn_nextframe.setDisabled(0)
        self.btn_markstart.setDisabled(0)
        self.btn_markend.setDisabled(0)
        self.btn_markzero.setDisabled(0)

    def disable_frame_by_frame(self):
        """Disables buttons for Frame by Frame control as well as timing marker buttons."""
        self.btn_previousframe.setDisabled(1)
        self.btn_nextframe.setDisabled(1)
        self.btn_markstart.setDisabled(1)
        self.btn_markend.setDisabled(1)
        self.btn_markzero.setDisabled(1)

    def disable_vidctrl_btns(self):
        """Disables all video control buttons as well as timing marker buttons."""
        self.btn_previousframe.setDisabled(1)
        self.btn_nextframe.setDisabled(1)
        self.btn_markstart.setDisabled(1)
        self.btn_markend.setDisabled(1)
        self.btn_markzero.setDisabled(1)
        self.btn_playpause.setDisabled(1)

    def enable_vidctrl_btns(self):
        """Enables all video control buttons as well as timing marker buttons."""
        self.btn_previousframe.setDisabled(0)
        self.btn_nextframe.setDisabled(0)
        self.btn_markstart.setDisabled(0)
        self.btn_markend.setDisabled(0)
        self.btn_markzero.setDisabled(0)
        self.btn_playpause.setDisabled(0)

    def change_playback_speed(self, speed):
        """Called when the playback speed slider is moved."""
        speed /= 10  # Slider values are times factor ten for provding one deciaml place accuracy
        self.lbl_playbackspeed.setText(str(speed))  # update the info lable
        if speed == 0:
            # playback is stopped when the speed is set to zero
            self.stop_playback()
            self.enable_frame_by_frame()
        elif speed != 0 and not self.playing:
            # resume playback when moving slider away from zero position
            self.disable_frame_by_frame()
            self.videosource.set_playback_speed(speed)
            self.start_playback()
        else:
            self.videosource.set_playback_speed(speed)

    def next_frame(self):
        """Called by next frame button in frame by frame mode."""
        self.singleframe = True
        self.videosource.set_playback_speed(1)
        self.draw_next_frame()

    def previous_frame(self):
        """Called by previous frame button in frame by frame mode."""
        self.singleframe = True
        self.videosource.set_playback_speed(-1)
        self.draw_next_frame()

    def mouse_drag(self, _event):
        """Calcultes image cordinates from diplay coordinates and updates the selection."""
        if not self.videosource.capture:
            return
        # move selection when dragging mouse in video
        size = self.lbl_display.contentsRect()

        # because of padding mouse coordinates in label may not be the same as the coordinates of the mouse in the
        # actual video frame; proper coordinates need to be calculated based on pixmap padding and scaling
        selection_x = int((_event.x() - size.x()) / self.videoscale)
        selection_y = int((_event.y() - size.y()) / self.videoscale)

        if selection_x >= 0:
            self.selection.set_x(selection_x)
        if selection_y >= 0:
            self.selection.set_y(selection_y)

        # only redraw frame when not playing to save unnecessary pixmap updates
        if not self.playing:
            self.update_pixmap()

    def mouse_scroll(self, _event):
        """Updates selection size by scrolling."""
        if not self.videosource.capture:
            return
        # increase or decrease selection size by scrolling
        if _event.angleDelta().y() > 0:
            self.selection.set_radius_delta(1)
        elif _event.angleDelta().y() < 0 and self.selection.radius > 0:
            self.selection.set_radius_delta(-1)

        # only redraw frame when not playing to save unnecessary pixmap updates
        if not self.playing:
            self.update_pixmap()

    def set_start_frame(self):
        """Sets the current frame as start of the selection."""
        self.selection.set_start_frame(self.frame_pos)
        self.lbl_markstart.setText(self.format_frame_time(self.frame_pos,
                                                          self.frame_pos/self.videosource.source_fps))

    def set_end_frame(self):
        """Sets the current frame as endof the selection."""
        self.selection.set_end_frame(self.frame_pos)
        self.lbl_markend.setText(self.format_frame_time(self.frame_pos,
                                                        self.frame_pos/self.videosource.source_fps))

    def set_zero_frame(self):
        """Sets the current frame as zero time of the selection."""
        self.selection.set_zero_frame(self.frame_pos)
        self.lbl_markzero.setText(self.format_frame_time(self.frame_pos,
                                                         self.frame_pos/self.videosource.source_fps))

    @staticmethod
    def format_frame_time(frames, seconds):
        """Returns a string containing frame and time in desired format for displaying on the lables."""
        return "{:d}f / {:.2f}s".format(int(frames), seconds)
