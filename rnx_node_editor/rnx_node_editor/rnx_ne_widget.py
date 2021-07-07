from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout,
                             QGraphicsItem,
                             QPushButton,
                             QTextEdit,
                             QApplication,
                             QMessageBox)
from PyQt5.QtGui import (QBrush,
                         QPen,
                         QColor,
                         QFont)
from PyQt5.QtCore import Qt, QFile
from .view_graphics_view import ViewQGraphicsView
from .node_scene import Scene, InvalidFile
from .node_node import Node
from .node_socket import Socket
from .node_edge import Edge
import os

"""
This is our main window
"""


class RnxNodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gr_scene = Scene()
        self.view = ViewQGraphicsView(self.gr_scene.scene, self)
        self.layout = QVBoxLayout()

        self.file_name = None

        self.init_ui()

    def is_modified(self):
        return self.gr_scene.is_modified()

    def is_file_name_set(self):
        return self.file_name

    def get_selected_items(self):
        return self.gr_scene.get_selected_items()

    def has_selected_item(self):
        return len(self.get_selected_items()) != 0

    def can_undo(self):
        return self.gr_scene.history.can_undo()

    def can_redo(self):
        return self.gr_scene.history.can_redo()

    def user_friendly_current_file(self):
        name = os.path.basename(self.file_name) if self.is_file_name_set() else "New Graph"
        print(self.is_modified())
        return name + ("*" if self.is_modified() else "")

    def file_new(self):
        self.gr_scene.clear()
        self.file_name = None
        self.gr_scene.history.clear()
        self.gr_scene.history.store_initial_history_stamp()

    def file_load(self, file_name):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.gr_scene.load_from_file(file_name)
            self.file_name = file_name
            self.gr_scene.history.clear()
            self.gr_scene.history.store_initial_history_stamp()
            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, f"Error loading file {os.path.basename(file_name)}", str(e))
            return False
        finally:
            QApplication.restoreOverrideCursor()

        return False

    def file_save(self, file_name=None):
        print("el nombre es:", file_name)
        if file_name:
            self.file_name = file_name
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.gr_scene.save_to_file(self.file_name)
        QApplication.restoreOverrideCursor()
        return True

    def init_ui(self):
        """
        Window configuration
        """
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.layout.addWidget(self.view)

    def add_node(self):
        node = Node(self.gr_scene, "Artificial data", outputs=[2])
        node.set_pos(-200, -300)
        node1 = Node(self.gr_scene, "PCA", inputs=[1], outputs=[1])
        node1.set_pos(200, -300)
        node2 = Node(self.gr_scene, "LLE", inputs=[1, 1], outputs=[1])
        node2.set_pos(300, 200)
        node3 = Node(self.gr_scene, "LE", inputs=[1, 2], outputs=[1])

        edge = Edge(self.gr_scene, node.outputs[0], node1.inputs[0], type_edge=2)
        edge2 = Edge(self.gr_scene, node1.outputs[0], node2.inputs[0], type_edge=2)

        self.gr_scene.history.store_initial_history_stamp()
