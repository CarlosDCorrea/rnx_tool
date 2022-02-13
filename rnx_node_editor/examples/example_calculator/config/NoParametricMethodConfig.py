from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QPushButton,
    QLabel,
    QLineEdit)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

class NoParametricMethodConfigWindow(QDialog):

    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.observers = []
        self.d = 3
        self.setWindowTitle("Configuración  de nodo: " + node.op_title)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Dimension
        self.dimension_layout = QFormLayout()
        self.edit_text_dimensions = QLineEdit("3")
        self.edit_text_dimensions.setValidator(QIntValidator(1, 100))
        self.dimension_layout.addRow(QLabel("Dimensiones"), self.edit_text_dimensions)

        # Options
        self.actions_layout = QFormLayout()
        self.save = QPushButton("Ok", self)
        self.cancel = QPushButton("Cancelar", self)
        self.actions_layout.addRow(self.save, self.cancel)

        self.save.clicked.connect(self.saveEvt)
        self.cancel.clicked.connect(self.cancelEvt)

        self.layout.addLayout(self.dimension_layout)
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
        self.notifyAllObservers()
        self.close()

    def cancelEvt(self):
        self.edit_text_dimensions.setText(str(self.d))
        self.close()
