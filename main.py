import sys
import os
from PyQt5.QtWidgets import QApplication
from client.gui import TextEditor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = TextEditor()
    sys.exit(app.exec_())
