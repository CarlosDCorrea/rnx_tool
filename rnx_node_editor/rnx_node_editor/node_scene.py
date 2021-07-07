from .node_graphics_scene import SceneGraphicsScene
from .node_serializable import Serializable
from .node_node import Node
from .node_edge import Edge
from .node_scene_history import SceneHistory
from .node_scene_clipboard import SceneClipboard
import json
import os
DEBUG = False


class InvalidFile(Exception):
    pass


class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.scene_width = 64000
        self.scene_height = 64000

        self._has_been_modified = False
        self._last_selected_item = []

        #  @TODO read about listeners in pyqt5 what are they functionlity
        self._has_been_modified_listeners = []
        self._item_selected_listener = []
        self._item_deselected_listener = []

        #  here we can store callback for retrieving the class for Node
        self.node_class_selector = None

        self.scene = SceneGraphicsScene(self)
        self.init_ui()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

        self.scene.item_selected.connect(self.on_item_selected)
        self.scene.item_deselected.connect(self.on_item_deselected)

    def init_ui(self):
        self.scene.set_scene(self.scene_width, self.scene_height)

    def get_view(self):
        return self.scene.views()[0]

    def get_item(self, pos):
        return self.get_view().itemAt(pos)


    def on_item_selected(self):
        current_selected_items = self.get_selected_items()
        if current_selected_items != self._last_selected_item:
            self._last_selected_item = current_selected_items
            self.history.store_history("Selection Changed")
            for callback in self._item_selected_listener:
                callback()

    def on_item_deselected(self):
        self.reset_last_selected_state()
        if self._last_selected_item:
            self._last_selected_item = []
            self.history.store_history("Deselected everything")
            for callback in self._item_deselected_listener:
                callback()

    def is_modified(self):
        return self.has_been_modified

    def get_selected_items(self):
        return self.scene.selectedItems()

    @property
    def has_been_modified(self):
        return self._has_been_modified

    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            # Call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value

    def add_has_been_modified_listener(self, callback):
        self._has_been_modified_listeners.append(callback)

    """Functions helper listeners"""
    def add_item_selected_listener(self, callback):
        self._item_selected_listener.append(callback)

    def add_item_deselected_listener(self, callback):
        self._item_deselected_listener.append(callback)

    def add_drag_enter_listener(self, callback):
        self.get_view().add_drag_enter_listener(callback)

    def add_drop_listener(self, callback):
        self.get_view().add_drop_listener(callback)

    def reset_last_selected_state(self):
        for node in self.nodes:
            node.gr_node._last_selected_state = False

        for edge in self.edges:
            edge.gr_edge._last_selected_state = False

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
        else:
            print("The node", node, "you are trying to remove from scene", self, "is not in the list")

    def remove_edge(self, edge):
        self.edges.remove(edge)
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("The edge", edge, "you are trying to remove from scene", self, "is not in the list")

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.has_been_modified = False

    def save_to_file(self, file_name):
        with open(file_name, "w") as file:
            file.write(json.dumps(self.serialize(), indent=4))
            if DEBUG: print(f"{file_name} has being saved")
            self.has_been_modified = False

    def load_from_file(self, file_name):
        with open(file_name, "r") as file:
            raw_data = file.read()
            try:
                data = json.loads(raw_data)  # The encodings argument is not necessary
                self.deserialize(data)

                self.has_been_modified = False
            except json.JSONDecodeError:
                raise InvalidFile(f"{os.path.basename(file_name)} is not a valid json file")
            except Exception as e:
                print(e)

    def set_node_class_selector(self, class_selecting_function):
        """ When the function get_node_class_selector is set, we can use different Node classes """
        self.node_class_selector = class_selecting_function

    def get_node_class_from_data(self, data):
        return Node if not self.node_class_selector else self.node_class_selector(data)

    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes:
            nodes.append(node.serialize())
        for edge in self.edges:
            edges.append(edge.serialize())

        return {
            'id': self.id,
            'scene_width': self.scene_width,
            'scene_height': self.scene_height,
            'nodes': nodes,
            'edges': edges
        }

    def deserialize(self, data, dictionary=None, restore_id=True):
        if DEBUG: print(f"deserializing {data}...")
        self.clear()

        if dictionary is None:
            dictionary = {}

        if restore_id:
            self.id = data['id']

        # Create nodes
        for node_data in data['nodes']:
            self.get_node_class_from_data(node_data)(self).deserialize(node_data, dictionary, restore_id)

        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, dictionary, restore_id)

        return True
