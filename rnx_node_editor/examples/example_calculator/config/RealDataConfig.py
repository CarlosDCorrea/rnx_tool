from PyQt5.QtWidgets import (QDialog,
                             QVBoxLayout,
                             QPushButton,
                             QFileDialog,
                             QLabel,
                             QComboBox,
                             QHBoxLayout)


class RealDataConfigWindow(QDialog):

    def __init__(self, node, parent = None):
        super().__init__(parent)
        self.observers = []
        self.path = None
        self.extention = None
        self.separator = None
        self.setFixedSize(300, 200)
        self.setWindowTitle("Configuración de nodo: " + node.op_title)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.separators_section = QHBoxLayout()
        self.button = QPushButton("Abrir archivo.")
        self.button.clicked.connect(self.openfile)
        self.title = QLabel("Selecciona un archivo.")
        self.options = QComboBox()

        self.optionsLayout = QHBoxLayout()
        self.save = QPushButton("Ok")
        self.cancel = QPushButton("Cancelar")

        self.optionsLayout.addWidget(self.save)
        self.optionsLayout.addWidget(self.cancel)

        self.separators_section.addWidget(QLabel("Elija un separador"))
        self.separators_section.addWidget(self.options)

        self.save.clicked.connect(self.saveEvt)
        self.cancel.clicked.connect(self.cancelEvt)

        self.layout.addWidget(self.title)
        self.layout.addLayout(self.separators_section)
        self.layout.addWidget(self.button)
        self.layout.addLayout(self.optionsLayout)

        self.setLayout(self.layout)

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