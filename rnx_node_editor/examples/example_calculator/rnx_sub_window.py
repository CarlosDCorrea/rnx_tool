from PyQt5.QtWidgets import QGraphicsProxyWidget, QMenu, QAction
from PyQt5.QtGui import QCloseEvent, QPixmap, QDropEvent, QContextMenuEvent, QIcon
from PyQt5.QtCore import QDataStream, QIODevice, Qt
from rnx_conf import *
from rnx_node_editor.rnx_ne_widget import RnxNodeEditorWidget, Node
from rnx_node_editor.utils import dump_exception
from rnx_node_editor.node_edge import EDGE_CURVE, EDGE_DIRECT


DEBUG_CONTEXT = False


class RnxSubWindow(RnxNodeEditorWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.set_title()

        self.init_new_node_actions()

        self.gr_scene.add_has_been_modified_listener(self.set_title)
        self.gr_scene.add_drag_enter_listener(self.on_drag_enter)
        self.gr_scene.add_drop_listener(self.on_drop)
        self.gr_scene.set_node_class_selector(self.get_node_class_from_data)

        self._close_event_listeners = []

    def get_node_class_from_data(self, data):
        if 'op_code' not in data:
            return Node
        return get_class_from_op_code(data['op_code'])

    def init_new_node_actions(self):
        self.node_actions = {}
        keys = list(RNX_NODES.keys())
        keys.sort()
        for key in keys:
            node = RNX_NODES[key]
            self.node_actions[node.op_code] = QAction(QIcon(node.icon), node.op_title)
            self.node_actions[node.op_code].setData(node.op_code)

    def init_nodes_context_menu(self):
        context_menu_new_nodes = QMenu(self)
        keys = list(RNX_NODES.keys())
        keys.sort()
        for key in keys:
            context_menu_new_nodes.addAction(self.node_actions[key])
        return context_menu_new_nodes

    def set_title(self):
        self.setWindowTitle(self.user_friendly_current_file())

    def add_close_event_listeners(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event: QCloseEvent) -> None:
        for callback in self._close_event_listeners:
            callback(self, event)

    def on_drag_enter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def on_drop(self, event: QDropEvent):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event_data = event.mimeData().data(LISTBOX_MIMETYPE)
            data_stream = QDataStream(event_data, QIODevice.ReadOnly)
            pixi = QPixmap()
            data_stream >> pixi
            op_code = data_stream.readInt()
            text = data_stream.readQString()

            mouse_pos = event.pos()
            scene_pos = self.gr_scene.scene.views()[0].mapToScene(mouse_pos)

            if DEBUG_CONTEXT:
                print("got dropped: [%d] %s" % (op_code, text), "mouse:", mouse_pos, "scene:", scene_pos)

            try:
                node = get_class_from_op_code(op_code)(self.gr_scene)
                node.set_pos(scene_pos.x(), scene_pos.y())
                self.gr_scene.history.store_history("Create Node %s" % node.__class__.__name__)
            except Exception as e:
                print(e)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            print("... drop ignored, bad format %s" % LISTBOX_MIMETYPE)
            event.ignore()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        try:
            item = self.gr_scene.get_item(event.pos())
            if DEBUG_CONTEXT:
                print(item)

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.handle_node_context_menu(event)
            elif hasattr(item, 'edge'):
                self.handle_edge_context_menu(event)
            else:
                self.handle_new_node_context_menu(event)

            return super().contextMenuEvent(event)
        except Exception as e:
            dump_exception(e)

    def handle_node_context_menu(self, event):
        if DEBUG_CONTEXT:
            print("NODE:: Context Menu")
        #  my form

        context_menu_node = QMenu()
        run_act = context_menu_node.addAction("Run")
        setting = context_menu_node.addAction("Configurations")
        action = context_menu_node.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.gr_scene.get_item(event.pos())

        if type(item) == QGraphicsProxyWidget:
            item = item.widget()

        if hasattr(item, 'node'):
            selected = item.node

        if hasattr(item, 'socket'):
            selected = item.socket.node

        if DEBUG_CONTEXT:
            print("SELECTED:: ", selected.__class__.__name__)
            print("SELECTED GNODE::", selected.gr_node)


        if selected and action == run_act:
            selected.run()

        if selected and action == setting:
            selected.configure()




    def handle_edge_context_menu(self, event):
        if DEBUG_CONTEXT:
            print("EDGE:: Context Menu")
        context_menu_edge = QMenu(self)
        curve_act = context_menu_edge.addAction("Curve Edge")
        direct_act = context_menu_edge.addAction("Direct Edge")
        action = context_menu_edge.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.gr_scene.get_item(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge
            if DEBUG_CONTEXT:
                print("SELECTED:: ", selected)

        if selected and action == curve_act:
            selected.type_edge = EDGE_CURVE
        if selected and action == direct_act:
            selected.type_edge = EDGE_DIRECT

    def handle_new_node_context_menu(self, event):
        if DEBUG_CONTEXT:
            print("NEW NODE:: Context Menu")

        context_menu_new_node = self.init_nodes_context_menu()
        action = context_menu_new_node.exec_(self.mapToGlobal(event.pos()))

        if action:
            new_rnx_node = get_class_from_op_code(action.data())(self.gr_scene)
            scene_pos = self.gr_scene.get_view().mapToScene(event.pos())
            new_rnx_node.set_pos(scene_pos.x(), scene_pos.y())
            if DEBUG_CONTEXT:
                print("SELECTED NODE::", new_rnx_node)