from videosource import VideoSource
from ui import Application
from read_values import do_regocgnition


videosource = VideoSource('testfiles/test1.mp4')

timing_data = [0, 0, 0]

app = Application(videosource, timing_data)

print("[INFO] starting...")
app.mainloop()

do_regocgnition(videosource, timing_data)

videosource.release()  # release web camera
