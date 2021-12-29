import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, \
    QFontComboBox, QSpinBox, QApplication, QInputDialog
import difflib
from threading import Thread

from client import TextSource, Client
import common.operations as operations


class EditTextSource(TextSource):

    def get_text(self) -> str:
        return self.source.toPlainText()


class TextEditor(QMainWindow):
    def __init__(self, client: Client):
        super().__init__()
        self.setWindowTitle("Google docss")
        self.setGeometry(150, 100, 960, 480)
        self.client = client
        self.text = QTextEdit()
        self.textSource = EditTextSource(self.text)
        self.prev_text = ""  # здесь нужно хранить последнюю версию
        # текста до изменений
        self.text.textChanged.connect(self.send_operation)

        self.setCentralWidget(self.text)

        self.menu_bar = self.menuBar()
        self.toolbar = self.addToolBar("Edit")

        self.init_menu()
        self.init_toolbar()

        # Thread(target=self.update_text_edit).start()

        self.show()

    def send_operation(self):
        current_text = self.text.toPlainText()
        matcher = difflib.SequenceMatcher(None, self.prev_text, current_text)
        opcodes = matcher.get_opcodes()
        if opcodes[0][0] == 'equal':
            operation = opcodes[1]
        else:
            operation = opcodes[0]
        if operation[0] == 'insert':
            inserted_text = current_text[operation[3]:operation[4]]
            index = operation[1]
            self.client.put_operation_in_waiting(
                operations.InsertOperation(inserted_text, index))
        elif operation[0] == 'delete':
            index = operation[1]
            self.client.put_operation_in_waiting(
                operations.DeleteOperation(index))
        self.prev_text = current_text

    def init_menu(self):
        open_action = self.create_action("Open", "Ctrl+O", "Open file",
                                         self.open_file)
        create_server_action = self.create_action(
            "Create connection", "Alt+C", "Create connection to edit file",
            self.client.create_server(self.textSource))
        connect_to_server_action = self.create_action(
            "Connect to file", "Alt+F",
            "Connect to server and share your file",
            self.connect_to_server)

        file_menu = self.menu_bar.addMenu("&File")
        file_menu.addAction(open_action)
        file_menu.addAction(create_server_action)
        file_menu.addAction(connect_to_server_action)

    def open_file(self):
        filepath = Path(QFileDialog.getOpenFileName(
            self, "Choose text file", ".", "Text files (*.txt)")[0])
        with open(filepath) as file:
            self.text.setText(file.read())

    def connect_to_server(self):
        text, ok = QInputDialog.getText(self, 'Connect to server',
                                        'Enter server id')
        if ok:
            self.client.connect_to_server(text)

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

    def update_text_edit(self):
        while True:
            self.text.setText(self.client.doc_state)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    a = TextEditor(client)
    sys.exit(app.exec_())
