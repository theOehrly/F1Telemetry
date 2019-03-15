from PyQt5.QtWidgets import QWidget, QFormLayout, QGridLayout, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QLabel
from PyQt5.Qt import QFont
from ui.customwidgets import LeftElidingLabel, F1CheckBox


FONT = QFont('Bahnschrift')


class BaseWidgetUI(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QFormLayout(self)

        self.fileNameLabel = LeftElidingLabel()
        self.fileNameLabel.setStyleSheet("""QLabel {background: None;
                                                    font: 9pt;}""")
        self.fileNameLabel.setFont(FONT)
        row1lbl = QLabel("File")
        row1lbl.setStyleSheet("""QLabel {background: None;}""")
        self.layout.addRow(row1lbl, self.fileNameLabel)

        self.datasetDropdown = QComboBox()
        self.datasetDropdown.setFont(FONT)
        self.datasetDropdown.setStyleSheet("""QComboBox {border: 1px solid #2f3235;
                                                            background-color: rgba(255, 255, 255, 125);
                                                            font: 9pt;}
                                            /*QComboBox::down-arrow { */
                                            /*image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);} */
                                            """)
        row2lbl = QLabel("Dataset")
        row2lbl.setStyleSheet("""QLabel {background: None;}""")
        self.layout.addRow(row2lbl, self.datasetDropdown)


class SpikesByChangeWidgetUI(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QGridLayout(self)
        self.layout.setColumnStretch(3, 1)  # set stretch factor for third column --> only column 3 expands

        infolbl = QLabel("Maximum Rate of Change")
        infolbl.setStyleSheet("""QLabel {background: None;
                                            font: bold;}""")
        self.layout.addWidget(infolbl, 1, 1, 1, 3)

        poslbl = QLabel("Pos")
        poslbl.setStyleSheet("""QLabel {background: None;}""")
        self.layout.addWidget(poslbl, 2, 1)

        neglbl = QLabel("Neg")
        neglbl.setStyleSheet("""QLabel {background: None;}""")
        self.layout.addWidget(neglbl, 3, 1)

        self.ratePosBox = QSpinBox()
        self.ratePosBox.setMaximum(9999)
        self.ratePosBox.setMinimum(0)
        self.ratePosBox.setProperty("value", 300)
        self.ratePosBox.setStyleSheet("""QSpinBox {background: None;}""")
        self.layout.addWidget(self.ratePosBox, 2, 2)

        self.rateNegBox = QSpinBox()
        self.rateNegBox.setMaximum(0)
        self.rateNegBox.setMinimum(-9999)
        self.rateNegBox.setProperty("value", -300)
        self.rateNegBox.setStyleSheet("""QSpinBox {background: None;}""")
        self.layout.addWidget(self.rateNegBox, 3, 2)

        unitinfolbl = QLabel("[km/h per sec]")
        unitinfolbl.setStyleSheet("""QLabel {background: None;}""")
        self.layout.addWidget(unitinfolbl, 2, 3, 2, 1)


class SmoothingSavgolWidgetUI(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = QVBoxLayout(self)

        self.splitCheckBox = F1CheckBox()
        self.splitCheckBox.setText("Split Acceleration/Breaking")
        self.layout.addWidget(self.splitCheckBox)

        splitsettingslayout = QHBoxLayout()
        self.layout.addLayout(splitsettingslayout)

        splittsettingslbl = QLabel("Minimum Deceleration Rate [km/h per sec]")
        splittsettingslbl.setStyleSheet("""QLabel {background: None;}""")
        self.minNegRateBox = QSpinBox()
        self.minNegRateBox.setMaximum(0)
        self.minNegRateBox.setMinimum(-9999)
        self.minNegRateBox.setProperty("value", 5)
        self.minNegRateBox.setStyleSheet("""QSpinBox {background: None;}""")

        splitsettingslayout.addWidget(splittsettingslbl)
        splitsettingslayout.addWidget(self.minNegRateBox)







