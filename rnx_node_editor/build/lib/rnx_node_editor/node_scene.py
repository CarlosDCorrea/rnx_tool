from .node_graphics_scene import SceneGraphicsScene
from .node_serializable import Serializable
from .node_node import Node
from .node_edge import Edge
from .node_scene_history import SceneHistory
from .node_scene_clipboard import SceneClipboard
import json
DEBUG = False


class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.scene_width = 64000
        self.scene_height = 64000

        self._has_been_modified = False
        self._has_been_modified_listeners = []

        self.scene = SceneGraphicsScene(self)
        self.init_ui()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

    @property
    def has_been_modified(self):
        return False
        # return self._has_been_modified

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

    def init_ui(self):
        self.scene.set_scene(self.scene_width, self.scene_height)

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
            data = json.loads(raw_data) # The encodings argument is not necesary
            self.deserialize(data)

            self.has_been_modified = False

    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())

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
            Node(self).deserialize(node_data, dictionary, restore_id)

        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, dictionary, restore_id)

        return True
