from PyQt5.Qt import QThread, pyqtSignal
import recognition


# classes providing functionality for background operations


class OCRWorker(QThread):
    progressUpdate = pyqtSignal(int)
    finished = pyqtSignal()
    STOP = False

    def __init__(self, fname, outfile, uid, selection, new_font=False):
        super().__init__()

        self.filename = fname
        self.outfile = outfile
        self.uid = uid
        self.selection = selection
        self.new_font = new_font

    def run(self):
        recognition.recognize(self.filename, self.outfile, self.uid, self.selection, self.new_font, self)

    def update_progress(self, frame):
        self.progressUpdate.emit(frame)

    def set_finished(self):
        self.finished.emit()

    def quit(self):
        self.STOP = True
        super().quit()


class Regenerator(QThread):
    regenerationFinished = pyqtSignal()

    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def run(self):
        for element in self.elements:
            element.reprocessData()

        self.regenerationFinished.emit()


class DataProcessor(QThread):
    processingFinished = pyqtSignal()

    def __init__(self, treeelement, function, *options):
        super().__init__()

        self.treeelement = treeelement
        self.function = function
        self.options = options

    def run(self):
        xdata, ydata = self.treeelement.getPreviousData()

        new_xdata, new_ydata = self.function(xdata, ydata, *self.options)

        self.treeelement.xdata = new_xdata
        self.treeelement.ydata = new_ydata
        self.processingFinished.emit()