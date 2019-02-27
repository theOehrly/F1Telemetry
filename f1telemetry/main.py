import sys
from PyQt5.Qt import QApplication
from f1telemetry.ui.qtmain import F1MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = F1MainWindow()
    app.exec()
