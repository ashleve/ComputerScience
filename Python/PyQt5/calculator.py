import sys

import PyQt5
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.uic.properties import QtGui


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.grid_layout = QGridLayout()
        # self.grid_layout.set

        self.q_widget = QWidget()
        self.q_widget.setLayout(self.grid_layout)

        self.line = QLineEdit(self)
        self.grid_layout.addWidget(self.line, 0, 0, 1, 0)


        for x in range(1, 4):
            for y in range(3):
                button = QPushButton(str(str(3*x+y)))
                # button.setMinimumWidth(100)
                button.setMaximumHeight(1000)
                assert isinstance(QtGui, object)
                self.grid_layout.addWidget(button, x, y)

        button = QPushButton("+")
        button.setMaximumHeight(1000)
        self.grid_layout.addWidget(button, 4, 0)
        button = QPushButton("0")
        button.setMaximumHeight(1000)
        self.grid_layout.addWidget(button, 4, 1)
        button = QPushButton("-")
        button.setMaximumHeight(1000)
        self.grid_layout.addWidget(button, 4, 2)
        # self.grid_layout.addWidget(QLabel("Podaj cyfrę"), 5, 0)
        self.statusBar().showMessage("Podaj cyfrę")
        self.setCentralWidget(self.q_widget)
        # self.grid_layout.setSpacing(100)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
