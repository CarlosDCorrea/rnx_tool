from .node_graphics_node import NodeGraphicsNode
from .node_widget_node import NodeWidgetContent
from .node_socket import *
from .node_serializable import Serializable
from .utils import dump_exception
"""
this is the base class for nodes, something to keep in mine
is that this class is a complement to the node_graphics_node
which is the graphics part of the nodes, the node_graphics_node module
contains the node view in the gui, and the node_node module, contains the behavior of node itself
"""
DEBUG = True


class Node(Serializable):
    def __init__(self, scene, title="PCA", inputs=None, outputs=None):
        super().__init__()
        self._title = title

        self.scene = scene

        self.init_inner_classes()
        self.init_settings()

        self.title = title

        self.scene.add_node(self)
        self.scene.scene.addItem(self.gr_node)

        self.inputs = []
        self.outputs = []

        self.init_sockets(inputs, outputs)

        self._is_dirty = False
        self._is_invalid = False


    def init_inner_classes(self):
        self.content = NodeWidgetContent(self)  # init of widgets node
        self.gr_node = NodeGraphicsNode(self)

    def init_settings(self):
        self.input_socket_position = LEFT_BOT
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edges = False
        self.output_multi_edges = True

    def init_sockets(self, inputs, outputs, reset=True):
        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []

        if reset:
            #  clear old sockets
            if hasattr(self, 'inputs') and hasattr(self, 'outputs'):
                for socket in (self.inputs + self.outputs):
                    self.scene.scene.removeItem(socket.gr_socket)
                self.inputs = []
                self.outputs = []

        #  Create new sockets
        counter_in = 0
        for item in inputs:
            socket = Socket(node=self,
                            index=counter_in,
                            position=self.input_socket_position,
                            socket_type=item,
                            multi_edges= not self.input_multi_edges if (self.op_title == "RNX" and item == inputs[0])
                                  else self.input_multi_edges,
                            count_on_this_node_site=len(inputs),
                            is_input=True)
            counter_in += 1
            self.inputs.append(socket)

        counter_out = 0
        for item in outputs:
            socket = Socket(node=self,
                            index=counter_out,
                            position=self.output_socket_position,
                            socket_type=item,
                            multi_edges=self.output_multi_edges,
                            count_on_this_node_site=len(outputs),
                            is_input=False)
            counter_out += 1
            self.outputs.append(socket)

    def on_edge_connection_changed(self, new_edge):
        print("%s:: onEdgeConnectionChanged" % self.__class__.__name__, new_edge)

    def on_input_changed(self, new_edge):
        print("%s:: onEdgeInputChanged" % self.__class__.__name__, new_edge + "node_name:", self.title)
        self.mark_descendents_dirty()


    def __str__(self):
        return "<Node %s>..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
            
    def get_socket_position(self, index, position, num_out_of=1):
        x = 0 if position in (LEFT_TOP, LEFT_CENTER, LEFT_BOT) else self.gr_node.width

        if position in (LEFT_BOT, RIGHT_BOT):
            y = self.gr_node.height - self.gr_node.title_height - index * 20
        elif position in (LEFT_CENTER, RIGHT_CENTER):

            num_sockets = num_out_of
            node_height = self.gr_node.height
            top_offset = self.gr_node.title_height + 2 * self.gr_node.padding_title_vertical + self.gr_node.edge_padding
            available_height = node_height - top_offset

            total_height_off_all_sockets = num_sockets * 20

            new_top = available_height - total_height_off_all_sockets

            #  y = top_offset + index * 20 + new_top / 2
            y = top_offset + available_height / 2 + (index - 0.5) * 20
            if num_sockets > 1:
                y -= 20 * (num_sockets - 1) / 2

        elif position in (LEFT_TOP, RIGHT_TOP):
            y = self.gr_node.title_height + self.gr_node.padding_title + index * 25
        else:
            #  this should not happen
            y = 0

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
            print(f"Los edges del socket:{socket} son {socket.edges}")
            for edge in socket.edges[0.]:
                if DEBUG: print("Removing from socket", socket, "Edge", edge)
                edge.remove()
                print("La lista de edges: ", socket.edges)

        if DEBUG: print("Remove gr_scene")
        self.scene.scene.removeItem(self.gr_node)
        self.gr_node = None
        if DEBUG: print("Remove node from the scene")
        self.scene.remove_node(self)
        if DEBUG: print("Proccess node removing complete")

    """Node evaluation"""
    def is_dirty(self):
        return self._is_dirty

    def mark_dirty(self, new_value=True):
        self._is_dirty = new_value
        if self._is_dirty:
            self.on_marked_dirty()

    def on_marked_dirty(self):
        pass

    def mark_children_dirty(self, new_value=True):
        for other_node in self.get_children_node():
            other_node.mark_dirty(new_value)
            other_node.mark_descendents_dirty(new_value)

    def mark_descendents_dirty(self, new_value=True):
        for other_node in self.get_children_node():
            other_node.mark_dirty(new_value)
            other_node.mark_children_dirty(new_value)

    def is_invalid(self):
        return self._is_invalid

    def mark_invalid(self, new_value=True):
        self._is_invalid = new_value
        if self._is_invalid:
            self.on_marked_invalid()

    def mark_children_invalid(self, new_value=True):
        for other_node in self.get_children_node():
            other_node.mark_invalid(new_value)
            other_node.mark_descendents_invalid(new_value)

    def mark_descendents_invalid(self, new_value=True):
        for other_node in self.get_children_node():
            other_node.mark_invalid(new_value)
            other_node.mark_children_invalid(new_value)

    def on_marked_invalid(self):
        pass

    def eval(self):
        self.mark_dirty(False)
        self.mark_invalid(False)
        return 0

    def eval_children(self):
        try:
            for node in self.get_children_node():
                node.eval()
        except Exception as e:
            dump_exception(e)

    """traversing node functions"""

    def get_children_node(self):
        if DEBUG:
            print(self.__class__.__name__)
        if not self.outputs:
            return []

        other_nodes = []
        for index in range(len(self.outputs)):
            for edge in self.outputs[index].edges:
                # print("EDGE::", edge)
                other_node = edge.get_other_socket(self.outputs[index]).node
                other_nodes.append(other_node)
        if DEBUG:
            print(other_nodes)
        return other_nodes

    def get_input(self, index=0):
        try:
            edge = self.inputs[index].edges[0]
            #  this is the node we are connected in
            socket = edge.get_other_socket(self.inputs[index])
            return socket.node # Retorna el node conectado en el socket especificado
        except IndexError as e:
            print(f"EXCEP: trying to get input, but {self.__class__.__name__} do not have one")
            return None
        except Exception as e:
            dump_exception(e)
            return None

    def get_inputs(self):
        other_nodes = []
        try:
            for socket in self.inputs:
                if socket.edges:
                    edge = socket.edges[0]
                    other_socket = edge.get_other_socket(socket)
                    other_nodes.append(other_socket.node)
                else:
                    print("There is not edges connected")
            return other_nodes
        except Exception as e:
            dump_exception(e)

        """ins = []
        for edge in self.inputs[index].edges:
            other_socket = edge.get_other_socket(self.inputs[index])
            ins.append(other_socket.node)
        return ins 
        """

    def get_outputs(self, index=0):
        outs = []
        for edge in self.outputs[index].edges:
            other_socket = edge.get_other_socket(self.outputs[index])
            outs.append(other_socket.node)
        return outs



    """serialization functions"""
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
        try:
            if restore_id:
                self.id = data['id']

            if dictionary is None:
                dictionary = {}

            dictionary[data['id']] = self

            self.set_pos(data['pos_x'], data['pos_y'])

            self.title = data['title']

            data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)
            data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 10000)

            num_inputs = len(data['inputs'])
            num_outputs = len(data['outputs'])

            self.inputs = []
            for socket_data in data['inputs']:
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                    socket_type=socket_data['socket_type'], count_on_this_node_site=num_inputs,
                                    is_input=True)
                new_socket.deserialize(socket_data, dictionary, restore_id)
                self.inputs.append(new_socket)

            self.outputs = []
            for socket_data in data['outputs']:
                new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                    socket_type=socket_data['socket_type'], count_on_this_node_site=num_outputs,
                                    is_input=False)
                new_socket.deserialize(socket_data, dictionary, restore_id)
                self.outputs.append(new_socket)
        except Exception as e:
            dump_exception(e)

        res = self.content.deserialize(data['content'], dictionary)

        return True and res
