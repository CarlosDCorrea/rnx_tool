from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QFocusEvent
from .node_serializable import Serializable


class NodeWidgetContent(QWidget, Serializable):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.layout = QVBoxLayout()
        self.condition = self.node.title

        self.init_ui()

    def init_ui(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def set_editing_flag(self, value: bool) -> bool:
        self.node.scene.get_view().editing_flag = value
        return self.node.scene.get_view().editing_flag

    def serialize(self):
        return {

        }

    def deserialize(self, data, dictionary=None):
        if dictionary is None:
            dictionary = {}
        return True


class MyQLineEdit(QLineEdit):
    def focusInEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().set_editing_flag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.parentWidget().set_editing_flag(False)
        super().focusOutEvent(event)
