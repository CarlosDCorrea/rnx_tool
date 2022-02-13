from PyQt5.QtWidgets import (QDialog,
                             QVBoxLayout,
                             QFormLayout,
                             QPushButton,
                             QFileDialog,
                             QLabel,
                             QComboBox,
                             QHBoxLayout)

from PyQt5.QtCore import Qt


class RealDataConfigWindow(QDialog):

    def __init__(self, node, parent = None):
        super().__init__(parent)
        self.observers = []
        self.path = None
        self.extention = None
        self.separator = None
        self.setWindowTitle("Configuración de nodo: " + node.op_title)
        self.init_ui()

    def init_ui(self):
        self.outer_layout = QVBoxLayout()
        self.actions_layout = QHBoxLayout()
        self.form_layout = QFormLayout()

        self.options = QComboBox()
        self.options.setStyleSheet("color: #ffffff; background-color: #474747")

        self.title = QLabel("Selecciona un archivo.")
        self.title.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Abrir archivo.")
        self.button.clicked.connect(self.openfile)
        self.save = QPushButton("Ok")
        self.cancel = QPushButton("Cancelar")
        self.save.clicked.connect(self.saveEvt)
        self.cancel.clicked.connect(self.cancelEvt)
        self.actions_layout.addWidget(self.save)
        self.actions_layout.addWidget(self.cancel)

        self.form_layout.addRow(QLabel('Seleccione un separador:'), self.options)

        self.outer_layout.addWidget(self.title)
        self.outer_layout.addLayout(self.form_layout)
        self.outer_layout.addWidget(self.button)
        self.outer_layout.addLayout(self.actions_layout)

        self.setLayout(self.outer_layout)

    def addSeparators(self, separators):
        self.options.clear()
        for item in separators:
            self.options.addItem(item)

    def openfile(self):
        try:
            file_names, _ = QFileDialog.getOpenFileNames(self, "Abrir archivo")
            if file_names:
                self.title.setText(file_names[0].split('/')[-1])
                self.path = file_names[0]
                self.extention = self.title.text().split(".")[-1]

        except():
            print("_")

    def saveEvt(self):
        if self.path == None:
            return
        self.separator = self.options.currentText()
        print(self.separator)
        self.notifyAllObservers()
        self.close()

    def cancelEvt(self):
        self.close()

    def addObserver(self, content):
        self.observers.append(content)

    def notifyAllObservers(self):
        for i in self.observers:
            i.update()