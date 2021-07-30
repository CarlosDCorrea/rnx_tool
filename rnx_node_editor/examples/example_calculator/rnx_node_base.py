from PyQt5.QtWidgets import QStyleOptionGraphicsItem
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QRectF
from rnx_node_editor.node_node import Node
from rnx_node_editor.node_widget_node import NodeWidgetContent
from rnx_node_editor.node_graphics_node import NodeGraphicsNode
from rnx_node_editor.node_socket import LEFT_CENTER, RIGHT_CENTER
from rnx_node_editor.utils import dump_exception


class RnxNodeBase(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_labels = ["Dimensions", "Neighbours"]
    content_label_obj_names = ["rnx_node_dimensions", "rnx_node_neighbours"]

    def __init__(self, scene, inputs=None, outputs=None):
        if outputs is None:
            outputs = [1]
        if inputs is None:
            inputs = [0]

        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None


        # All the nodes will have a dirty mark by default
        self.mark_dirty()

    def init_inner_classes(self):
        self.content = NodeContent(self)
        self.gr_node = NodeBaseGraphicsNode(self)

    def init_settings(self):
        super().init_settings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def eval_implementation(self):
        return 123

    def eval(self):
        if not (self.is_dirty() and self.is_invalid()):
            print("_> returning cached %s value:" % self.__class__.__name__, self.value)

        try:
            val = self.eval_implementation()
            return val
        except ValueError as e:
            self.mark_invalid()
            self.gr_node.setToolTip(str(e))
            self.mark_descendents_dirty()
        except Exception as e:
            self.mark_invalid()
            self.gr_node.setToolTip(str(e))
            dump_exception(e)

    def on_input_changed(self, new_edge):
        print("%s::__onInputChanged %s" % (self.__class__.__name__, self.title))
        self.mark_dirty()
        self.mark_descendents_dirty()
        self.high_data = None

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, dictionary=None, restore_id=True):
        res = super().deserialize(data, dictionary, restore_id)
        print("DESEREALIZE:: Node %s" % self.__class__.__name__, "res", res)
        return res


class NodeContent(NodeWidgetContent):
    """The nodes are inheriting from it do not delete"""
    pass


class NodeBaseGraphicsNode(NodeGraphicsNode):
    def init_geometry(self):
        super().init_geometry()
        self.width = 170
        self.height = 100
        self._padding_title_horizontal = 20.0
        self._padding_title_vertical = 20.0
        self.edge_roundness = 20
        self.edge_padding = 0

    def init_assets(self):
        super().init_assets()
        self.icons = QImage("icons/status_icons.png")

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None) -> None:
        super().paint(painter, option, widget)

        offset = 24.0
        if self.node.is_dirty():
            offset = 0.0
        if self.node.is_invalid():
            offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )

