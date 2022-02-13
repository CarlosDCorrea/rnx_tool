from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QLabel,
    QLineEdit)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

class ParametricMethodConfigWindow(QDialog):

    def __init__(self, node, parent = None):
        super().__init__(parent)
        self.observers = []
        self.d = 3
        self.n = 10
        self.setWindowTitle("Configuración  de nodo: " + node.op_title)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Dimension
        self.dimensionLayout = QFormLayout()
        self.edit_text_dimensions = QLineEdit("3")
        self.edit_text_dimensions.setValidator(QIntValidator(1, 100))
        self.dimensionLayout.addRow(QLabel("Dimensiones"), self.edit_text_dimensions)

        # Neighbours
        self.neighboursLayout = QFormLayout()
        self.edit_text_neighbours = QLineEdit("10")
        self.edit_text_neighbours.setValidator(QIntValidator(1, 100))
        self.dimensionLayout.addRow(QLabel("Vecindarios"), self.edit_text_neighbours)

        # Options
        self.actions_layout = QFormLayout()
        self.save = QPushButton("Ok", self)
        self.cancel = QPushButton("Cancelar", self)
        self.actions_layout.addRow(self.save, self.cancel)

        self.save.clicked.connect(self.saveEvt)
        self.cancel.clicked.connect(self.cancelEvt)

        self.layout.addLayout(self.dimensionLayout)
        self.layout.addLayout(self.neighboursLayout)
        self.layout.addLayout(self.actions_layout)

        self.setLayout(self.layout)

        self.setWindowModality(Qt.ApplicationModal)

    def addObserver(self, content):
        self.observers.append(content)

    def notifyAllObservers(self):
        for i in self.observers:
            i.update()

    def saveEvt(self):
        self.d = int(self.edit_text_dimensions.text())
        self.n = int(self.edit_text_neighbours.text())
        self.notifyAllObservers()
        self.close()

    def cancelEvt(self):
        self.edit_text_dimensions.setText(str(self.d))
        self.edit_text_neighbours.setText(str(self.n))
        self.close()







