import sys

from PyQt5.Qt import QApplication

from ui.qtmainui import MainUI

app = QApplication(sys.argv)
mainui = MainUI()
app.exec()
