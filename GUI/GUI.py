import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QAction, QMessageBox, QRadioButton, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from Container import Container
from Container import create_subset
from Tree import learn
from collections import Counter
from c45 import *


labels = {'tennis.data': ["weather", "temp", "wind", "other", "play"],
          'car.data': ["buying", "maint", "doors", "persons", "lug_boot", "safety"]}


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
    def __init__(self):
        super(window, self).__init__()
        self.constants()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.show()

    def constants(self):
        self.qline_size = 12
        self.btn_text_size = 14
        self.label_text_size = 15
        self.radiobtn_text_size = 15

    def setupLabels(self, gridLayoutWidget, gridLayout):
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

    def setupButtons(self, gridLayoutWidget, gridLayout):
        font = QtGui.QFont()
        font.setPointSize(self.btn_text_size)
        font_important = QtGui.QFont()
        font_important.setPointSize(self.btn_text_size)
        font_important.setBold(True)

        pushButton = QtWidgets.QPushButton("Open", self.gridLayoutWidget)
        pushButton.setFont(font)
        pushButton.clicked.connect(self.setFileName)
        gridLayout.addWidget(pushButton, 0, 4, 1, 1)
        pushButton = QtWidgets.QPushButton("Learn", self.gridLayoutWidget)
        pushButton.setFont(font_important)
        pushButton.clicked.connect(self.setLearn)
        gridLayout.addWidget(pushButton, 1, 4, 1, 1)
        pushButton = QtWidgets.QPushButton("Predict", self.gridLayoutWidget)
        pushButton.setFont(font_important)
        pushButton.clicked.connect(self.setPredict)
        gridLayout.addWidget(pushButton, 4, 4, 1, 1)
        pushButton = QtWidgets.QPushButton("Plot", self.gridLayoutWidget)
        pushButton.setFont(font)
        pushButton.clicked.connect(self.setPlot)
        gridLayout.addWidget(pushButton, 5, 4, 1, 1)

    def setupRadioButtons(self, gridLayoutWidget, gridLayout):
        font = QtGui.QFont()
        font.setPointSize(self.radiobtn_text_size)

        horizontalLayout = QtWidgets.QHBoxLayout()

        self.radioButtonID3 = QtWidgets.QRadioButton("ID3", gridLayoutWidget)
        self.radioButtonID3.setFont(font)
        self.radioButtonID3.setChecked(True)

        horizontalLayout.addWidget(self.radioButtonID3)

        self.radioButtonC45 = QtWidgets.QRadioButton("C4.5", self.gridLayoutWidget)
        self.radioButtonC45.setFont(font)
        self.radioButtonC45.setChecked(False)
        self.radioButtonC45.toggled.connect(lambda:self.changePruneState(self.radioButtonC45))

        horizontalLayout.addWidget(self.radioButtonC45)

        gridLayout.addLayout(horizontalLayout, 1, 3, 1, 1)

    def setupQLine(self, gridLayoutWidget, gridLayout):

        self.fileLabel = QtWidgets.QLineEdit(gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(self.qline_size)
        self.fileLabel.setFont(font)
        gridLayout.addWidget(self.fileLabel, 0, 3, 1, 1)

        self.pruneLabel = QtWidgets.QLineEdit(gridLayoutWidget)
        self.pruneLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(self.qline_size)
        self.pruneLabel.setFont(font)
        gridLayout.addWidget(self.pruneLabel, 3, 3, 1, 1)

        self.predictionLabel = QtWidgets.QLineEdit(gridLayoutWidget)
        self.predictionLabel.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(self.qline_size)
        self.predictionLabel.setFont(font)
        gridLayout.addWidget(self.predictionLabel, 4, 3, 1, 1)


    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Techniques of Artificial Intelligence")
        MainWindow.resize(600, 300)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(26, 10, 530, 280))

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(5, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(10)

        self.setupLabels(self.gridLayoutWidget, self.gridLayout)
        self.setupButtons(self.gridLayoutWidget, self.gridLayout)
        self.setupRadioButtons(self.gridLayoutWidget, self.gridLayout)
        self.setupQLine(self.gridLayoutWidget, self.gridLayout)

        self.outputLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(self.qline_size)
        self.outputLabel.setFont(font)
        self.gridLayout.addWidget(self.outputLabel, 5, 3, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setFileName(self):
        from tkinter import Tk, filedialog
        Tk().withdraw()
        fileName = filedialog.askopenfilename()
        self.fileLabel.setText("" + fileName)

    def setLearn(self):
        try:
            filePath = self.fileLabel.text()
            dataName = filePath.split("/")[-1]
            columnNames = labels[dataName]
        except:
            print("Data not known")
        try:
            if(self.radioButtonID3.isChecked()):
                self.container = Container()
                self.container._set_debug(columnNames)
                self.container.load_from_file(filePath, len(columnNames)-1)
                self.tree = learn(self.container)

                #print(list(set(self.container.data[0])))
                print("ID3")

            elif(self.radioButtonC45.isChecked()):
                pruneVal = float(self.pruneLabel.text())
                trainingData = load_data(filePath)
                self.tree = build_decision_tree(trainingData)
                prune_tree(self.tree, pruneVal, debug=False)
                print("C4.5")
        except:
            print("Learning Error")


    def setPredict(self):
        try:
            toPredict = self.predictionLabel.text()
            toPredict = [x.strip() for x in toPredict.split(',')]
            if(self.radioButtonID3.isChecked()):
                prediction = self.tree.decide(toPredict)
                self.outputLabel.setText(prediction)
            elif(self.radioButtonC45.isChecked()):
                prediction = classify(toPredict, self.tree)
                self.outputLabel.setText(prediction)
        except:
            self.outputLabel.setText("Error")

    def setPlot(self):
        """TO DO"""

    def changePruneState(self, radioButton):
        if radioButton.isChecked() == True:
            self.pruneLabel.setEnabled(True)
        else:
            self.pruneLabel.setEnabled(False)  

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            print(path)
            self.fileLabel.setText("" + path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())
    #overcast, hot, high, false
    #med,med,2,4,big,high
