from PyQt5.QtWidgets import QWidget, QMessageBox


class ConnectServerWindow(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create connection")
        self.setGeometry(100, 100, 100, 100)
        self.setIcon(QMessageBox.Information)
        self.setText("You created connection. Your file id:")
        self.setStandardButtons(QMessageBox.Ok)
        returned = self.exec_()
        if returned == QMessageBox.Ok:
            self.close()
