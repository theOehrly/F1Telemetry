# base construction for this video player is tkaen from:
# http://answers.opencv.org/question/137744/python-opencv-tkinter-playing-video-help/
# as I have never worked with tkinter before


from PIL import Image, ImageTk
import tkinter as tk
import cv2


class Application(tk.Tk):
    def __init__(self, video_source, timing_data):
        super(Application, self).__init__()

        self.video_source = video_source  # videosource class provides advanced playback options
        self.playing = True  # set player state

        self.timing_data = timing_data
        self.timing_data[2] = self.video_source.total_frames  # set end time to total frames for now

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
        self.slider_playback = tk.Scale(self, orient='horizontal', from_=0, to=self.video_source.total_frames,
                                        resolution=1, length=1000, showvalue=False)
        self.top_row.add(self.slider_playback)
        self.slider_playback.bind('<B1-Motion>', self.seek_to)  # call when slider is beeing dragged
        self.slider_playback.bind('<ButtonRelease-1>', self.end_seek)  # resume playback when slider released
        self.label_duration = tk.Label(text=str(self.video_source.duration)+'s', padx=10, width=10)
        self.top_row.add(self.label_duration)

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

        # explanation of following three timing control buttons:
        # image recognition later will be done from start time to end time
        # timing will be referenced to zero position, meaning start time is not necessarily zero in data
        # add button/label for selecting end time
        self.label_end_time = tk.Label(self, padx=10, width=10, text='{}f / {}s'.format(round(self.timing_data[2]),
                                                                                        self.video_source.total_frames))
        self.label_end_time.pack(side=tk.RIGHT)
        self.btn_end_time = tk.Button(self, text='Mark End', padx=10, width=10, state=tk.DISABLED,
                                      command=self.set_end_time)
        self.btn_end_time.pack(side=tk.RIGHT)
        # add button/label for selecting zero time position
        self.label_zero_time = tk.Label(self, padx=10, width=10, text='0f / 0s')
        self.label_zero_time.pack(side=tk.RIGHT)
        self.btn_zero_time = tk.Button(self, text='Mark Zero', padx=10, width=10, state=tk.DISABLED,
                                       command=self.set_zero_time)
        self.btn_zero_time.pack(side=tk.RIGHT)
        # add button/label for selecting start time
        self.label_start_time = tk.Label(self, padx=10, width=10, text='0f / 0s')
        self.label_start_time.pack(side=tk.RIGHT)
        self.btn_start_time = tk.Button(self, text='Mark Start', padx=10, width=10, state=tk.DISABLED,
                                        command=self.set_start_time)
        self.btn_start_time.pack(side=tk.RIGHT)

        # start a self.video_loop that constantly updates the displayed image
        # for the most recently read frame
        self.video_loop()

    def video_loop(self):
        # get frame from videosource and show it with tkinter
        frame = self.video_source.next_video_frame()
        if frame:  # frame captured without any errors
            imgtk = ImageTk.PhotoImage(image=frame)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image

            # playback progress information
            time_code = self.video_source.capture.get(cv2.CAP_PROP_POS_MSEC) / 1000
            frame = int(self.video_source.capture.get(cv2.CAP_PROP_POS_FRAMES))
            self.label_time_code['text'] = str(frame) + ' / ' + "{0:.2f}".format(time_code) + 's'
            self.slider_playback.set(frame)

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
            self.playing = True
            self.disable_frame_by_frame()
            self.video_source.change_playback_speed(factor)
            # start playback
            self.after(1, self.video_loop)
        else:
            self.video_source.change_playback_speed(factor)

    def seek_to(self, event):
        self.playing = False
        self.enable_frame_by_frame()
        # self.after(1, self.continue_seek)
        # self.video_source.no_delay = True  # deliver frames without delay when seeking

        frame = self.slider_playback.get()
        self.video_source.seek_to(frame-1)
        self.video_loop()

    def end_seek(self, event):
        self.disable_frame_by_frame()

        self.playing = True
        self.after(1, self.video_loop)

    def prev_frame(self):
        # set flag in video source telling it that the next requested frame will be previous one
        self.video_source.playback_direction = -1
        # call videoloop without setting player state to playing so it will only run once
        self.after(1, self.video_loop)

    def next_frame(self):
        # call videoloop without setting player state to playing so it will only run once
        self.video_source.playback_direction = 1
        self.after(1, self.video_loop)

    def enable_frame_by_frame(self):
        # enable frame-by-frame buttons and timing control buttons
        self.btn_prev_frame['state'] = tk.NORMAL
        self.btn_next_frame['state'] = tk.NORMAL
        self.btn_start_time['state'] = tk.NORMAL
        self.btn_end_time['state'] = tk.NORMAL
        self.btn_zero_time['state'] = tk.NORMAL

        self.video_source.frame_by_frame = False

    def disable_frame_by_frame(self):
        # disable frame-by-frame and timing control buttons
        self.btn_prev_frame['state'] = tk.DISABLED
        self.btn_next_frame['state'] = tk.DISABLED
        self.btn_start_time['state'] = tk.DISABLED
        self.btn_end_time['state'] = tk.DISABLED
        self.btn_zero_time['state'] = tk.DISABLED

        self.video_source.frame_by_frame = False
        self.video_source.playback_direction = self.slider_speed.get()

    def set_start_time(self):
        # set start time for image recognition
        current_frame = self.video_source.capture.get(cv2.CAP_PROP_POS_FRAMES)
        self.timing_data[1] = current_frame
        self.label_start_time['text'] = '{}f / {}s'.format(current_frame,
                                                           current_frame * self.video_source.frame_duration / 1000)

    def set_end_time(self):
        # set end time for video recognition
        current_frame = self.video_source.capture.get(cv2.CAP_PROP_POS_FRAMES)
        self.timing_data[2] = current_frame
        self.label_end_time['text'] = '{}f / {}s'.format(current_frame,
                                                         current_frame * self.video_source.frame_duration / 1000)

    def set_zero_time(self):
        # set zero time for video recognition
        current_frame = self.video_source.capture.get(cv2.CAP_PROP_POS_FRAMES)
        self.timing_data[0] = current_frame
        self.label_zero_time['text'] = '{}f / {}s'.format(current_frame,
                                                          current_frame * self.video_source.frame_duration / 1000)

    def destructor(self):
        # destroy everything and exit
        print("[INFO] closing...")
        self.destroy()
