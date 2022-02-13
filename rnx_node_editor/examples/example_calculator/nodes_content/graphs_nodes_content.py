from PyQt5.QtWidgets import QLabel, QHBoxLayout
from rnx_node_editor.node_widget_node import NodeWidgetContent
from examples.example_calculator.views.scatter_plot import *
from examples.example_calculator.views.line_plot import line_chart


class GraphsNodesContent(NodeWidgetContent):


    def generate_graph(self, input_node, dimension):
        """
        We can do two different things
        1: d > 3: Not possible
        2: d == 3: graph_3d
        3: d <= 2: graph
        4: d <= 0 Not possible
        """
        if dimension > 3:
            self.node.gr_node.setToolTip("Los datos con más de 3 dimensiones no pueden ser visualizados con este gráfico")
            self.node.mark_invalid()
            return False
        elif dimension == 3:
            self.graph_3d(input_node)
            return True
        elif dimension in [1, 2]:
            self.graph(dimension) # debería recibir las dimensiones como parámetro
            return True
        else:
            self.node.gr_node.setToolTip("Error: Dimensión 0 o menor")
            return False

    def graph_3d(self, input_node):
        print("1")
        view_3d(input_node, self.node.data)

    def graph(self, dimension):
        view(dimension, self.node.data)


class LineGraphContent(NodeWidgetContent):

    def generate_line_chart(self, node):
        return line_chart(node)
