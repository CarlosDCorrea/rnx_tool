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
            QColor("#FF0000FF"),  # input components
            QColor("#FFB22222"),  # output PCA
            QColor("#FFFF8C00"),  # input neighbours
            QColor("#FF20B2AA"),  # output KPCA
            QColor("#FF4B0082"),  # output MDS
            QColor("#FF008080"),  # output ISOMAP
            QColor("#FFFFD700"),  # RNX
            QColor("#FF9400D3"),  # output Artificial Data
            QColor("#FF00FF00")   # output Real data
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
