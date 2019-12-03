import sys

import PyQt5
from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QVBoxLayout, QPushButton, QLineEdit, \
    QLabel, QFileSystemModel, QTreeView, QToolBar, QSplitter, QMenuBar
from PyQt5.uic.properties import QtGui


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.q_widget = QWidget()
        self.model = QFileSystemModel()
        self.model2 = QFileSystemModel()
        self.tree = QTreeView()
        self.tree2 = QTreeView()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)

        self.model.setRootPath('')
        self.tree.setModel(self.model)
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        self.model2.setRootPath('')
        self.tree2.setModel(self.model)
        self.tree2.setAnimated(False)
        self.tree2.setIndentation(20)
        self.tree2.setSortingEnabled(True)

        menu_bar = self.menuBar()
        menu_bar.addMenu('&Files')
        menu_bar.addMenu('&Mark')
        menu_bar.addMenu('&Commands')
        menu_bar.addMenu('&Net')
        menu_bar.addMenu('&Show')
        menu_bar.addMenu('&Configuration')
        menu_bar.addMenu('&Start')
        m2 = QMenuBar()
        m2.addMenu('&Help')
        menu_bar.setCornerWidget(m2)

        window_layout = QVBoxLayout()
        window_layout.addWidget(menu_bar, 0)

        tool_bar = QToolBar()

        button = QPushButton()
        button.setMaximumWidth(50)
        tool_bar.addWidget(button)

        button = QPushButton()
        button.setMaximumWidth(50)
        tool_bar.addWidget(button)

        button = QPushButton()
        button.setMaximumWidth(50)
        tool_bar.addWidget(button)

        window_layout.addWidget(tool_bar, 1)

        split_pane = QSplitter()
        split_pane.addWidget(self.tree)
        split_pane.addWidget(self.tree2)
        window_layout.addWidget(split_pane, 2)

        tool_bar_down = QToolBar()
        qlabel = QLabel("c/:>")
        qlabel.setMaximumWidth(30)
        tool_bar_down.addWidget(qlabel)
        tool_bar_down.addWidget(QLineEdit())
        window_layout.addWidget(tool_bar_down, 3)

        tool_bar_down2 = QSplitter()
        buttons = ["F3 View", "F4 View", "F5 View", "F6 View", "F7 View"]
        for i in range(len(buttons)):
            button = QPushButton(buttons[i])
            button.setMaximumHeight(25)
            tool_bar_down2.addWidget(button)

        window_layout.addWidget(tool_bar_down2, 4)

        self.q_widget.setLayout(window_layout)
        self.setCentralWidget(self.q_widget)

        self.setWindowIcon(QIcon('/home/ukasz/PycharmProjects/KCK-LAB01/logo.png')) # nie dziala na linuxie



        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
