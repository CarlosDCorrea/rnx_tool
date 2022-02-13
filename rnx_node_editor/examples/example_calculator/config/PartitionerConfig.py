from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QFormLayout, QComboBox
from PyQt5.QtCore import Qt


class PartitionerConfigWindow(QDialog):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.observers = []
        self.column = None
        self.setWindowTitle("Configuración  de nodo: " + node.op_title)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        dataLabel = QFormLayout()
        optionsLabel = QFormLayout()

        self.options = QComboBox()
        self.options.setStyleSheet("color: #ffffff; background-color: #474747")

        dataLabel.addRow(QLabel("Seleccione una columna"), self.options)

        self.save = QPushButton("Ok", self)
        self.cancel = QPushButton("Cancelar", self)

        optionsLabel.addWidget(self.save)
        optionsLabel.addWidget(self.cancel)

        self.save.clicked.connect(self.saveEvt)
        self.cancel.clicked.connect(self.cancelEvt)

        self.layout.addLayout(dataLabel)
        self.layout.addLayout(optionsLabel)
        self.setLayout(self.layout)

        self.setWindowModality(Qt.ApplicationModal)

    def addItems(self, headers):
        self.options.clear()
        self.options.addItem("Seleccionar")
        for item in headers:
            self.options.addItem(item)

    def saveEvt(self):
        opt = self.options.currentIndex()
        if opt != 0:
            self.column = self.options.currentText()
            self.close()

    def cancelEvt(self):
        self.close()

    def addObserver(self, content):
        self.observers.append(content)

    def notifyAllObservers(self):
        for i in self.observers:
            i.update()
