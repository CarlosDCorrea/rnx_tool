from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem
from PyQt5.QtGui import QPen, QPainter, QPolygonF, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QPointF


class CutLineGraphicsCutLine(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_points = []
        
        self._pen = QPen(Qt.white)
        self._pen.setWidthF(2.0)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self) -> QRectF:
        return self.shape().boundingRect()

    def shape(self) -> QPainterPath:
        polygon = QPolygonF(self.line_points)

        if len(self.line_points) > 1:
            path = QPainterPath(self.line_points[0])
            for point in self.line_points[1:]:
                path.lineTo(point)
        else:
            path = QPainterPath(QPointF(0, 0))
            path.lineTo(QPointF(1, 1))

        return path

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None) -> None:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)

        polygon = QPolygonF(self.line_points)
        painter.drawPolyline(polygon)
