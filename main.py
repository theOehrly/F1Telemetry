from videosource import VideoSource
from recognition import do_regocgnition

infile = 'D:\\Dateien\\Projekte\\F1Telemetry\\Races\\2018\\Brasilien\\vettelq3.mp4'
uid = 'vet_q3'

videosource = VideoSource(infile)
# videosource = VideoSource('testfiles/test1.mp4')
outfile = 'D:\\Dateien\\Projekte\\F1Telemetry\\Races\\2018\\Brasilien\\vettelq3.csv'

timing_data = [0, 0, 0]
selection = [81, 359, 42]

print(selection)

# do_regocgnition(videosource, timing_data, selection, outfile, uid)

videosource.release()
