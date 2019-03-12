from PyQt5.QtWidgets import QFileDialog

from ui.customwidgets import StartRecognitionDialog
from ui.videorecognition_ui import VideoRecognitionUI


class VideoRecognition(VideoRecognitionUI):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.videofile = str()

        self.background_worker = None
        self.progress_dialog = None

    def init_ui(self):
        self.openBtn.clicked.connect(self.open_infile)
        self.runBtn.clicked.connect(self.run_recognition)

    def open_infile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Videofile", "", "Video files (*.*)")
        if filepath:
            self.videofile = filepath
            self.videoplayer.open_file(self.videofile)

    def run_recognition(self):
        dialog = StartRecognitionDialog(self)
        dialog.setWindowTitle("Run Recognition")
        dialog.show()
