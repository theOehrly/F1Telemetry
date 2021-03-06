import cv2
import collections
import threading
from PyQt5.QtGui import QPixmap, QImage
import time

# Video source class - the following actions are supported
#  - forward and reverse playback
#       (reverse playback is slow; this is an inherent issue of videodecoding)
#  - seeking to a specified frame
#  - change playback speed while playing
#       (at playback speeds above two times source fps the videosource skips frames to be faster)
#  - frame by frame playback (forward and reverse) is supported through default get_frame method


class VideoSource:
    """OpenCV based videosource that provides single frames.
    Features: variable playback speed (also reverse), frame by frame mode, seek to a specific frame
    Frames are read in a seperate thread."""
    def __init__(self, videofile=None):
        self.capture = None

        # some information about the source file; values are constants
        self.source_fps = 0  # video fps
        self.source_frame_duration = 0  # duration of one frame
        self.total_frames = 0
        self.duration = 0  # video duration

        if videofile:
            self.open_file(videofile)

        # threaded frame loading into a buffer
        self.frame_buffer = collections.deque()
        # a deque with target length 1 used because of access from multiple threads
        # it ensures that even if when timing between threads is not as expected
        # no frames get skipped or lost, as the deque can increase length
        # the code supports longer buffer length but currently this leads to a slugish user
        # experience as most imortantly playback speed changes are not happening instantaneous then
        self.frame_buffer_length = 5
        self.buffer_reload_thread = None

        # playback controls
        self.playback_direction = 1  # either 1 (forward) or -1 (backward)
        self.seek_target = None  # target frame; gets set when seeking was requested
        self.frame_skip_factor = 1  # 1=every frame, 2=every 2nd frame, ... used for high playback speeds
        self.playback_frame_duration = 0  # can be different from source due to playbackspeed
        # playback_frame_duration is used by the GUI to determine frame timing. It also changes depending on
        # frame skipping therefore it is calculated by the videosource

        self.continous_buffer_thread = None

    def open_file(self, filepath):
        """Opens the the provided file."""
        try:
            if self.capture:
                self.release()
                self.continous_buffer_thread.join()

            self.capture = cv2.VideoCapture(filepath)  # video source
            if not self.capture.get(cv2.CAP_PROP_FRAME_COUNT):
                self.capture.release()
                self.capture = None
                return  # if ain't got no frames it ain't no videofile
            self.load_source_info()
            self.frame_buffer.clear()
            self.continous_buffer_thread = threading.Thread(target=self.continious_buffer)
            self.continous_buffer_thread.start()
        except Exception as e:
            print('Error while opening file: ', e)

    def load_source_info(self):
        """Loads required video info when a new file is opened. (internal)"""
        if self.capture:
            # some information about the source file; values are constants
            self.source_fps = self.capture.get(cv2.CAP_PROP_FPS)  # video fps
            self.source_frame_duration = int(1000 / self.source_fps)  # duration of one frame
            self.playback_frame_duration = self.source_frame_duration
            self.total_frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
            self.duration = self.total_frames / self.source_fps  # video duration

    def continious_buffer(self):
        try:
            while self.capture:
                if len(self.frame_buffer) < self.frame_buffer_length:
                    # buffer has not as many frames as it should have
                    if not (self.capture.get(cv2.CAP_PROP_POS_FRAMES) == self.total_frames and
                            self.playback_direction > 0):
                            # if we're at the end and should play forward don't top up the buffer
                        self.top_up_buffer()
                    elif self.seek_target and not self.seek_target == self.total_frames:
                        # BUT, if we're at the end and a seek target is set to something different than the end do it
                        self.top_up_buffer()
                    else:
                        time.sleep(0.1)
                else:
                    time.sleep(0.1)
        except Exception as e:
            print(e)

    def top_up_buffer(self):
        """Adds a new frame to the frame buffer. (internal)"""
        if not self.capture:
            return

        self.modify_capture_position()  # takes care of seeking, frame skipping and reverse playback
        frame_pos = self.capture.get(cv2.CAP_PROP_POS_FRAMES)
        ok, frame = self.capture.read()
        if ok:
            img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
                         QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap(img)
            self.frame_buffer.appendleft((pixmap, frame_pos, self.playback_frame_duration))
            # every frame is added together with info about it's position and the calculated duration

    def modify_capture_position(self):
        """Handles advanced playback functionality like reverse, seeking and frame skipping. (internal)"""
        if self.seek_target:
            # set new position
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.seek_target)

            # clear buffer and refill as frames in it just got useless
            self.frame_buffer.clear()

            # reset seek target so we don't seek to it again
            self.seek_target = None

        elif self.playback_direction == -1:
            # play reverse
            frame_position_is = self.capture.get(cv2.CAP_PROP_POS_FRAMES)
            if frame_position_is >= 0:
                # set new timecode
                frame_position_new = frame_position_is - 2 - (self.frame_skip_factor - 1)
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_position_new)

        elif self.frame_skip_factor != 1:
            # play forward but speed is greater than 2, so we skip some frames
            # the most effective way of doing this (when playing forwards) is reading the frames but just don't use them
            for _ in range(self.frame_skip_factor-1):
                self.capture.read()

    def get_frame(self):
        """Returns the next frame from the buffer together wit info about it's positon and duration."""
        if self.frame_buffer:
            fd = self.frame_buffer.pop()
            # If playbackspeed is slower than realtime, the precalculated frame duration is substituted with the current
            # frame duration. At slow speeds frames spent rather long time in the buffer, so the calculated timing
            # may no longer be correct if the user changed the playback speed in between.
            # Substitution is not done at higher speeds as it might mess up transitions when frame skipping. This means
            # that playback speed changes are technically not instantaneous but lag behind a few frames.
            if fd[2] > self.source_frame_duration:
                return fd[0], fd[1], self.playback_frame_duration
            else:
                return fd
        return None

    def get_raw_frame(self):
        """Returns next frame directly from source (non threaded!). Speed, direction and seek targets are ignored!"""
        return self.capture.read()

    def set_seek_target(self, frame):
        """Sets a seek target. Actual seeking of the capture is done when the next frame is loaded in to the buffer."""
        self.seek_target = frame

    def set_playback_speed(self, speed):
        """Sets a new playback speed.
        Also handles reversing (if necessary) and frame skipping for playback speeds greater than times two."""

        dir_old_new = speed * self.playback_direction
        # if old and new are the same direction this results in a positive value
        # if direction changes the value is negative

        if speed > 0:
            self.playback_direction = 1
        elif speed < 0:
            self.playback_direction = -1

        if dir_old_new < 0:
            # playback direction changed
            try:
                seek_target = self.frame_buffer[-1][1] + 2*self.playback_direction
            except IndexError:
                # buffer empty; most probably end of file, read frame from self.capture
                # not always used as a none-empty buffer offsets the frame position from self.capure
                seek_target = self.capture.get(cv2.CAP_PROP_POS_FRAMES) + self.playback_direction
            self.seek_target = seek_target if seek_target >= 0 else 0
            self.frame_buffer.clear()

        self.frame_skip_factor = int(abs(speed)) if abs(speed) >= 1 else 1
        # used to skip frames so that playback framerate stays within one to two times source fps
        try:
            self.playback_frame_duration = int(1000 / (self.source_fps * abs(speed))) * self.frame_skip_factor
        except ZeroDivisionError:
            pass  # should only happen when no videofile is opened; no errorhandling required

    def release(self):
        """Releases the capture."""
        if self.capture:
            self.capture.release()
        self.capture = None  # set to None, so continous buffer thread terminates itself
