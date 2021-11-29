from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, \
    QToolBar, QComboBox, QFontComboBox, QSpinBox
from PyQt5.QtGui import QFontDatabase


class TextRedactor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text = QTextEdit()
        self.setCentralWidget(self.text)

        self.menu_bar = self.menuBar()
        self.toolbar = self.addToolBar("Edit")

        self.init_menu()
        self.init_toolbar()

        self.show()

    def init_menu(self):
        open_action = self.create_action("Open", "Ctrl+O", "Open file",
                                         self.open_file)
        # save_action = self.create_action("Download", "Ctrl+D",
        #                                  "Download file", self.download_file)
        # create_file_action = self.create_action(
        #     "New", "Ctrl+N", "Create new file", self.create_file)

        file_menu = self.menu_bar.addMenu("&File")
        file_menu.addAction(open_action)
        # file_menu.addAction(save_action)
        # file_menu.addAction(create_file_action)

    def open_file(self):
        filepath = Path(QFileDialog.getOpenFileName(
            self, "Choose text file", ".", "Text files (*.txt)")[0])
        with open(filepath) as file:
            self.text.setText(file.read())

    # def download_file(self):
    #     # todo

    # def create_file(self):
    #     # do smth to create new file

    def init_toolbar(self):
        font_box = QFontComboBox()
        font_box.currentFontChanged.connect(lambda font:
                                           self.text.setCurrentFont(font))
        fontsize_box = QSpinBox()
        fontsize_box.setValue(14)
        fontsize_box.setSuffix(" pt")
        fontsize_box.valueChanged.connect(lambda size:
                                          self.text.setFontPointSize(size))
        self.toolbar.addWidget(font_box)
        self.toolbar.addWidget(fontsize_box)

    def create_action(self, name, shortcut, status_tip, triggered_method):
        action = QAction(name, self)
        action.setShortcut(shortcut)
        action.setStatusTip(status_tip)
        action.triggered.connect(triggered_method)
        return action
