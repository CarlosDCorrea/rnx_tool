from PyQt5.QtWidgets import QGraphicsPathItem, QStyleOptionGraphicsItem, QGraphicsSceneMouseEvent
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF
from math import fabs
from .node_socket import RIGHT_BOT, RIGHT_TOP, LEFT_BOT, LEFT_TOP


EDGE_CP_ROUNDNESS = 100


class EdgeGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._last_selected_state = False
        self.pos_source = [0, 0]
        self.pos_target = [200, -100]

        self._pen = QPen(QColor("#FFCD853F"))
        self._pen_selected = QPen(QColor("#FF1E90FF"))
        self._pen_dragging = QPen(QColor("#FFCD853F"))

        self.init_assets()
        self.init_ui()

    def init_ui(self):
        self.setFlag(QGraphicsPathItem.ItemIsSelectable)
        self.setZValue(-1)

    def init_assets(self):
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_dragging.setWidthF(2.0)
        self._pen_dragging.setStyle(Qt.DashLine)

    def on_selected(self):
        #  print("EDGE selected")
        self.edge.scene.scene.item_selected.emit()


    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        if self._last_selected_state != self.isSelected():
            self.edge.scene.reset_last_selected_state()
            self._last_selected_state = self.isSelected()
            self.on_selected()

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_target(self, x, y):
        self.pos_target = [x, y]

    def boundingRect(self) -> QRectF:
        return self.shape().boundingRect()

    def shape(self) -> QPainterPath:
        return self.calc_path()

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None) -> None:
        self.setPath(self.calc_path())

        if not self.edge.target:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def calc_path(self):
        """
        This method will handle drawing path from point A to B
        :return:
        """
        raise NotImplemented("This method has to be override in a child class")

    def intersect_with(self, p1, p2):
        cut_path = QPainterPath(p1)
        cut_path.lineTo(p2)
        path = self.calc_path()
        return cut_path.intersects(path)


class EdgeGraphicsEdgeDirect(EdgeGraphicsEdge):
    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.lineTo(self.pos_target[0], self.pos_target[1])
        return path


class EdgeGraphicsEdgeCurve(EdgeGraphicsEdge):
    def calc_path(self):
        s = self.pos_source
        t = self.pos_target
        dist = (t[0] - s[0]) * 0.5

        cpx_source = +dist
        cpx_target = -dist
        cpy_source = 0
        cpy_target = 0

        if self.edge.source:
            start_socket_pos = self.edge.source.position

            # if s[0] > t[0] and (start_socket_pos in (LEFT_TOP, LEFT_BOT)

            if s[0] > t[0] and start_socket_pos in (RIGHT_TOP, RIGHT_BOT) or (s[0] < t[0] and start_socket_pos in (LEFT_TOP, LEFT_BOT)):

                cpx_source *= -1
                cpx_target *= -1

                cpy_target = ((s[1] - t[1]) /
                              fabs((s[1] - t[1]) if (s[1] - t[1]) else 0.000001)
                              ) * EDGE_CP_ROUNDNESS

                cpy_source = ((t[1] - s[1]) /
                              fabs((t[1] - s[1]) if (t[1] - s[1]) else 0.000001)
                              ) * EDGE_CP_ROUNDNESS

                """
                my hypothesis is that the bug is being created because of 
                not removing the old edge at all
                """

        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.cubicTo(s[0] + cpx_source, s[1] + cpy_source, t[0] + cpx_target, t[1] + cpy_target, self.pos_target[0], self.pos_target[1])
        return path
