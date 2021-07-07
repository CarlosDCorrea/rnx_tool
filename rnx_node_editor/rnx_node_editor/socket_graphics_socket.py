from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem
from PyQt5.QtGui import QColor, QBrush, QPen, QPainter
from PyQt5.QtCore import QRectF


class SocketGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=1):
        super().__init__(socket.node.gr_node)

        self.socket = socket
        self.radius = 6.0
        self._outline_width = 1.0
        self.socket_type = socket_type
        self.colors = [
            QColor("#FF1807BE"),  # input HDD the output of AD and RD should be the same
            QColor("#FF07C20F"),  # output LDD The input of RNX should be the same
            QColor("#FF05B27B"),  # input graphs
        ]
        self._color_background = self.colors[self.socket_type]
        self._outline_color = QColor("#FF000000")

        self._pen = QPen(self._outline_color)
        self._pen.setWidthF(self._outline_width)
        self._brush = QBrush(self._color_background)

    def __str__(self):
        return "<Socket graphics class %s>..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None) -> None:

        # paint circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        rect_f = QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
        painter.drawEllipse(rect_f)

    def boundingRect(self) -> QRectF:
        return QRectF(
            -self.radius - self._outline_width,
            -self.radius - self._outline_width,
            2 * (self.radius + self._outline_width),
            2 * (self.radius + self._outline_width)
        )
