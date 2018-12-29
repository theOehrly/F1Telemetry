import cv2
import collections
import threading

# Video source class - the following actions are supported
#  - forward and reverse playback
#       (reverse playback is slow; this is an inherent issue of videodecoding)
#  - seeking to a specified frame
#  - change playback speed while playing
#       (at playback speeds above two times source fps this feature skips frames to be faster)
#  - frame by frame playback (forward and reverse) is supported through default get_frame method


class VideoSource:
    def __init__(self, videofile):
        self.source_file = videofile
        self.capture = cv2.VideoCapture(self.source_file)  # video source

        # some information about the source file; values are constants
        self.source_fps = self.capture.get(cv2.CAP_PROP_FPS)  # video fps
        self.source_frame_duration = int(1000 / self.source_fps)  # duration of one frame
        self.total_frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = self.total_frames / self.source_fps  # video duration

        # threaded frame loading into a buffer
        self.frame_buffer = collections.deque()
        # a deque with target length 1 used because of access from multiple threads
        # it ensures that even if when timing between threads is not as expected
        # no frames get skipped or lost, as the deque can increase length
        # the code supports longer buffer length but currently this leads to a slugish user
        # experience as most imortantly playback speed changes are not happening instantaneous then
        self.frame_buffer_length = 1
        self.buffer_reload_thread = None

        # playback controls
        self.playback_direction = 1  # either 1 (forward) or -1 (backward)
        self.seek_target = None  # target frame; gets set when seeking was requested
        self.frame_skip_factor = 1  # 1=every frame, 2=every 2nd frame, ... used for high playback speeds
        self.playback_frame_duration = self.source_frame_duration  # can be different from source due to playbackspeed
        # playback_frame_duration is used by the GUI to determine frame timing. It also changes depending on
        # frame skipping therefore it is calculated by the videosource

        self.preload_framebuffer()

    def top_up_buffer(self):
        self.set_position()
        frame_pos = self.capture.get(cv2.CAP_PROP_POS_FRAMES)
        ok, frame = self.capture.read()
        if ok:
            # convert to rgb for PyQt
            self.frame_buffer.appendleft((cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                                          frame_pos, self.playback_frame_duration))
        else:
            return None

    def preload_framebuffer(self):
        while len(self.frame_buffer) < self.frame_buffer_length:
            self.top_up_buffer()

    def get_frame(self):
        if self.buffer_reload_thread:
            self.buffer_reload_thread.join()
        self.buffer_reload_thread = threading.Thread(target=self.top_up_buffer)
        self.buffer_reload_thread.start()
        # self.top_up_buffer()
        if self.frame_buffer:
            return self.frame_buffer.pop()

    def set_position(self):
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
            frame_position_is = self.capture.get(cv2.CAP_PROP_POS_FRAMES)
            frame_position_new = frame_position_is + (self.frame_skip_factor - 1)

            if frame_position_new <= self.total_frames:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_position_new)

    def next_raw_frame(self):
        return self.capture.read()

    def seek_to(self, frame):
        # self.seek_target = frame * 1000 / self.source_fps
        self.seek_target = frame

    def set_playback_speed(self, speed):
        dir_old_new = speed * self.playback_direction

        if speed > 0:
            self.playback_direction = 1
        elif speed < 0:
            self.playback_direction = -1

        if dir_old_new < 0:
            # one is negative and one positive, meaning new direction not equal to old direction
            try:
                seek_target = self.frame_buffer[-1][1] + 2*self.playback_direction
            except IndexError:
                # buffer empty; most probably end of file, read frame from self.capture
                # not always used as a none-empty buffer offsets the frame position from self.capure
                seek_target = self.capture.get(cv2.CAP_PROP_POS_FRAMES) + 2 * self.playback_direction
            self.seek_target = seek_target if seek_target >=0 else 0
            self.frame_buffer.clear()
            self.preload_framebuffer()

        self.frame_skip_factor = int(abs(speed)) if abs(speed) >= 1 else 1
        # used to skip frames so that playback framerate stays within one to two times source fps
        self.playback_frame_duration = int(1000 / (self.source_fps * abs(speed))) * self.frame_skip_factor

    def release(self):
        self.capture.release()
