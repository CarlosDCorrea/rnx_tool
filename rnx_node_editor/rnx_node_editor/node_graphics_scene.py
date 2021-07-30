from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneDragDropEvent
from PyQt5.QtCore import QRectF, QLine, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen
import math


class SceneGraphicsScene(QGraphicsScene):
    item_selected = pyqtSignal()
    item_deselected = pyqtSignal()

    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene
        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self._grid_size = 20
        self._grid_square = 5

        self.setBackgroundBrush(self._color_background)

    def dragMoveEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        """
        The drag event wont be allowed until dragModeEvent is override
        """
        pass

    def set_scene(self, width, height):
        """
            This method help us to create a grid in our scene
        """
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)

        """
        Grid
        """
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self._grid_size)
        first_top = top - (top % self._grid_size)

        """
        Compute lines to be draw
        """
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self._grid_size):
            if x % (self._grid_size * self._grid_square) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self._grid_size):
            if y % (self._grid_size * self._grid_square) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))


        """
        Draw lines
        """
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)