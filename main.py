from videosource import VideoSource
from ui import Application
from recognition import do_regocgnition

infile = 'results/mex_q2/ver_alo_q2.mp4'
uid = 'alo_q2'

videosource = VideoSource(infile)
# videosource = VideoSource('testfiles/test1.mp4')
outfile = 'results/ver_q2_ref.csv'

timing_data = [0, 0, 0]

app = Application(videosource, timing_data)

print("[INFO] starting...")
app.mainloop()

do_regocgnition(videosource, timing_data, outfile, uid)

videosource.release()  # release web camera
