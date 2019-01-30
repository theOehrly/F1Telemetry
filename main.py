from PyQt5.Qt import QApplication
import sys

from videosource import VideoSource
from qtmainui import MainUI
from recognition import do_regocgnition
from datastruct import SelectionData

infile = 'testfiles\\hamilton monza 2018 first q3 lap 1.19.390.mp4'
uid = 'f1a_nsc'

outfile = 'testruns\\f1a_nsc.csv'

selection = SelectionData()
app = QApplication(sys.argv)
mainui = MainUI(selection, infile)
app.exec()
# selection.x = 164
# selection.y = 359
# selection.radius = 82
# selection.start_frame = 0
# selection.zero_frame = 0
# selection.end_frame = 2178

print(selection.x, selection.y, selection.radius)
print(selection.start_frame, selection.zero_frame, selection.end_frame)

videosource = VideoSource(infile)
do_regocgnition(videosource, selection, outfile, uid)
