from PyQt5.QtWidgets import QLabel, QHBoxLayout
from rnx_node_editor.node_widget_node import NodeWidgetContent
from examples.example_calculator.views.scatter_plot import *
from examples.example_calculator.views.line_plot import line_chat


class GraphsNodesContent(NodeWidgetContent):
    def init_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.text_points = QLabel(self.node.content_labels[0])
        self.text_dimensions = QLabel(self.node.content_labels[1])

        self.layout.addWidget(self.text_points)
        self.layout.addWidget(self.text_dimensions)

    """
    We can do two different things 
    1: when d = 3 we use the function for 3 dimensions
    2: when d < 3 we use the function for 2 or less dimensions
    """

    def generate_graph(self, dimension):
        if dimension == 3:
            self.graph_3d()
        elif dimension <= 3:
            self.graph()

    def graph_3d(self):
        view_3d(self.node.data)

    def graph(self):
        view(self.node.data)


class LineGraphContent(NodeWidgetContent):
    def init_ui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.text_method = QLabel(self.node.content_labels[0])
        self.text_rnx = QLabel(self.node.content_labels[1])

        self.layout.addWidget(self.text_method)
        self.layout.addWidget(self.text_rnx)

    def generate_line_chart(self, node):
        return line_chat(node)
