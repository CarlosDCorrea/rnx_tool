from PyQt5.QtCore import pyqtSignal
from rnx_node_base import *
from rnx_conf import *
from nodes_content.methods_content import *
from nodes_content.artificial_data_widgets_content import ArtificialDataNodeContent
from nodes_content.real_data_widget_content import RealDataNodeContent
from nodes_content.metrics_content import RnxMetricContent
from nodes_content.table_of_data import TableOfDataNode
from nodes_content.graphs_nodes_content import *
from PyQt5.QtCore import QThread
from config.ParametricMethodConfig import ParametricMethodConfigWindow
from config.NoParametricMethodConfig import NoParametricMethodConfigWindow
from config.ArtificialDataConfig import ArtificalDataConfigWindow
from config.RealDataConfig import RealDataConfigWindow
from config.PartitionerConfig import PartitionerConfigWindow
from nodes_content.partitioner_content import PartitionerContentNode

DEBUG = True


@register_node(OP_NODE_PCA)
class RnxNodePCA(RnxNodeBase):
    icon = "icons/linear-regression.png"
    op_code = OP_NODE_PCA
    op_title = "PCA"

    def init_inner_classes(self):
        self.config = NoParametricMethodConfigWindow(self)
        self.content = NonParametricMethodsContent(self, self.config)
        self.config.addObserver(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.content.run()
        print(self.content.result)

    def configure(self):
        self.config.show()

    def get_node_components(self):
        return self.content.result


@register_node(OP_NODE_MDS)
class RnxNodeMDS(RnxNodeBase):
    icon = "icons/mds.png"
    op_code = OP_NODE_MDS
    op_title = "MDS"

    def init_inner_classes(self):
        self.config = NoParametricMethodConfigWindow(self)
        self.content = NonParametricMethodsContent(self, self.config)
        self.config.addObserver(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        return self.content.run()

    def configure(self):
        self.config.exec_()

    def get_node_components(self):
        return self.content.result


@register_node(OP_NODE_KPCA)
class RnxNodeKPCA(RnxNodeBase):
    icon = ""
    op_code = OP_NODE_KPCA
    op_title = "KPCA"

    def init_inner_classes(self):
        self.config = NoParametricMethodConfigWindow(self)
        self.content = NonParametricMethodsContent(self, self.config)
        self.config.addObserver(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        return self.content.run()

    def configure(self):
        self.config.exec_()

    def get_node_components(self):
        return self.content.result


@register_node(OP_NODE_LLE)
class RnxNodeLLE(RnxNodeBase):
    icon = "icons/graph.png"
    op_code = OP_NODE_LLE
    op_title = "LLE"

    def init_inner_classes(self):
        self.config = ParametricMethodConfigWindow(self)
        self.content = ParametricMethodsContent(self, self.config)
        self.config.addObserver(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.high_data = None
        self.low_data = None
        return self.content.run()

    def configure(self):
        self.config.exec_()

    def get_node_components(self):
        return self.content.result

@register_node(OP_NODE_LE)
class RnxNodeLE(RnxNodeBase):
    icon = ""
    op_code = OP_NODE_LE
    op_title = "LE"

    def init_inner_classes(self):
        self.config = ParametricMethodConfigWindow(self)
        self.content = ParametricMethodsContent(self, self.config)
        self.config.addObserver(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.high_data = None
        self.low_data = None
        return self.content.run()

    def configure(self):
        self.config.exec_()

    def get_node_components(self):
        return self.content.result

@register_node(OP_NODE_ISOMAP)
class RnxNodeISOMAP(RnxNodeBase):
    icon = "icons/isomap.png"
    op_code = OP_NODE_ISOMAP
    op_title = "ISOMAP"

    def init_inner_classes(self):
        self.config = ParametricMethodConfigWindow(self)
        self.content = ParametricMethodsContent(self, self.config)
        self.config.addObserver(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        return self.content.run()

    def configure(self):
        self.config.exec_()

    def get_node_components(self):
        return self.content.result

@register_node(OP_NODE_RNX)
class RnxNodeRNX(RnxNodeBase):
    icon = ""
    op_code = OP_NODE_RNX
    op_title = "RNX"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 0], outputs=[2])
        self.high_data = None
        self.score = None
        self.rnx = None
        self.is_configurable = False
        self.methods_dict_output = []  # this list contains methods dicts


    def init_inner_classes(self):
        self.content = RnxMetricContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def init_settings(self):
        super().init_settings()
        self.iinput_multi_edges = True


    def run(self):
        self.thread = MyThread(self)
        self.thread.finished.connect(self.is_runned)
        self.thread.start()

    def is_runned(self, x_pos):
        """
        When the independent thread finished, the paint method of the node
        is not called, therefore the new state is not visible, to address it,
        we update the pos node once the new thread is finished,
        this calls the paint method and repaint the node
        with the new state of the node.
        """
        self.set_pos(self.get_pos().x() + x_pos, self.get_pos().y())


@register_node(OP_NODE_ARTIFICIAL_DATA)
class RnxNodeArtificialData(RnxNodeBase):
    icon = "icons/sphere.png"
    op_code = OP_NODE_ARTIFICIAL_DATA
    op_title = "Datos Artificiales"
    data_name = None

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])

    def init_inner_classes(self):
        self.config = ArtificalDataConfigWindow(self)
        self.content = ArtificialDataNodeContent(self, self.config)
        self.config.addObservers(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        return self.content.run()

    def configure(self):
        self.config.exec_()

    def get_node_components(self):
        value = self.content.get_components()
        return value


@register_node(OP_NODE_REAL_DATA)
class RnxNodeRealData(RnxNodeBase):
    icon = "icons/real_data.png"
    op_code = OP_NODE_REAL_DATA
    op_title = "Datos"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])

    def init_inner_classes(self):
        self.config = RealDataConfigWindow(self)
        self.content = RealDataNodeContent(self, self.config)
        self.config.addObserver(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
         self.content.run()


    def get_node_components(self):
        value = self.content.get_components()
        return value

    def configure(self):
        separators = [',', ';', '/']
        self.config.addSeparators(separators)
        self.config.exec_()

@register_node(OP_NODE_PARTITIONER)
class RnxNodePartitioner(RnxNodeBase):
    icon = "icons/real_data.png"
    op_code = OP_NODE_PARTITIONER
    op_title = "Particionador"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0], outputs=[0])

    def init_inner_classes(self):
        self.config = PartitionerConfigWindow(self)
        self.content = PartitionerContentNode(self, self.config)
        self.config.addObserver(self.content)
        self.gr_node = NodeBaseGraphicsNode(self)


    def run(self):
         self.content.run()

    def configure(self):

        input_node = self.get_input()

        if not input_node:
            self.gr_node.setToolTip("There are missing inputs")
            self.mark_invalid()
            return

        headers = list(input_node.get_node_components().columns.values)
        self.config.addItems(headers)
        self.config.exec_()

    def get_node_components(self):
        value = self.content.get_components()
        return value



@register_node(OP_NODE_SCATTER_PLOT)
class RnxNodeScatterPlot(RnxNodeBase):
    icon = "icons/Scatter-plot.png"
    op_code = OP_NODE_SCATTER_PLOT
    op_title = "Scatter Plot"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[])

    def init_inner_classes(self):
        self.content = GraphsNodesContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        input_node = self.get_input()
        self.data = input_node.get_node_components()
        if not self.content.generate_graph(input_node, self.data.shape[1]):
            return
        else:
            self.mark_dirty(False)
            self.mark_invalid(False)



@register_node(OP_NODE_LINE_CHART)
class RnxNodeLineChart(RnxNodeBase):
    icon = "icons/line-chart.png"
    op_code = OP_NODE_LINE_CHART
    op_title = "Line Chart"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[])

    def init_inner_classes(self):
        self.content = LineGraphContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        input_node = self.get_input()
        # self.y = input_node.rnx
        # self.score = input_node.score
        # self.previous_method_name = input_node.previous_method
        #
        # self.content.text_rnx.setText(self.content_labels[1] + str(self.score))
        self.content.generate_line_chart(input_node.methods_dict_output)
        self.mark_dirty(False)
        self.mark_invalid(False)


@register_node(OP_NODE_DATA_TABLE)
class RnxNodeDataTable(RnxNodeBase):
    icon = "icons/real_data.png"
    op_code = OP_NODE_DATA_TABLE
    op_title = "Tabla de datos"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])

    def init_inner_classes(self):
        self.content = TableOfDataNode(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        input_node = self.get_input()
        data = input_node.get_node_components()
        self.content.createTable(data)



class MyThread(QThread):
    finished = pyqtSignal(float)

    def __init__(self, node):
        super().__init__()
        self.node = node

    def run(self) -> None:
        self.node.content.run()
        self.finished.emit(0.1)


