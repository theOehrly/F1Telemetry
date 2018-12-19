import cv2
import collections
import threading

# TODO reversing direction is not immediate
# TODO threaded videoloading results in the playbackbar beeing jittery


class VideoSource:
    def __init__(self, videofile):
        self.source_file = videofile
        self.capture = cv2.VideoCapture(self.source_file)  # video source

        self.frame_buffer = collections.deque()
        self.buffer_thread = None

        self.playback_direction = 1  # either 1 or -1
        self.frame_by_frame = False  # if true, frames are returned without delay
        self.seek_target = None
        self.reverse_once = False  # if set next_video_frame returns previous frame once

        self.source_fps = self.capture.get(cv2.CAP_PROP_FPS)  # video fps
        self.source_frame_duration = int(1000 / self.source_fps)  # duration of one frame
        self.playback_frame_duration = self.source_frame_duration  # can be different from source due to playbackspeed
        self.frame_skip_factor = 1  # 1=every frame, 2=every 2nd frame, ...

        self.total_frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = self.total_frames / self.source_fps  # video duration

        # prefill frame buffer
        while len(self.frame_buffer) < 1:
            self.top_up_buffer()

    def top_up_buffer(self):
        self.set_position()
        ok, frame = self.capture.read()
        if ok:
            self.frame_buffer.appendleft(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))

    def get_frame(self):
        if self.buffer_thread:
            self.buffer_thread.join()
        self.buffer_thread = threading.Thread(target=self.top_up_buffer)
        self.buffer_thread.start()
        # self.top_up_buffer()
        if self.frame_buffer:
            return self.frame_buffer.pop()

    def set_position(self):
        if self.seek_target:
            # set new position
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.seek_target)

            # clear buffer and refill as frames in it just got useless
            self.frame_buffer.clear()
            while len(self.frame_buffer) < 3:
                ok, frame = self.capture.read()
                if ok:
                    self.frame_buffer.appendleft(cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA))

            # reset seek target so we don't seek to it again
            self.seek_target = None

        if self.playback_direction == -1:
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

    def change_playback_speed(self, speed):
        if speed * self.playback_direction == -1:
            # one is negative and one positive, meaning new direction not equal to old direction
            self.frame_buffer.reverse()

        if speed > 0:
            self.playback_direction = 1
        elif speed < 0:
            self.playback_direction = -1

        self.frame_skip_factor = int(abs(speed)) if abs(speed) >= 1 else 1
        # used to skip frames so that playback framerate stays within one to two times source fps
        self.playback_frame_duration = int(1000 / (self.source_fps * abs(speed))) * self.frame_skip_factor

    def release(self):
        self.capture.release()
