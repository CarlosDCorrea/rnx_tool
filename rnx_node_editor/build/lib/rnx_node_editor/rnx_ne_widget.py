from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout,
                             QGraphicsItem,
                             QPushButton,
                             QTextEdit,
                             QApplication)
from PyQt5.QtGui import (QBrush,
                         QPen,
                         QColor,
                         QFont)
from PyQt5.QtCore import Qt, QFile
from .view_graphics_view import ViewQGraphicsView
from .node_scene import Scene
from .node_node import Node
from .node_socket import Socket
from .node_edge import Edge

"""
This is our main window
"""


class RnxNodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gr_scene = Scene()
        self.view = ViewQGraphicsView(self.gr_scene.scene, self)
        self.layout = QVBoxLayout()

        self.style_sheet_filename = 'qss/node_style.qss'
        self.load_style_sheet(self.style_sheet_filename)

        self.init_ui()

    def init_ui(self):
        """
        Window configuration
        """


        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.layout.addWidget(self.view)

        self.add_node()

    def add_node(self):
        node = Node(self.gr_scene, "Artificial data", outputs=[8])
        node.set_pos(-200, -300)
        node1 = Node(self.gr_scene, "PCA", inputs=[1], outputs=[6])
        node1.set_pos(200, -300)
        node2 = Node(self.gr_scene, "LLE", inputs=[3, 7], outputs=[2])
        node2.set_pos(300, 200)
        node3 = Node(self.gr_scene, "LE", inputs=[8, 2], outputs=[4])

        edge = Edge(self.gr_scene, node.outputs[0], node1.inputs[0], type_edge=2)
        edge2 = Edge(self.gr_scene, node1.outputs[0], node2.inputs[0], type_edge=2)

    def load_style_sheet(self, filename):
        # print("STYLE loaded: ", filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly or QFile.Text)
        style_sheet = file.readAll()
        QApplication.instance().setStyleSheet(str(style_sheet, encoding="utf-8"))
