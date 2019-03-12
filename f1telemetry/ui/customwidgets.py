from pyqtgraph import PlotWidget
from PyQt5.Qt import QSize, QFont, QIcon, QFontMetrics
from PyQt5.QtWidgets import (QToolButton, QCheckBox, QSizePolicy, QSpacerItem, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QDialog, QFormLayout, QLineEdit, QFileDialog, QProgressDialog)
from PyQt5.QtCore import Qt, pyqtSignal

from backgroundtasks import OCRWorker


# custom widgets: themed and/or providing some custom functionality

FONT = QFont('Bahnschrift')


class F1PlotWidget(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseReleaseEvent(self, _event):
        # suppress right clicks
        if _event.button() == Qt.RightButton:
            _event.accept()
        else:
            super().mouseReleaseEvent(_event)


class F1ClickableHeader(QWidget):
    """A Widget that provides the clicked signal. Used as Header for TreeItems."""
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, _event):
        self.clicked.emit()


class F1TreeItem(QWidget):
    """A widget consisting of a header with title and some variable content.
    Clicking on the header shows/hides the content. The header also provides remove/supress buttons."""

    def __init__(self):
        super(QWidget, self).__init__()

        # general layout settings
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # clickable header + styling
        self.header = F1ClickableHeader()
        self.header.clicked.connect(self.toggleContentView)
        self.header.setAttribute(Qt.WA_StyledBackground, True)
        self.header.setStyleSheet('''QWidget {background-color: rgba(55, 58, 62, 100);
                                                padding: 0px;
                                                margin: 0px;}''')
        self.header.setFixedHeight(30)
        self.layout.addWidget(self.header)

        # header layout: add label for title and control buttons
        self.headerLayout = QHBoxLayout(self.header)
        self.headerLayout.setContentsMargins(10, 0, 0, 0)
        self.headerLayout.setSpacing(0)
        self.titleLbl = QLabel()
        self.titleLbl.setFont(FONT)
        self.titleLbl.setStyleSheet('''QLabel {background: transparent;
                                                font: 10pt;
                                                color: #373a3e;}''')
        self.headerLayout.addWidget(self.titleLbl)
        self.headerLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.supressInd = F1SupressItemIndicator()  # styled checkbox
        self.supressInd.setChecked(True)
        self.headerLayout.addWidget(self.supressInd)
        self.removeBtn = QPushButton()
        self.removeBtn.setFixedSize(30, 30)
        self.removeBtn.setStyleSheet('''QPushButton {background: transparent;}''')
        self.removeBtn.setIcon(QIcon('./ui/images/close.png'))
        self.removeBtn.setIconSize(QSize(16, 16))
        self.headerLayout.addWidget(self.removeBtn)

        self.content = None  # content is a QWidget; added by calling setWidget(widget)

    def setTitle(self, text):
        """Set header title.
        setTitle(string)"""

        self.titleLbl.setText(text)

    def setDeleteable(self, _bool):
        """Sets whether this item can be deleted/supressed by user.
        If set to False, the Remove and Supress Button are hidden.
        setDeletable(bool)"""

        pass

    def setWidget(self, widget):
        """Set Widget as content.
        setWidget(widget)"""

        self.content = widget
        self.content.setAttribute(Qt.WA_StyledBackground, True)
        self.content.setStyleSheet('''QWidget {background-color: rgba(109, 179, 249, 100);
                                            padding: 0px;
                                            margin: 0px;}''')
        self.layout.addWidget(self.content)

    def toggleContentView(self):
        """Change whether content is visible or not.
        Every call switches from the current the opposite one.
        The function is indifferent to the current state."""

        if self.content.isVisible():
            self.content.hide()
        else:
            self.content.show()


class F1Tree(QWidget):
    """This Widget is a container for TreeItems.
    Items can be added and removed. They are displayed in a list vertically stacked.
    A new item is added at the bottom by default."""

    def __init__(self):
        super(QWidget, self).__init__()

        self.tree_items = list()

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('''QWidget {background: transparent;
                                                padding: 0px;
                                                margin: 0px;}''')

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 5, 0, 0)
        self.setLayout(self.layout)

        # spacer height needs to be set to some very heigh number to get the intended behaviout in scrollview
        self.layout.addItem(QSpacerItem(0, 10000, QSizePolicy.Preferred, QSizePolicy.Preferred))

    def addItem(self, content, title):
        """Creates and adds a new TreeItem with the provided content and title.
        addItem(content, title)"""

        widget = F1TreeItem()
        widget.setWidget(content)
        widget.setTitle(title)
        self.tree_items.append(widget)
        self.layout.insertWidget(len(self.tree_items)-1, widget, Qt.AlignCenter, Qt.AlignTop)
        # widget is inserted instead of simply added as the spacer is always the last element in the layout

    def removeIndex(self, index):
        """Removes the item at the given list position.
        removeItem(index)"""

        widget = self.tree_items.pop(index)
        self.layout.removeWidget(widget)

    def removeAll(self):
        """Removes all items.
        removeAll()"""

        while self.tree_items:
            widget = self.tree_items.pop(0)
            self.layout.removeWidget(widget)


class F1ToolBarButton(QToolButton):
    """A styled QToolButton with the ToolButtonTextUnderIcon style property set.
    Use default QToolButton.setText and setIcon"""
    def __init__(self):
        super().__init__()

        self.setStyleSheet('''QToolButton{
                                    background: None;
                                    color: #373a3e;
                                    border: None;
                                    font: 9pt;
                                    margin: 0px;
                                    padding: 0px;
                                }
                                QToolButton:pressed {
                                    border: 2px solid #3c9af7;
                                }
                                QToolButton:hover {
                                    background-color: #c5c6c7;
                                }
                                ''')
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.setFont(FONT)

        self.setIconSize(QSize(60, 40))
        self.setFixedSize(60, 65)

    def setButtonSize(self, width):
        """Sets the Button size.
        Height is constant. For width changes: Keywords 'single' (60px), 'double' (120px) or 'double+menu' (140px).
        setButtonSize(keyword)"""

        if width == 'single':
            self.setIconSize(QSize(60, 40))
            self.setFixedSize(60, 65)
        elif width == 'double':
            self.setIconSize(QSize(120, 40))
            self.setFixedSize(120, 65)
        elif width == 'double+menu':
            self.setIconSize(QSize(120, 40))
            self.setFixedSize(140, 65)


class F1SupressItemIndicator(QCheckBox):
    """A Styled QCheckBox."""

    def __init__(self):
        super().__init__()

        self.setStyleSheet('''QCheckBox {
                                spacing: 5px;
                                font: 10pt;
                                color: #373a3e;
                                background: transparent;
                            }

                            QCheckBox::indicator {
                                width: 20px;
                                height: 20px;
                            }

                            QCheckBox::indicator:unchecked {
                                image: url(./ui/images/indicator_supressed.png);
                            }

                            QCheckBox::indicator:unchecked:hover {
                                image: url(./ui/images/indicator_supressed_hover.png);
                            }

                            QCheckBox::indicator:unchecked:pressed {
                                image: url(./ui/images/indicator_pressed.png);
                            }

                            QCheckBox::indicator:checked {
                                image: url(./ui/images/indicator_active.png);
                            }

                            QCheckBox::indicator:checked:hover {
                                image: url(./ui/images/indicator_active_hover.png);
                            }

                            QCheckBox::indicator:checked:pressed {
                                image: url(./ui/images/indicator_pressed.png);
                            }
                           ''')


class F1CheckBox(QCheckBox):
    """Custom styled QCheckBox."""
    def __init__(self):
        super().__init__()

        self.setStyleSheet('''QCheckBox {
                                spacing: 5px;
                                font: 10pt;
                                color: #373a3e;
                                border: None;
                            }
                            
                            QCheckBox::indicator {
                                width: 20px;
                                height: 20px;
                            }
                            
                            QCheckBox::indicator:unchecked {
                                image: url(./ui/images/checkbox_unchecked.png);
                            }
                            
                            QCheckBox::indicator:unchecked:hover {
                                image: url(./ui/images/checkbox_unchecked_hover.png);
                            }
                            
                            QCheckBox::indicator:unchecked:pressed {
                                image: url(./ui/images/checkbox_pressed.png);
                            }
                            
                            QCheckBox::indicator:checked {
                                image: url(./ui/images/checkbox_checked.png);
                            }
                            
                            QCheckBox::indicator:checked:hover {
                                image: url(./ui/images/checkbox_checked_hover.png);
                            }
                            
                            QCheckBox::indicator:checked:pressed {
                                image: url(./ui/images/checkbox_pressed.png);
                            }
                           ''')
        self.setFont(FONT)


class F1PushButton(QPushButton):
    """Styled version of QPushButton."""

    def __init__(self):
        super(QPushButton, self).__init__()

        self.setStyleSheet("""QPushButton{
                                    background: None;
                                    color: #373a3e;
                                    background-color: #c5c6c7;
                                    border: 1px solid #77797c; /**/
                                    font: 9pt;
                                    margin: 0px;
                                    padding: 0px;
                                }
                                QPushButton:pressed {
                                    border: 2px solid #3c9af7;
                                }
                                QPushButton:hover {
                                    background-color: #9ea0a2;
                                }""")


class F1LineEdit(QLineEdit):
    """Styled QTextEdit."""
    def __init__(self):
        super(QLineEdit, self).__init__()

        self.setFont(FONT)
        self.setStyleSheet("""QLineEdit {
                                border: 1px solid #77797c;
                                }""")


class LeftElidingLabel(QLabel):
    def __init__(self):
        super(QLabel, self).__init__()
        self.full_str = str()

    def setText(self, p_str):
        self.full_str = p_str
        self.setTextElided(p_str)

    def setTextElided(self, p_str):
        qfm = QFontMetrics(FONT)
        elided_str = qfm.elidedText(p_str, Qt.ElideLeft, self.width())
        super().setText(elided_str)

    def resizeEvent(self, *args, **kwargs):
        self.setTextElided(self.full_str)
        super().resizeEvent(*args, **kwargs)


class StartRecognitionDialog(QDialog):
    """Styled QDialog."""
    def __init__(self, parent):
        # create super dialog with title and close button BUT WITHOUT "What's this" button
        super(QDialog, self).__init__(parent, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.parent = parent
        self.worker = None
        self.progress_dialog = None

        self.setModal(True)

        self.output_folder_path = None

        self.layout = QFormLayout(self)
        self.layout.setHorizontalSpacing(40)

        outputfolderlabel = QLabel()
        outputfolderlabel.setText('Output Folder')
        outputfolderlabel.setStyleSheet("""QLabel {font: bold;
                                                    color: #373a3e;}""")
        self.outputFolderPathLbl = LeftElidingLabel()
        self.outputFolderPathLbl.setMinimumWidth(250)
        self.outputFolderPathLbl.setFont(FONT)
        self.outputFolderPathLbl.setStyleSheet("""QLabel {font: 10pt;}""")
        self.outputFolderBtn = F1PushButton()
        # self.outputFolderBtn.setText('...')
        self.outputFolderBtn.setIcon(QIcon('./ui/images/open.png'))
        self.outputFolderBtn.setIconSize(QSize(30, 30))
        self.outputFolderBtn.setFixedSize(30, 30)
        self.outputFolderBtn.clicked.connect(self.getOutputFolder)
        outputfolderlayout = QHBoxLayout()
        outputfolderlayout.setSpacing(10)
        outputfolderlayout.addWidget(self.outputFolderPathLbl)
        outputfolderlayout.addWidget(self.outputFolderBtn)
        self.layout.addRow(outputfolderlabel, outputfolderlayout)

        uidlabel = QLabel()
        uidlabel.setText('Unique ID')
        uidlabel.setStyleSheet("""QLabel {font: bold;
                                            color: #373a3e;}""")

        uidlabel.setToolTip('A unique identifier for the dataset')
        self.uidLineEdit = F1LineEdit()
        self.uidLineEdit.setStyleSheet(self.uidLineEdit.styleSheet() + """QLineEdit {font: 10pt;}""")
        self.uidLineEdit.setFixedHeight(25)
        self.layout.addRow(uidlabel, self.uidLineEdit)

        self.runBtn = F1PushButton()
        self.runBtn.setIcon(QIcon('./ui/images/runrecognition.png'))
        self.runBtn.setIconSize(QSize(45, 30))
        self.runBtn.setFixedSize(40, 40)
        self.runBtn.clicked.connect(self.run)
        self.cancelBtn = F1PushButton()
        self.cancelBtn.setIcon(QIcon('./ui/images/close_large.png'))
        self.cancelBtn.setIconSize(QSize(20, 20))
        self.cancelBtn.setFixedSize(40, 40)
        self.cancelBtn.clicked.connect(self.close)

        spacerwidget = QWidget(self)
        spacerwidget.setFixedHeight(20)
        self.layout.addRow(None, spacerwidget)

        controllayout = QHBoxLayout()
        controllayout.setSpacing(10)
        self.errorLbl = QLabel()
        self.errorLbl.setStyleSheet("""QLabel {color: red;}""")
        controllayout.addWidget(self.errorLbl)
        controllayout.addWidget(self.cancelBtn)
        controllayout.addWidget(self.runBtn)
        self.layout.addRow("", controllayout)

    def getOutputFolder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder", "", QFileDialog.ShowDirsOnly)
        if path:
            self.output_folder_path = str(path)
            self.outputFolderPathLbl.setText(self.output_folder_path)
            self.outputFolderPathLbl.setToolTip(self.output_folder_path)

    def run(self):
        if not self.output_folder_path:
            self.errorLbl.setText("Missing Parameter: Output Folder")
            return
        uid = self.uidLineEdit.text()
        if not uid:
            self.errorLbl.setText("Missing Parameter: Unique ID")
            return

        # show progress bar
        n_frames = self.parent.videoplayer.selection.end_frame - self.parent.videoplayer.selection.start_frame
        self.progress_dialog = QProgressDialog('Processing Frames...', 'Cancel', 0, n_frames, self)
        self.progress_dialog.setMinimumWidth(400)
        self.progress_dialog.setWindowTitle('OCR Running')
        self.progress_dialog.canceled.connect(self.cancel_ocr)
        self.progress_dialog.show()

        # run ocr in seperate QThread
        outfile = self.output_folder_path + '/' + uid + '.csv'
        self.worker = OCRWorker(self.parent.videofile, outfile, uid, self.parent.videoplayer.selection)
        self.worker.progressUpdate.connect(self.update_ocr_progress)
        self.worker.finished.connect(self.update_ocr_finished)
        self.worker.start()

    def update_ocr_progress(self, value):
        self.progress_dialog.setValue(value)

    def update_ocr_finished(self):
        self.progress_dialog.reset()
        self.progress_dialog = None
        self.close()

    def cancel_ocr(self):
        self.worker.quit()
        self.worker.wait()
