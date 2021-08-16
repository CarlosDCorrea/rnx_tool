from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel,QPushButton

class Dialog(QDialog):

    def __init__(self, message: str,parent = None):
        super().__init__(parent)
        self.setFixedSize(300, 150)
        self.setWindowTitle("Message")
        self.init_ui(message)
        self.exec_()

    def init_ui(self, message):

        self.layout = QVBoxLayout()

        self.message = QLabel(message)
        self.done = QPushButton("Done")

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.done)

        self.done.clicked.connect(self.doneEvt)

        self.setLayout(self.layout)

    def doneEvt(self):
        self.destroy()