from PyQt5.QtWidgets import QPushButton, QAction


def load_recent_files():
    ll = []
    with open("recents.dcr", "r") as fle:
        for line in fle.readlines():
            ll.append(line.strip("\n"))
        return ll


def save_recents(pwd):
    with open("recents.dcr", "a") as fle:
        fle.write(str(pwd) + "\n")


import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow


class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle('Techiniques of Artificial Intelligence')
        self.setWindowIcon(QIcon('logo.png'))
        extractAction = QAction('&Get to the choppah', self)
        extractAction.setShortcut('Ctrl+R')
        extractAction.setStatusTip('leave the app')
        extractAction.triggered.connect(self.run)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        extractAction = QAction(QIcon('pic.png'), 'flee the scene', self)
        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar('extraction')
        self.toolBar.addAction(extractAction)

        self.load_training_data()
        self.load_testing_data()
        self.run()
        self.show()

    def load_training_data(self):
        btn = QPushButton('Load training data', self)
        btn.clicked.connect(self.read_data)
        btn.resize(100, 100)
        btn.move(0,400)
        self.show()

    def load_testing_data(self):
        btn = QPushButton('Load testing data', self)
        btn.clicked.connect(self.read_data)
        btn.resize(100, 100)
        btn.move(0, 200)
        self.show()

    def run(self):
        btn = QPushButton('Run', self)
        btn.clicked.connect(self.read_data)
        btn.resize(100, 50)
        btn.move(0, 300)
        self.show()

    def read_data(self):
        ll = load_recent_files()
        for i in ll:
            print(i)

    def close_application(self):

        choice = QMessageBox.question(self, 'Message',
                                      "Are you sure to quit?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('quit application')
            sys.exit()
        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())
