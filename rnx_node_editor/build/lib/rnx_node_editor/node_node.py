from .node_graphics_node import NodeGraphicsNode
from .node_widget_node import NodeWidgetContent
from .node_socket import *
from .node_serializable import Serializable
"""
this is the base class for nodes, something to keep in mine
is that this class is a complement to the node_graphics_node
which is the graphics part of the nodes, the node_graphics_node module
contains the node view in the gui, and the node_node module, contains the behavior of node itself
"""
DEBUG = False


class Node(Serializable):
    def __init__(self, scene, title="Undefined", inputs=None, outputs=None):
        super().__init__()
        self._title = title
        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []
        self.scene = scene

        self.content = NodeWidgetContent(self)  # init of widgets node
        self.gr_node = NodeGraphicsNode(self)

        self.title = title

        self.scene.add_node(self)
        self.scene.scene.addItem(self.gr_node)

        self.inputs = []
        self.outputs = []
        counter_in = 0
        for item in inputs:
            socket = Socket(node=self, index=counter_in, position=LEFT_BOT, socket_type=item, multi_edges=False)
            counter_in += 1
            self.inputs.append(socket)

        counter_out = 0
        for item in outputs:
            socket = Socket(node=self, index=counter_out, position=RIGHT_TOP, socket_type=item)
            counter_out += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s>..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
            
    def get_socket_position(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOT) else self.gr_node.width

        if position in (LEFT_BOT, RIGHT_BOT):
            y = self.gr_node.height - self.gr_node.title_height - index * 20
        else:
            y = self.gr_node.title_height + self.gr_node.padding_title + index * 25

        return [x, y]

    def set_pos(self, x, y):
        self.gr_node.setPos(x, y)

    def get_pos(self):
        return self.gr_node.pos()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):   # Dont sent the same value of the attribute setter
        self._title = value
        self.gr_node.title = self._title
    
    def update_connection_edges(self):
        for socket in self.inputs + self.outputs:
            # if socket.has_edge():
            for edge in socket.edges:
                edge.update_pos()
            else:
                if DEBUG: print("Edge pos is not being updated")

    def remove(self):
        if DEBUG: print("Removing node", self)
        if DEBUG: print("Remove edges of the node")
        for socket in self.inputs + self.outputs:
            # if socket.has_edge():
            for edge in socket.edges:
                if DEBUG: print("Removing from socket", socket, "Edge", edge)
                edge.remove()
        if DEBUG: print("Remove gr_scene")
        self.scene.scene.removeItem(self.gr_node)
        self.gr_node = None
        if DEBUG: print("Remove node from the scene")
        self.scene.remove_node(self)
        if DEBUG: print("Proccess node removing complete")

    def serialize(self):

        inputs, outputs = [], []

        for socket in self.inputs:
            inputs.append(socket.serialize())
        for socket in self.outputs:
            outputs.append(socket.serialize())

        return {
            'id': self.id,
            'title': self.title,
            'pos_x': self.gr_node.scenePos().x(),
            'pos_y': self.gr_node.scenePos().y(),
            'inputs': inputs,
            'outputs': outputs,
            'content': self.content.serialize()
        }

    def deserialize(self, data, dictionary=None, restore_id=True):
        if restore_id:
            self.id = data['id']

        if dictionary is None:
            dictionary = {}

        dictionary[data['id']] = self

        self.set_pos(data['pos_x'], data['pos_y'])

        self.title = data['title']

        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)

        self.inputs = []
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, dictionary, restore_id)
            self.inputs.append(new_socket)

        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, dictionary, restore_id)
            self.outputs.append(new_socket)

        return True
