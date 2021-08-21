from PyQt5.QtWidgets import  QDialog, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout


class RealDataConfigWindow(QDialog):

    def __init__(self, node, parent = None):
        super().__init__(parent)
        self.observers = []
        self.path = None
        self.extention = None
        self.setFixedSize(300, 200)
        self.setWindowTitle("Configuration of node: " + node.op_title)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.button = QPushButton("Open File")
        self.button.clicked.connect(self.openfile)
        self.title = QLabel("-")

        self.optionsLayout = QHBoxLayout()
        self.save = QPushButton("Ok")
        self.cancel = QPushButton("Cancel")

        self.optionsLayout.addWidget(self.save)
        self.optionsLayout.addWidget(self.cancel)

        self.save.clicked.connect(self.saveEvt)
        self.cancel.clicked.connect(self.cancelEvt)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.button)
        self.layout.addLayout(self.optionsLayout)

        self.setLayout(self.layout)


    def openfile(self):
        try:
            file_names, _ = QFileDialog.getOpenFileNames(self, "Open file")
            self.title.setText(file_names[0].split('/')[-1])
            self.path = file_names[0]
            self.extention = self.title.text().split(".")[-1]

        except():
            print("_")

    def saveEvt(self):
        if self.path == None:
            return

        self.close()

    def cancelEvt(self):
        self.close()

    def addObserver(self, content):
        self.observers.append(content)

    def notifyAllObservers(self):
        for i in self.observers:
            i.update()