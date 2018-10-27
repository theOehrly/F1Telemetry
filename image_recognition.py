from videosource import VideoSource
from ui import Application


videosource = VideoSource('testfiles/test1.mp4')

t_data = [0, 0, 0]

app = Application(videosource, t_data)

print("[INFO] starting...")
app.mainloop()

videosource.release()  # release web camera
