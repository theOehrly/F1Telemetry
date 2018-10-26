# base construction for this video player is tkaen from:
# http://answers.opencv.org/question/137744/python-opencv-tkinter-playing-video-help/
# as I have never worked with tkinter before


from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import cv2


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

        self.reverse_once = False  # if set next_frame returns previous frame once

    def next_frame(self):
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
            cv2.waitKey(self.frame_duration)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_frame = Image.fromarray(cv2image)  # convert image for PIL
            # self.current_image= self.current_image.resize([1280,1024],PIL.Image.ANTIALIAS)
            return self.current_frame

        else:
            return None

    def change_playback_speed(self, factor):
        if factor > 0:
            self.playback_direction = 1
        else:
            self.playback_direction = -1

        self.frame_duration = int(1000 / (self.source_fps * abs(factor)))

    def release(self):
        self.capture.release()


class Application(tk.Tk):
    def __init__(self, video_source):
        super(Application, self).__init__()
        self.video_source = video_source  # videosource class provides advanced playback options

        self.playing = True  # set player state

        self.title("F1 Video Telemetry ")  # set window title
        # self.destructor function gets fired when the window is closed
        self.protocol('WM_DELETE_WINDOW', self.destructor)
        self.panel = tk.Label(self)  # initialize image panel
        self.panel.pack(padx=10, pady=10, side=tk.TOP)
        self.config(cursor="arrow")

        # add playback progress bar with labels left/rigth
        self.top_row = tk.PanedWindow()
        self.top_row.pack(side=tk.TOP)
        self.label_time_code = tk.Label(text='0f/ 0s', padx=10, width=10)
        self.top_row.add(self.label_time_code)
        self.bar_playback = ttk.Progressbar(self.top_row, orient="horizontal", mode="determinate", length=1000)
        self.bar_playback['maximum'] = self.video_source.duration
        self.top_row.add(self.bar_playback)
        self.label_end_time = tk.Label(text=str(self.video_source.duration)+'s', padx=10, width=10)
        self.top_row.add(self.label_end_time)

        # add buttons for playback control
        # show previous frame
        self.btn_prev_frame = tk.Button(self, text="<", command=self.prev_frame, width=3, state=tk.DISABLED)
        self.btn_prev_frame.pack(padx=10, pady=10, side=tk.LEFT)
        # play/pause playback
        self.btn_pause = tk.Button(self, text="Play / Pause", command=self.playpause, width=10)
        self.btn_pause.pack(padx=0, pady=0, side=tk.LEFT)
        # show next frame
        self.btn_next_frame = tk.Button(self, text=">", command=self.next_frame, width=3, state=tk.DISABLED)
        self.btn_next_frame.pack(padx=10, pady=10, side=tk.LEFT)
        # set playback speed
        self.slider_speed = tk.Scale(self, command=self.change_playback_speed, orient='horizontal',
                                     from_=-5, to=5, resolution=0.1, length=300)
        self.slider_speed.set(1.0)  # set slider to 1.0
        self.slider_speed.pack(padx=10, pady=10, side=tk.LEFT)

        # start a self.video_loop that constantly updates the displayed image
        # for the most recently read frame
        self.video_loop()

    def video_loop(self):
        # get frame from videosource and show it with tkinter
        frame = self.video_source.next_frame()
        if frame:  # frame captured without any errors
            imgtk = ImageTk.PhotoImage(image=frame)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image

            # playback progress information
            time_code = self.video_source.capture.get(cv2.CAP_PROP_POS_MSEC) / 1000
            frame = int(self.video_source.capture.get(cv2.CAP_PROP_POS_FRAMES))
            self.label_time_code['text'] = str(frame) + ' / ' + "{0:.2f}".format(time_code) + 's'
            self.bar_playback['value'] = time_code

        if self.playing:
            self.after(1, self.video_loop)  # call the same function again

    def playpause(self):
        if self.playing:
            # set playback state
            self.playing = False
            self.enable_frame_by_frame()
        else:
            # set playback state
            self.playing = True
            # disable frame - by - frame buttons
            self.disable_frame_by_frame()
            self.after(1, self.video_loop)

    def change_playback_speed(self, factor):
        # changes playback speed; default playbackspeed is multiplied by "factor"
        # zero can't be used by video source and is rather used to pause video playback completely
        factor = float(factor)
        if factor == 0:
            self.playing = False  # stop playback
            self.video_source.playback_direction = 1
            self.enable_frame_by_frame()
        elif factor != 0 and not self.playing:
            self.video_source.change_playback_speed(factor)
            self.playing = True
            self.disable_frame_by_frame()
            # start playback
            self.after(1, self.video_loop)
        else:
            self.video_source.change_playback_speed(factor)

    def prev_frame(self):
        # set flag in video source telling it that the next requested frame will be previous one
        self.video_source.reverse_once = True
        # call videoloop without setting player state to playing so it will only run once
        self.after(1, self.video_loop)

    def next_frame(self):
        # call videoloop without setting player state to playing so it will only run once
        self.after(1, self.video_loop)

    def enable_frame_by_frame(self):
        # enable frame-by-frame buttons
        self.btn_prev_frame['state'] = tk.NORMAL
        self.btn_next_frame['state'] = tk.NORMAL

        self.video_source.frame_by_frame = False

    def disable_frame_by_frame(self):
        # disable frame - by - frame buttons
        self.btn_prev_frame['state'] = tk.DISABLED
        self.btn_next_frame['state'] = tk.DISABLED

        self.video_source.frame_by_frame = False

    def destructor(self):
        # destroy everything and exit
        print("[INFO] closing...")
        self.destroy()
        self.video_source.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application


# construct the argument parse and parse the arguments

# start the app
print("[INFO] starting...")
videosource = VideoSource('testfiles/test1.mp4')
app = Application(videosource)
app.mainloop()
