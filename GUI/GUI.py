import sys
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QAction, QMessageBox, QRadioButton, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from ..id3.Container import Container
from id3.Container import create_subset
from id3.Tree import learn
from collections import Counter
from c45.c45 import *

labels = {'tennis.data': ["weather", "temp", "wind", "other", "play"],
          'ca.data': ["buying", "maint", "doors", "persons", "lug_boot", "safety", "output"]}


def load_recent_files():
    ll = []
    with open("recents.dcr", "r") as fle:
        for line in fle.readlines():
            ll.append(line.strip("\n"))
        return ll


def save_recents(pwd):
    with open("recents.dcr", "a") as fle:
        fle.write(str(pwd) + "\n")


class window(QMainWindow):
    """
        Class implementing a window for the awesome proejct we have
    """

    def __init__(self):
        """
        Constructor
        """
        super(window, self).__init__()
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.constants()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.show()

    def constants(self):
        """
        Definition of border constants
        :return: 
        """
        self.qline_size = 12
        self.btn_text_size = 14
        self.label_text_size = 15
        self.radiobtn_text_size = 15

    def setup_labels(self, gridLayoutWidget, gridLayout):
        """
        Create labels for window
        :param gridLayoutWidget: 
        :param gridLayout: 
        :return: 
        """
        font = QtGui.QFont()
        font.setPointSize(self.label_text_size)
        font.setBold(True)

        label = QtWidgets.QLabel("File", gridLayoutWidget)
        label.setFont(font)
        gridLayout.addWidget(label, 0, 0, 1, 1)
        label = QtWidgets.QLabel("Algo", gridLayoutWidget)
        label.setFont(font)
        gridLayout.addWidget(label, 1, 0, 1, 1)
        label = QtWidgets.QLabel("Prune", gridLayoutWidget)
        label.setFont(font)
        gridLayout.addWidget(label, 3, 0, 1, 1)
        label = QtWidgets.QLabel("Prediction  ", gridLayoutWidget)
        label.setFont(font)
        gridLayout.addWidget(label, 4, 0, 1, 1)
        label = QtWidgets.QLabel("Output", gridLayoutWidget)
        label.setFont(font)
        gridLayout.addWidget(label, 5, 0, 1, 1)

    def setup_buttons(self, gridLayoutWidget, grid_layout):
        font = QtGui.QFont()
        font.setPointSize(self.btn_text_size)
        font_important = QtGui.QFont()
        font_important.setPointSize(self.btn_text_size)
        font_important.setBold(True)

        push_button = QtWidgets.QPushButton("Open", self.grid_layout_widget)
        push_button.setFont(font)
        push_button.clicked.connect(self.set_file_name)
        grid_layout.addWidget(push_button, 0, 4, 1, 1)
        push_button = QtWidgets.QPushButton("Learn", self.grid_layout_widget)
        push_button.setFont(font_important)
        push_button.clicked.connect(self.set_learn)
        grid_layout.addWidget(push_button, 1, 4, 1, 1)
        self.predictButton = QtWidgets.QPushButton("Predict", self.grid_layout_widget)
        self.predictButton.setFont(font_important)
        self.predictButton.setEnabled(False)
        self.predictButton.clicked.connect(self.set_predict)
        grid_layout.addWidget(self.predictButton, 4, 4, 1, 1)
        pushButton = QtWidgets.QPushButton("Erase", self.grid_layout_widget)
        pushButton.setFont(font)
        pushButton.clicked.connect(self.set_erase)
        grid_layout.addWidget(pushButton, 5, 4, 1, 1)

    def setup_radio_buttons(self, gridLayoutWidget, gridLayout):
        font = QtGui.QFont()
        font.setPointSize(self.radiobtn_text_size)

        horizontal_layout = QtWidgets.QHBoxLayout()

        self.radio_Button_ID3 = QtWidgets.QRadioButton("ID3", gridLayoutWidget)
        self.radio_Button_ID3.setFont(font)
        self.radio_Button_ID3.setChecked(True)

        horizontal_layout.addWidget(self.radio_Button_ID3)

        self.radio_button_C45 = QtWidgets.QRadioButton("C4.5", self.grid_layout_widget)
        self.radio_button_C45.setFont(font)
        self.radio_button_C45.setChecked(False)
        self.radio_button_C45.toggled.connect(lambda: self.change_prune_State(self.radio_button_C45))

        horizontal_layout.addWidget(self.radio_button_C45)

        gridLayout.addLayout(horizontal_layout, 1, 3, 1, 1)

    def setupQLine(self, gridLayoutWidget, gridLayout):

        self.file_label = QtWidgets.QLineEdit(gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(self.qline_size)
        self.file_label.setFont(font)
        gridLayout.addWidget(self.file_label, 0, 3, 1, 1)

        # self.pruneLabel = QtWidgets.QLineEdit(gridLayoutWidget)
        # self.pruneLabel.setEnabled(False)
        # font = QtGui.QFont()
        # font.setPointSize(self.qline_size)
        # self.pruneLabel.setFont(font)
        # gridLayout.addWidget(self.pruneLabel, 3, 3, 1, 1)

        self.lcdNumber = QtWidgets.QLCDNumber(gridLayoutWidget)
        self.lcdNumber.setEnabled(False)
        self.lcdNumber.display(0.0)
        self.lcdNumber.setFixedWidth(80)
        self.lcdNumber.setFixedHeight(30)
        gridLayout.addWidget(self.lcdNumber, 3, 4, 1, 1)

        self.horizontalScrollBar = QtWidgets.QScrollBar(gridLayoutWidget)
        self.horizontalScrollBar.setEnabled(False)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.sliderMoved.connect(self.on_slider_move)
        self.horizontalScrollBar.setFixedHeight(20)
        gridLayout.addWidget(self.horizontalScrollBar, 3, 3, 1, 1)

        self.predictionLabel = QtWidgets.QLineEdit(gridLayoutWidget)
        self.predictionLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(self.qline_size)
        self.predictionLabel.setFont(font)
        gridLayout.addWidget(self.predictionLabel, 4, 3, 1, 1)

    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Techniques of Artificial Intelligence")
        MainWindow.resize(600, 300)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QColor("#fff7d1"))
        self.setPalette(palette)

        self.central_widget = QtWidgets.QWidget(MainWindow)

        self.grid_layout_widget = QtWidgets.QWidget(self.central_widget)
        self.grid_layout_widget.setGeometry(QtCore.QRect(26, 10, 530, 280))

        self.grid_layout = QtWidgets.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.grid_layout.setContentsMargins(5, 0, 0, 0)
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setVerticalSpacing(10)

        self.setup_labels(self.grid_layout_widget, self.grid_layout)
        self.setup_buttons(self.grid_layout_widget, self.grid_layout)
        self.setup_radio_buttons(self.grid_layout_widget, self.grid_layout)
        self.setupQLine(self.grid_layout_widget, self.grid_layout)

        self.output_label = QtWidgets.QLabel(self.grid_layout_widget)
        font = QtGui.QFont()
        font.setPointSize(self.qline_size)
        self.output_label.setFont(font)
        self.grid_layout.addWidget(self.output_label, 5, 3, 1, 1)

        MainWindow.setCentralWidget(self.central_widget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_file_name(self):
        from tkinter import Tk, filedialog
        Tk().withdraw()
        file_name = filedialog.askopenfilename()
        self.file_label.setText("" + file_name)

    def set_learn(self):
        try:
            file_path = self.file_label.text()
            dataName = file_path.split("/")[-1]
            columnNames = labels[dataName]
        except:
            # If data not known, just give random column names
            columnNames = []
            f = open(file_path, 'r')
            lines = f.readlines()
            nbColumns = len(lines[0].split(","))
            for i in range(nbColumns):
                columnNames.append(str(i))
        try:
            if self.radio_Button_ID3.isChecked():
                self.container = Container()
                self.container._set_debug(columnNames)
                self.container.load_from_file(file_path, len(columnNames) - 1)
                self.tree = learn(self.container)

                self.predictButton.setEnabled(True)
                print("ID3")

            elif self.radio_button_C45.isChecked():
                pruneVal = float(self.lcdNumber.value())
                training_data = load_data(file_path)
                self.tree = build_decision_tree(training_data)
                prune_tree(self.tree, pruneVal, debug=False)

                self.predictButton.setEnabled(True)
                print("C4.5")
        except:
            print("Learning Error")

    def set_predict(self):
        try:
            to_predict = self.predictionLabel.text()
            to_predict = [x.strip() for x in to_predict.split(',')]
            if self.radio_Button_ID3.isChecked():
                prediction = self.tree.decide(to_predict)
                self.output_label.setText(prediction)
            elif self.radio_button_C45.isChecked():
                prediction = classify(to_predict, self.tree)
                self.output_label.setText(prediction)
        except:
            self.output_label.setText("Error")

    def set_erase(self):
        self.output_label.setText("")

    def on_slider_move(self, value):
        roundedVal = round(value / 100, 1)
        self.lcdNumber.display(roundedVal)

    def change_prune_State(self, radioButton):
        if radioButton.isChecked():
            self.lcdNumber.setEnabled(True)
            self.horizontalScrollBar.setEnabled(True)
        else:
            self.lcdNumber.setEnabled(False)
            self.horizontalScrollBar.setEnabled(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            print(path)
            self.file_label.setText("" + path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet('QMainWindow{background-color: darkgray;border: 2px solid black;}')
    Gui = window()
    sys.exit(app.exec_())
    # overcast, hot, high, false
    # med,med,2,4,big,high
