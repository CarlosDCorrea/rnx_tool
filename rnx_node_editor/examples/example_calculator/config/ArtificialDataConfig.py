from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QComboBox,
    QLabel
)
from PyQt5.QtCore import Qt
from enum import Enum


class ArtificialDataConfigWindow(QDialog):
    def __init__(self, node, parent = None):
        super().__init__(parent)
        self.setSizeGripEnabled(False)
        self.observers =[]
        self.status = 0
        self.setWindowTitle("Configuración de nodo: " + node.op_title)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        selection_layout = QFormLayout()
        actions_layout = QFormLayout()
        self.options = QComboBox()
        self.options.addItem("Seleccionar")
        self.options.addItem("Esfera")
        self.options.addItem("Rollo Suizo")
        self.options.addItem("Toroide")
        self.options.setStyleSheet("color: #ffffff; background-color: #474747")

        selection_layout.addRow(QLabel("Datos"), self.options)
        self.save = QPushButton("Ok", self)
        self.cancel = QPushButton("Cancelar", self)
        actions_layout.addRow(self.save, self.cancel)

        self.save.clicked.connect(self.saveEvt)
        self.cancel.clicked.connect(self.cancelEvt)

        self.layout.addLayout(selection_layout)
        self.layout.addLayout(actions_layout)
        self.setLayout(self.layout)

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