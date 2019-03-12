from PyQt5.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QLabel, QFrame)
from PyQt5.Qt import QIcon, QSizePolicy, QLayout, QFont
from PyQt5.QtCore import Qt

from ui.customwidgets import F1ToolBarButton

# some functions that create basic ui elements that are needed multiple times

FONT = QFont('Bahnschrift')


def create_toolbar_category(title, icons, texts, buttonsize=()):
    # creates a category widget with an arbitrary number of buttons

    # set up widget and layout
    category = QWidget()
    category.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    category.setStyleSheet('''QWidget {
                                background-color: #e8e8e9;
                                padding: 0px;
                                margin: 0px;
                                }''')

    categorylayout = QGridLayout(category)
    categorylayout.setSizeConstraint(QLayout.SetFixedSize)
    categorylayout.setSpacing(0)
    categorylayout.setContentsMargins(0, 0, 0, 0)

    # create all buttons and add them to the grid layout's first row
    columnindex = 0
    btns = list()
    for icon, text in zip(icons, texts):
        columnindex += 1
        btn = F1ToolBarButton()
        btn.setText(text)
        btn.setIcon(QIcon('./ui/images/' + icon))
        if buttonsize:
            btn.setButtonSize(buttonsize[columnindex - 1])
        categorylayout.addWidget(btn, 1, columnindex)
        btns.append(btn)

    # create all dividerlines and the name label
    dividerline = QFrame()  # horizontal line between buttons and label
    dividerline.setFixedHeight(1)
    dividerline.setLineWidth(1)
    dividerline.setFrameShape(QFrame.HLine)
    dividerline.setStyleSheet('''QFrame[frameShape="4"] {color: #2f3235;}''')  # frame shape 4 is HLine

    categoryname = QLabel()  # category title label
    categoryname.setText(title)
    categoryname.setAlignment(Qt.AlignCenter)
    categoryname.setFixedHeight(25)
    categoryname.setFont(FONT)
    categoryname.setStyleSheet('''QLabel {
                                            background-color: #9ea0a2;
                                            color: #2f3235;
                                            font: 11pt;}''')

    dividerline2 = QFrame()  # horizontal line below label
    dividerline2.setFixedHeight(1)
    dividerline2.setLineWidth(1)
    dividerline2.setFrameShape(QFrame.HLine)
    dividerline2.setStyleSheet('''QFrame[frameShape="4"] {color: #2f3235;}''')  # frame shape 4 is HLine

    shadow = QFrame()  # # horizontal shaddow line below label
    shadow.setFixedHeight(2)
    shadow.setLineWidth(2)
    shadow.setFrameShape(QFrame.HLine)
    shadow.setStyleSheet('''QFrame[frameShape="4"] {color: #5a5d60;}''')  # frameShape 4 is HLine

    # add lines and label to gridlayout (row, column, rowspan, columnspan)
    categorylayout.addWidget(dividerline, 2, 1, 1, columnindex)
    categorylayout.addWidget(categoryname, 3, 1, 1, columnindex)
    categorylayout.addWidget(dividerline2, 5, 1, 1, columnindex)
    categorylayout.addWidget(shadow, 6, 1, 1, columnindex)

    return category, btns


def create_toolbar_divider():
    # vertical category divider
    divider = QFrame()
    divider.setFixedWidth(1)
    divider.setLineWidth(1)
    divider.setFrameShape(QFrame.VLine)
    divider.setStyleSheet('''QFrame[frameShape="5"] {color: #77797c;}''')  # frame shape 5 is VLine
    return divider


def create_toolbar_spacer():
    toolbarspacer = QWidget()
    toolbarspacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    toolbarspacerlayout = QVBoxLayout(toolbarspacer)
    toolbarspacerlayout.setSpacing(0)
    toolbarspacerlayout.setContentsMargins(0, 0, 0, 0)

    # widget in place of buttons
    upper = QWidget()  # category title label
    upper.setFixedHeight(65)
    upper.setMinimumWidth(0)
    upper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    # create all dividerlines and the name label
    tbdividerline = QFrame()  # horizontal line between buttons and label
    tbdividerline.setFixedHeight(1)
    tbdividerline.setLineWidth(1)
    tbdividerline.setFrameShape(QFrame.HLine)
    tbdividerline.setStyleSheet('''QFrame[frameShape="4"] {color: #2f3235;}''')  # frame shape 4 is HLine

    # widget in place of category title
    lower = QWidget()  # category title label
    lower.setFixedHeight(25)
    lower.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    lower.setStyleSheet('''QWidget {background-color: #9ea0a2;}''')

    tbdividerline2 = QFrame()  # horizontal line below label
    tbdividerline2.setFixedHeight(1)
    tbdividerline2.setLineWidth(1)
    tbdividerline2.setFrameShape(QFrame.HLine)
    tbdividerline2.setStyleSheet('''QFrame[frameShape="4"] {color: #2f3235;}''')  # frame shape 4 is HLine

    shadow = QFrame()  # # horizontal shaddow line below label
    shadow.setFixedHeight(2)
    shadow.setLineWidth(2)
    shadow.setFrameShape(QFrame.HLine)
    shadow.setStyleSheet('''QFrame[frameShape="4"] {color: #5a5d60;}''')  # frameShape 4 is HLine

    toolbarspacerlayout.addWidget(upper)
    toolbarspacerlayout.addWidget(tbdividerline)
    toolbarspacerlayout.addWidget(lower)
    toolbarspacerlayout.addWidget(tbdividerline2)
    toolbarspacerlayout.addWidget(shadow)

    return toolbarspacer
