from PyQt5.QtWidgets import (QGraphicsItem,
                             QGraphicsTextItem,
                             QStyleOptionGraphicsItem,
                             QGraphicsProxyWidget,
                             QGraphicsSceneMouseEvent)
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QPen, QColor, QBrush, QMouseEvent
from PyQt5.QtCore import Qt, QRectF


DEBUG = False


class NodeGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content
        self.title_item = QGraphicsTextItem(self)
        self._color_title = Qt.white
        self._font_title = QFont("ububtu", 10)
        self.title_height = 24.0

        self.gr_content = QGraphicsProxyWidget(self)

        self.width = 180
        self.height = 240

        self._padding_title = 20.0

        self.edge_size = 10.0

        self._pen = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        # init title
        self.init_title()
        self.title = self.node.title

        """
        init dockets: the sockets are the inputs and outputs of our node
        """
        self.init_sockets()

        """
        init content: the content is the container for the widgets
        that our node will have
        """
        self.init_content()

        self.init_ui()

        self.was_moved = False

    """
    BoundingRect can be interpreted as the area of the node
    in that way when we click in that area the node is selected, and therefore
    it can be movable, etc. 
    """
    def boundingRect(self) -> QRectF:
        return QRectF(0,
                      0,
                      self.width,
                      self.height).normalized()

    def init_ui(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def init_title(self):
        self.title_item.setDefaultTextColor(self._color_title)
        self.title_item.node = self.node
        self.title_item.setFont(self._font_title)
        self.title_item.setPos(self._padding_title, 0)

    def init_sockets(self):
        pass

    def init_content(self):
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2 * self.edge_size, self.height - 2 * self.edge_size - self.title_height)
        self.gr_content.setWidget(self.content)

    """
    QMaouseEvent test: i will to test if when clicking the rifht botton in the graphicsnode
    it will accept that event
    """
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            """
            La idea para posibles mejoras, es que al realizar este evento, aparezca
            un menú para el nodo, en donde se pueda configurar y ejecutar
            """
            # print("se ha precionado el click derecho sobre el nodo")
            pass

    """
    When we move the node it return that signal, it can be usefull when 
    updating the positions of our edges
    """
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)
        # self.node.update_connection_edges()
        """
        when we select different nodes at the time and move them, the edges are not being updated
        because we are calling the update edge only we move an specific node
        """
        for node in self.scene().scene.nodes:
            if node.gr_node.isSelected():
                node.update_connection_edges()

        self.was_moved = True

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)

        if self.was_moved:
            self.was_moved = False
            self.node.scene.history.store_history("node moved", set_modified=True)

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    @property
    def padding_title(self):
        return self._padding_title

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None) -> None:
        """
        title
        """
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size,
                           self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        """
        content 
        """
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height,
                                    self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        """
        outline
        """
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        # podemos preguntar si el item ha sido seleccionado
        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
