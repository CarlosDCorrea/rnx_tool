from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout,QPushButton, QComboBox, QLabel
from PyQt5.QtCore import Qt
from enum import Enum

class ArtificalDataConfigWindow(QDialog):
    def __init__(self, node, parent = None):
        super().__init__(parent)
        self.observers =[]
        self.status = 0
        self.setFixedSize(300, 200)
        self.setWindowTitle("Configuración de nodo: " + node.op_title)
        self.init_ui()

    def init_ui(self):

        self.layout = QVBoxLayout()
        dataLabel = QHBoxLayout()
        optionsLabel = QHBoxLayout()
        # def combo box
        self.options = QComboBox()
        self.options.addItem("Seleccionar")
        self.options.addItem("Esfera")
        self.options.addItem("Rollo Suizo")
        self.options.addItem("Toroide")

        dataLabel.addWidget(QLabel("Datos"))
        dataLabel.addWidget(self.options)

        self.save = QPushButton("Ok", self)
        self.cancel = QPushButton("Cancelar", self)


        optionsLabel.addWidget(self.save)
        optionsLabel.addWidget(self.cancel)

        self.save.clicked.connect(self.saveEvt)
        self.cancel.clicked.connect(self.cancelEvt)

        self.layout.addLayout(dataLabel)
        self.layout.addLayout(optionsLabel)
        self.setLayout(self.layout)
        self.setFixedSize(300,200)

        self.setWindowModality(Qt.ApplicationModal)


    def saveEvt(self):
        opt = self.options.currentIndex()
        if opt != 0:
            self.status = opt
            self.notifyAllObservers()
            self.close()

    def cancelEvt(self):
        self.close()

    def addObservers(self, content):
        self.observers.append(content)

    def notifyAllObservers(self):
        for i in self.observers:
            i.update()


class TypesConfig(Enum):
    Select = 0
    Sphere = 1
    Swiss_Roll = 2
    Toroid = 3