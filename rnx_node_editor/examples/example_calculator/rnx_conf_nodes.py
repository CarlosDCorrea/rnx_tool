from rnx_node_base import *
from rnx_conf import *
from nodes_content.methods_content import *
from nodes_content.artificial_data_widgets_content import ArtificialDataNodeContent
from nodes_content.real_data_widget_content import RealDataNodeContent
from nodes_content.metrics_content import RnxMetricContent
from nodes_content.graphs_nodes_content import *
from PyQt5.QtCore import QRunnable, QThreadPool
from PyQt5.QtCore import pyqtSignal


DEBUG = True


@register_node(OP_NODE_PCA)
class RnxNodePCA(RnxNodeBase):
    icon = "icons/linear-regression.png"
    op_code = OP_NODE_PCA
    op_title = "PCA"
    content_labels = ["Dimensions", ""]
    content_label_obj_names = ["rnx_node_dimensions", ""]

    def init_inner_classes(self):
        self.content = NonParametricMethodsContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.high_data = None
        self.low_data = None
        return self.content.run()


@register_node(OP_NODE_MDS)
class RnxNodeMDS(RnxNodeBase):
    icon = "icons/mds.png"
    op_code = OP_NODE_MDS
    op_title = "MDS"
    content_labels = ["Dimensions", ""]
    content_label_obj_names = ["rnx_node_dimensions", ""]

    def init_inner_classes(self):
        self.content = NonParametricMethodsContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.high_data = None
        self.low_data = None
        return self.content.run()


@register_node(OP_NODE_KPCA)
class RnxNodeKPCA(RnxNodeBase):
    icon = ""
    op_code = OP_NODE_KPCA
    op_title = "KPCA"
    content_labels = ["Dimensions", "Neighbours"]
    content_label_obj_names = ["rnx_node_dimensions", "rnx_node_neighbours"]

    def init_inner_classes(self):
        self.content = NonParametricMethodsContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.high_data = None
        self.low_data = None
        return self.content.run()


@register_node(OP_NODE_LLE)
class RnxNodeLLE(RnxNodeBase):
    icon = "icons/graph.png"
    op_code = OP_NODE_LLE
    op_title = "LLE"
    content_labels = ["Dimensions", "Neighbours"]
    content_label_obj_names = ["rnx_node_dimensions", "rnx_node_neighbours"]

    def init_inner_classes(self):
        self.content = ParametricMethodsContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.high_data = None
        self.low_data = None
        return self.content.run()


@register_node(OP_NODE_LE)
class RnxNodeLE(RnxNodeBase):
    icon = ""
    op_code = OP_NODE_LE
    op_title = "LE"
    content_labels = ["Dimensions", "Neighbours"]
    content_label_obj_names = ["rnx_node_dimensions", "rnx_node_neighbours"]

    def init_inner_classes(self):
        self.content = ParametricMethodsContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.high_data = None
        self.low_data = None
        return self.content.run()


@register_node(OP_NODE_ISOMAP)
class RnxNodeISOMAP(RnxNodeBase):
    icon = "icons/isomap.png"
    op_code = OP_NODE_ISOMAP
    op_title = "ISOMAP"
    content_labels = ["Dimensions", "Neighbours"]
    content_label_obj_names = ["rnx_node_dimensions", "rnx_node_neighbours"]

    def init_inner_classes(self):
        self.content = ParametricMethodsContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        self.high_data = None
        self.low_data = None
        return self.content.run()


@register_node(OP_NODE_RNX)
class RnxNodeRNX(RnxNodeBase):
    icon = ""
    op_code = OP_NODE_RNX
    op_title = "RNX"
    content_labels = ["Method:", "RNX:"]
    content_label_obj_names = ["rnx_node_method", "rnx_node_rnx"]

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 0], outputs=[2])
        self.high_data = None
        self.method_data = None
        self.score = None
        self.rnx = None
        self.previous_method = None

    def init_inner_classes(self):
        self.content = RnxMetricContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        # self.thread = QThread()

        worker = WorkerThread(self)

        # self.worker.moveToThread(self.thread)

        # self.thread.started.connect(self.worker.run)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)

        # self.thread.start()
        self.thread_pool = QThreadPool()
        self.thread_pool.start(worker)


@register_node(OP_NODE_LDA)
class RnxNodeLDA(RnxNodeBase):
    icon = ""
    op_code = OP_NODE_LDA
    op_title = "LDA"
    content_labels = ["", ""]
    content_label_obj_names = ["", ""]

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])


@register_node(OP_NODE_ARTIFICIAL_DATA)
class RnxNodeArtificialData(RnxNodeBase):
    icon = "icons/sphere.png"
    op_code = OP_NODE_ARTIFICIAL_DATA
    op_title = "Artificial Data"
    content_labels = ["Data: ", ""]
    content_label_obj_names = ["rnx_node_art_data", ""]

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])

    def init_inner_classes(self):
        self.content = ArtificialDataNodeContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        return self.content.run()

    def get_node_components(self):
        self.value = self.content.get_components()
        return self.value


@register_node(OP_NODE_REAL_DATA)
class RnxNodeRealData(RnxNodeBase):
    icon = "icons/real_data.png"
    op_code = OP_NODE_REAL_DATA
    op_title = "Real Data"
    content_labels = ["Select data set ", ""]
    content_label_obj_names = ["rnx_node_real_data", ""]

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])

    def init_inner_classes(self):
        self.content = RealDataNodeContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)


@register_node(OP_NODE_SCATTER_PLOT)
class RnxNodeScatterPlot(RnxNodeBase):
    icon = "icons/Scatter-plot.png"
    op_code = OP_NODE_SCATTER_PLOT
    op_title = "Scatter Plot"
    content_labels = ["points: ", "dimensions: "]
    content_label_obj_names = ["rnx_node_points", ""]

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[])

    def init_inner_classes(self):
        self.content = GraphsNodesContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        input_node = self.get_input()
        self.data = input_node.get_node_components() if input_node.title == "Artificial Data" else input_node.low_data
        self.content.text_points.setText(self.content_labels[0] + str(self.data.shape[0]))
        self.content.text_dimensions.setText(self.content_labels[1] + str(self.data.shape[1]))

        self.content.generate_graph(self.data.shape[1])
        self.mark_dirty(False)
        self.mark_invalid(False)


@register_node(OP_NODE_LINE_CHART)
class RnxNodeLineChart(RnxNodeBase):
    icon = "icons/line-chart.png"
    op_code = OP_NODE_LINE_CHART
    op_title = "Line Chart"
    content_labels = ["method: ", "Score: "]
    content_label_obj_names = ["rnx_node_method", ""]

    def __init__(self, scene):
        super().__init__(scene, inputs=[2], outputs=[])

    def init_inner_classes(self):
        self.content = LineGraphContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def run(self):
        input_node = self.get_input()
        self.y = input_node.rnx
        self.score = input_node.score
        self.previous_method_name = input_node.previous_method

        self.content.text_rnx.setText(self.content_labels[1] + str(self.score))
        self.content.generate_line_chart(self)
        self.mark_dirty(False)
        self.mark_invalid(False)


class WorkerThread(QRunnable):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, node):
        super().__init__()
        self.node = node

    def run(self) -> None:
        self.node.content.run()
