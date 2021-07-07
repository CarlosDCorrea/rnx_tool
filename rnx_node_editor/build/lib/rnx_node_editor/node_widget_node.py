from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFocusEvent
from .node_serializable import Serializable


class NodeWidgetContent(QWidget, Serializable):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.layout = QVBoxLayout()
        self.title_label = QLabel("Seleccione los datos a cargar")

        self.init_ui()

    def init_ui(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(MyQTextEdit("Esfera, Rollo suizo, curva S"))

    def set_editing_flag(self, value: bool) -> bool:
        self.node.scene.scene.views()[0].editing_flag = value
        return self.node.scene.scene.views()[0].editing_flag

    def serialize(self):
        return {

        }

    def deserialize(self, data, dictionary=None):
        if dictionary is None:
            dictionary = {}
        return False


class MyQTextEdit(QTextEdit):

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().set_editing_flag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().set_editing_flag(False)
        super().focusOutEvent(event)
