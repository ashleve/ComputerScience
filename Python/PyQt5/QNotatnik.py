import sys

import PyQt5
from PyQt5 import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QVBoxLayout, QPushButton, QLineEdit, \
    QLabel, QFileSystemModel, QTreeView, QToolBar, QSplitter, QMenuBar, QTextEdit, QRadioButton, QButtonGroup, \
    QColorDialog, QInputDialog, QComboBox, QFileDialog, QAction
from PyQt5.uic.properties import QtGui, QtCore


class _PaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.main_widget = QWidget()

        self.split_pane = QSplitter()
        self.left_v_box = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.pal = QPalette()
        self.opened_file = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)

        # MENU BAR
        menu_bar = self.menuBar()
        _ = menu_bar.addMenu('&File')
        edit = menu_bar.addMenu('&Edit')

        copy = edit.addAction('&copy')
        copy.triggered.connect(self.text_edit.copy)
        paste = edit.addAction('&paste')
        paste.triggered.connect(self.text_edit.paste)
        select_all = edit.addAction('&select all')
        select_all.triggered.connect(self.text_edit.selectAll)
        undo = edit.addAction('&undo')
        undo.triggered.connect(self.text_edit.undo)
        redo = edit.addAction('&redo')
        redo.triggered.connect(self.text_edit.redo)

        window_layout = QVBoxLayout()
        window_layout.addWidget(menu_bar, 0)

        # TOOL BAR
        tool_bar = QToolBar()
        button = QAction(QIcon("icons/new-file.png"), "a", self)
        button.triggered.connect(self.new_file)
        tool_bar.addAction(button)
        button = QAction(QIcon("icons/open-archive.png"), "a", self)
        button.triggered.connect(self.getfile)
        tool_bar.addAction(button)
        button = QAction(QIcon("icons/save.png"), "a", self)
        button.triggered.connect(self.save_file)
        tool_bar.addAction(button)
        button = QAction(QIcon("icons/saveas.png"), "a", self)
        button.triggered.connect(self.save_as)
        tool_bar.addAction(button)
        tool_bar.addSeparator()
        button = QAction(QIcon("icons/undo.png"), "a", self)
        button.triggered.connect(self.text_edit.undo)
        tool_bar.addAction(button)
        button = QAction(QIcon("icons/redo.png"), "a", self)
        button.triggered.connect(self.text_edit.redo)
        tool_bar.addAction(button)
        tool_bar.addSeparator()
        button = QAction(QIcon("icons/copy.png"), "a", self)
        button.triggered.connect(self.text_edit.copy)
        tool_bar.addAction(button)
        button = QAction(QIcon("icons/paste.png"), "a", self)
        button.triggered.connect(self.text_edit.paste)
        tool_bar.addAction(button)
        button = QAction(QIcon("icons/selection.png"), "a", self)
        button.triggered.connect(self.text_edit.selectAll)
        tool_bar.addAction(button)
        window_layout.addWidget(tool_bar, 1)

        # SPLIT PANE
        window_layout.addWidget(self.split_pane, 2)

        # LEFT PANE
        w = QWidget()
        w.setLayout(self.left_v_box)
        w.setFixedWidth(250)
        self.split_pane.addWidget(w)

        # RIGHT PANE
        self.split_pane.addWidget(self.text_edit)

        # LEFT PANE FONT SIZE
        combo_box = QComboBox(self)
        combo_box.addItem("10")
        combo_box.addItem("12")
        combo_box.addItem("14")
        combo_box.addItem("16")
        combo_box.addItem("18")
        combo_box.activated[str].connect(self.change_font_size)
        self.left_v_box.addWidget(combo_box)

        # # LEFT PANE FONT STYLE
        # options = ['Times Nes Roman', 'Arial', 'Courier New']
        # cbg = QButtonGroup(self)
        # cbg.setExclusive(True)
        # for id, ch in enumerate(options):
        #     rb = QRadioButton(ch)
        #     cbg.addButton(rb)
        #     cbg.setId(rb, id)
        #     self.left_v_box.addWidget(rb)

        # LEFT PANE FONT STYLE
        options = ['Times Nes Roman', 'Arial', 'Courier New']
        rb = QRadioButton(options[0])
        rb.clicked.connect(self.set_font1)
        self.left_v_box.addWidget(rb)
        rb = QRadioButton(options[1])
        rb.pressed.connect(self.set_font2)
        self.left_v_box.addWidget(rb)
        rb = QRadioButton(options[2])
        rb.pressed.connect(self.set_font3)
        self.left_v_box.addWidget(rb)

        # LEFT PANE COLOR PALETTE
        pal_widget = QWidget()
        pal_widget.setFixedHeight(120)
        pal_widget.setFixedWidth(120)
        palette = QGridLayout()
        pal_widget.setLayout(palette)
        self.left_v_box.addWidget(pal_widget)
        colors = ['#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49', '#458352', '#dcd37b',
                  '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b', '#f45b7a', '#ffffff']
        row, col = 0, 0
        num_of_columns = 4
        for c in colors:
            b = _PaletteButton(c)
            b.clicked.connect(self.ColorChanger(c, self.pal, self.text_edit, self.statusBar()))
            palette.addWidget(b, row, col)
            col += 1
            if col == num_of_columns:
                col = 0
                row += 1

        # ALIGN LEFT PANE TO TOP
        self.left_v_box.addStretch(1)

        # SET MAIN WINDOW
        self.main_widget.setLayout(window_layout)
        self.setCentralWidget(self.main_widget)

        # STATUS BAR
        self.statusBar().showMessage("Status bar")

        self.show()

    def getfile(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            with open(filenames[0], 'r') as f:
                data = f.read()
                self.text_edit.setText(data)
                self.opened_file = filenames[0]
                self.change_status("file " + filenames[0] + " opened")

    def save_file(self):
        if self.opened_file is None:
            print("no file opened")
            return
        with open(self.opened_file, 'w') as f:
            data = self.text_edit.toPlainText()
            f.write(data)
            self.change_status("file saved")
            print("file saved")

    def save_as(self):
        filename = self.getText()
        if filename is None:
            print("saving cancelled")
            self.change_status("saving cancelled")
            return
        with open(filename, 'w+') as f:
            data = self.text_edit.toPlainText()
            f.write(data)
            self.opened_file = filename
            self.change_status("file saved as " + filename)
            print("file saved as", filename)

    def getText(self):
        text, ok_pressed = QInputDialog.getText(self, "", "Filename:", QLineEdit.Normal, "")
        if ok_pressed and text != '':
            return text

    def new_file(self):
        self.opened_file = None
        self.text_edit.setText("")

    def set_font1(self):
        self.text_edit.setFont(QFont('Times Nes Roman'))
        self.change_status("font changed")

    def set_font2(self):
        self.text_edit.setFont(QFont('Courier New'))
        self.change_status("font changed")

    def set_font3(self):
        self.text_edit.setFont(QFont('Arial'))
        self.change_status("font changed")

    def change_font_size(self, size):
        self.text_edit.setFontPointSize(float(size))
        self.change_status("font size changed")

    def change_status(self, status):
        self.statusBar().showMessage(status)

    class ColorChanger:
        def __init__(self, color, pal, text_edit, status_bar):
            self.color = color
            self.pal = pal
            self.text_edit = text_edit
            self.status_bar = status_bar

        def __call__(self):
            self.pal.setColor(QPalette.Base, QColor(self.color))
            self.text_edit.setPalette(self.pal)
            print(self.color)
            self.status_bar.showMessage("background color changed")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
