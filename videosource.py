import cv2
from PIL import Image


class VideoSource:
    def __init__(self, videofile):
        self.source_file = videofile
        self.capture = cv2.VideoCapture(self.source_file)  # video source

        self.current_frame = None
        self.playback_direction = 1  # either 1 or -1
        self.frame_by_frame = False  # if true, frames are returned without delay
        self.source_fps = self.capture.get(cv2.CAP_PROP_FPS)  # video fps
        self.frame_duration = int(1000 / self.source_fps)  # duration of one frame
        self.total_frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration = self.total_frames / self.source_fps  # video duration

        self.reverse_once = False  # if set next__video_frame returns previous frame once

    def next__video_frame(self):
        # returns next frame depending on playback direction
        if self.playback_direction == -1 or self.reverse_once:
            # return previous frame
            self.reverse_once = False  # reset always
            time_position_is = self.capture.get(cv2.CAP_PROP_POS_MSEC)
            if time_position_is >= 0:
                # set new timecode
                time_position_new = time_position_is - 2 * (1000 / self.source_fps)
                self.capture.set(cv2.CAP_PROP_POS_MSEC, time_position_new)
            else:
                return None

        ok, frame = self.capture.read()  # read frame from video stream
        # frame = cv2.resize(frame, (1500,1000))
        if ok:  # frame captured without any errors
            if not self.frame_by_frame:
                cv2.waitKey(self.frame_duration)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_frame = Image.fromarray(cv2image)  # convert image for PIL
            # self.current_image= self.current_image.resize([1280,1024],PIL.Image.ANTIALIAS)
            return self.current_frame

        else:
            return None

    def next_raw_frame(self):
        return self.capture.read()

    def seek_to(self, frame):
        time_position_new = frame * 1000 / self.source_fps
        self.capture.set(cv2.CAP_PROP_POS_MSEC, time_position_new)

    def change_playback_speed(self, factor):
        if factor > 0:
            self.playback_direction = 1
        elif factor < 0:
            self.playback_direction = -1

        self.frame_duration = int(1000 / (self.source_fps * abs(factor)))

    def release(self):
        self.capture.release()
