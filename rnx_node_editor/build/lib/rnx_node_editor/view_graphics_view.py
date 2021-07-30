from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QApplication
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QKeyEvent
from PyQt5.QtCore import QEvent, pyqtSignal

from .socket_graphics_socket import SocketGraphicsSocket
from .edge_graphical_edge import *
from .node_edge import Edge, EDGE_CURVE
from .cutline_graphics_cutline import CutLineGraphicsCutLine

"""
SubGraphicsViewClass 
---
All we do here will affect the graphicsView widget and whatever is inside it
"""

DEBUG = True

# These constant variables are useful to determine if we can drag an edge from a socket
MODE_OFF = 0
MODE_ON = 1
MODE_EDGE_CUTLINE = 2

THRESHOLD = 10  # the drag has to be bigger than the threshold


class ViewQGraphicsView(QGraphicsView):
    scene_pos_changed = pyqtSignal(int, int)

    def __init__(self, scene, parent=None) -> None:
        super().__init__(parent)
        self.scene = scene
        self.zoom_in_factor = 1.25
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [0, 10]
        self.zoom_clamp = True

        self.press_button_pos = [0, 0]

        self.mode = MODE_OFF
        self.cut_line = CutLineGraphicsCutLine()
        self.scene.addItem(self.cut_line)
        self.editing_flag = False

        self.rubber_brand_dragging_rectangle = False

        self.init_ui()

        self.setScene(self.scene)

    def init_ui(self):
        self.setRenderHint(QPainter.Antialiasing or
                           QPainter.HighQualityAntialiasing or
                           QPainter.TextAntialiasing or
                           QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event: QMouseEvent) -> None:
        release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(),
                                    event.screenPos(), Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(release_event)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.LeftButton, event.buttons() or Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fake_event)

    def middleMouseButtonRelease(self, event: QMouseEvent) -> None:
        fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                 Qt.LeftButton, event.buttons() and Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fake_event)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def leftMouseButtonPress(self, event: QMouseEvent) -> None:

        item = self.get_item_at_click(event)

        self.press_button_pos = self.mapToScene(event.pos())

        """
        in some tutorials for the logic expressions the & and | caracters are used
        but it really depends of what python version is being used, to have a common 
        form to code we will use "and", "or" expressions
        """

        if DEBUG: print("LMB on item:", item, "modifier:", self.debug_modifier(event))

        if hasattr(item, 'node') or isinstance(item, EdgeGraphicsEdge) or not item:
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ShiftModifier:
                event.ignore()
                fake_event = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                         Qt.LeftButton, event.buttons() or Qt.LeftButton,
                                         event.modifiers() or Qt.ControlModifier)
                super().mousePressEvent(fake_event)
                return

        # print("el punto inicial es:", self.press_button_pos)

        """
        We are asking if the item that we´ve clicked is a socket, 
        if so, then we can draw edges
        """
        if isinstance(item, SocketGraphicsSocket):
            if self.mode == MODE_OFF:
                self.mode = MODE_ON
                if DEBUG: print("The item is a socket")
                self.edge_drag_start(item)
                return

        if self.mode == MODE_ON:
            res = self.assign_end_socket(item)
            if res:
                return

        if not item:
            modifiers = QApplication.keyboardModifiers()
            if (modifiers and Qt.ControlModifier) == Qt.ControlModifier:
                if DEBUG: print("El modificador control se ha presionado")
                self.mode = MODE_EDGE_CUTLINE
                if DEBUG: print("The mode is ", self.mode)
                fake_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                         Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fake_event)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
            else:
                self.rubber_brand_dragging_rectangle = True

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event: QMouseEvent) -> None:

        item = self.get_item_at_click(event)

        if hasattr(item, 'node') or isinstance(item, EdgeGraphicsEdge) or not item:
            if event.modifiers() and Qt.ShiftModifier:
                event.ignore()
                fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                         Qt.LeftButton, Qt.NoButton,
                                         event.modifiers() or Qt.ControlModifier)
                super().mouseReleaseEvent(fake_event)
                return

        release_button_pos = self.mapToScene(event.pos())
        # print(f"el punto final es {release_button_pos}")
        dist_pos = release_button_pos - self.press_button_pos
        if DEBUG: print(f"The distance of click is {dist_pos}")
        pos_squared = dist_pos.x() ** 2 + dist_pos.y() ** 2

        if self.mode == MODE_ON:
            if pos_squared > THRESHOLD ** 2:
                res = self.assign_end_socket(item)
                if res:
                    return

        if self.mode == MODE_EDGE_CUTLINE:
            self.cut_intersecting_edges()
            self.cut_line.line_points = []
            self.cut_line.update()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_OFF
            return

        # if self.dragMode() == QGraphicsView.RubberBandDrag:
        if self.rubber_brand_dragging_rectangle:
            self.scene.scene.history.store_history("Selected changed")
            self.rubber_brand_dragging_rectangle = False

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event: QMouseEvent) -> None:

        item = self.get_item_at_click(event)

        if DEBUG: print("The right button has been pressed item:", item)

        if isinstance(item, EdgeGraphicsEdgeCurve):
            if DEBUG: print("Right button presses on edge curve:", item.edge,
                            "socket:", item.edge.source, "-->", item.edge.target)

        if isinstance(item, SocketGraphicsSocket):
            if DEBUG: print("Right button pressed on socket:", item.socket, "has edge:", item.socket.edges)

        if not item:
            if DEBUG: print("SCENE")
            if DEBUG: print("Nodes: ")
            for node in self.scene.scene.nodes:
                if DEBUG: print("node object:", node)
            for edge in self.scene.scene.edges:
                if DEBUG: print("edge object:", edge)

        super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mode == MODE_ON:
            pos = self.mapToScene(event.pos())
            self.drag_edge.gr_edge.set_target(pos.x(), pos.y())
            self.drag_edge.gr_edge.update()

        if self.mode == MODE_EDGE_CUTLINE:
            if DEBUG: print("El modo esta en cutline")
            pos = self.mapToScene(event.pos())
            self.cut_line.line_points.append(pos)
            self.cut_line.update()

        self.last_scene_mouse_position = self.mapToScene(event.pos())

        self.scene_pos_changed.emit(
            int(self.last_scene_mouse_position.x()),
            int(self.last_scene_mouse_position.y())
        )

        super().mouseMoveEvent(
            event)  # Algo interesante es que el nodo no puede ser movido si esta linea no se especifica

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if DEBUG: print("Graphics View:: Key Pressed")
        #        modifiers = QApplication.keyboardModifiers()
        #        if event.key() == Qt.Key_Delete:
        #            if not self.editing_flag:
        #                self.delete_item()
        #            else:
        #                super().keyPressEvent(event)
        #        elif event.key() == Qt.Key_S and event.modifiers() and Qt.ControlModifier:
        #            self.scene.scene.save_to_file("graph.json.txt")
        #        elif event.key() == Qt.Key_L and event.modifiers() and Qt.ControlModifier:
        #            self.scene.scene.load_from_file("graph.json.txt")
        #        elif event.key() == Qt.Key_Z and (modifiers and Qt.ControlModifier):
        #            self.scene.scene.history.undo()
        #        elif event.key() == Qt.Key_Y and (modifiers and Qt.ControlModifier):
        #            self.scene.scene.history.redo()
        #        elif event.key() == Qt.Key_H:
        #            if DEBUG: print("HISTORY:: len(%d)" % len(self.scene.scene.history.history_stack),
        #                  " -- Current_step", self.scene.scene.history.history_current_step)
        #
        #            index = 0
        #            for item in self.scene.scene.history.history_stack:
        #                if DEBUG: print("#", index, "--", item['desc'])
        #                index += 1
        #
        #        else:
        super().keyPressEvent(event)

    def cut_intersecting_edges(self):
        for ix in range(len(self.cut_line.line_points) - 1):
            p1 = self.cut_line.line_points[ix]
            p2 = self.cut_line.line_points[ix + 1]

            for edge in self.scene.scene.edges:
                if edge.gr_edge.intersect_with(p1, p2):
                    edge.remove()

        self.scene.scene.history.store_history("Delete cut edges", set_modified=True)

    def delete_item(self):
        for item in self.scene.selectedItems():
            if isinstance(item, EdgeGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

        self.scene.scene.history.store_history("Delete selected items", set_modified=True)

    def debug_modifier(self, event: QMouseEvent):
        out = "Mod: "
        if event.modifiers() and Qt.ShiftModifier:
            out += 'Shift'
        if event.modifiers() and Qt.AltModifier:
            out += 'Alt'
        if event.modifiers() and Qt.ControlModifier:
            out += 'Control'
        return out

    def get_item_at_click(self, event: QMouseEvent) -> QGraphicsItem:
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edge_drag_start(self, item):
        if DEBUG: print("The mode has changed to on")
        if DEBUG: print("assign start socket")
        # self.previous_edge = item.socket.edges
        self.drag_start_socket = item.socket
        #  A partir de aquí es posible que inicie el bug en el programa
        self.drag_edge = Edge(self.scene.scene, item.socket, None, EDGE_CURVE)  # here the drag view is created
        if DEBUG: print("The edge view created", self.drag_edge)

    def assign_end_socket(self, item):
        self.mode = MODE_OFF

        if DEBUG: print("End drag edge")
        self.drag_edge.remove()
        self.drag_edge = None

        if isinstance(item, SocketGraphicsSocket):
            """
            Here we will to solve the previous bug
            """
            if item.socket != self.drag_start_socket:
                # if we release dragging in a socket (other than the beginning socket)
                # if DEBUG: print("the previous edge is:", self.previous_edge)

                # if item.socket.has_edge():
                #    item.socket.edges.remove()

                # for edge in item.socket.edges:
                #    edge.remove()
                if not item.socket.is_multi_edges:
                    item.socket.remove_all_edges()

                if not self.drag_start_socket.is_multi_edges:
                    self.drag_start_socket.remove_all_edges()


                # if DEBUG: print("Assign end socket -->", item.socket)
                # if self.previous_edge:
                #    self.previous_edge.remove()
                #    if DEBUG: print("------------------------\n"
                #                    "The previos edge has being removed")

                # self.drag_edge.source = self.drag_start_socket
                # self.drag_edge.target = item.socket
                # self.drag_edge.source.add_edge(self.drag_edge)
                # self.drag_edge.target.add_edge(self.drag_edge)
                # if DEBUG: print("---------------------------")
                # if DEBUG: print("The start and end socket have being resigned")
                # self.drag_edge.update_pos()

                new_edge = Edge(self.scene.scene, self.drag_start_socket, item.socket, type_edge=EDGE_CURVE)
                if DEBUG:
                    print("Edge Created:", new_edge, "source:", new_edge.source, "target:", new_edge.target)

                self.scene.scene.history.store_history("Edge Created by dragging", set_modified=True)
                return True

        # if DEBUG: print("About to set socket to previous edge ", self.previous_edge)
        # if self.previous_edge:
        #    self.previous_edge.source.edges = self.previous_edge
        if DEBUG: print("The edge has been destroyed")

        return False

    def wheelEvent(self, event: QWheelEvent) -> None:
        """
        Room factor calculation
        """
        zoom_out_factor = 1 / self.zoom_in_factor

        # Calculate zoom
        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step

        clamped = False
        if self.zoom < self.zoom_range[0]:
            self.zoom, clamped = self.zoom_range[0], True

        if self.zoom > self.zoom_range[1]:
            self.zoom, clamped = self.zoom_range[1], True

        if not clamped or self.zoom_clamp is False:
            self.scale(zoom_factor, zoom_factor)
