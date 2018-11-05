from videosource import VideoSource
from ui import Application
# from recognition import do_regocgnition

infile = 'C:/users/phisc/sonstige/test1.mp4'
uid = 'alo_q2'

videosource = VideoSource(infile)
# videosource = VideoSource('testfiles/test1.mp4')
outfile = 'results/ver_q3_ref.csv'

timing_data = [0, 0, 0]
selection = [81, 359, 42]

app = Application(videosource, timing_data, selection)

print("[INFO] starting...")
app.mainloop()

print(selection)

# do_regocgnition(videosource, timing_data, selection, outfile, uid)

videosource.release()  # release web camera
