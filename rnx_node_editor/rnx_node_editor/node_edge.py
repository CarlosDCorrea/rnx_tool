from .edge_graphical_edge import EdgeGraphicsEdgeDirect, EdgeGraphicsEdgeCurve
from .node_serializable import Serializable
from rnx_node_editor.utils import dump_exception


EDGE_DIRECT = 1
EDGE_CURVE = 2

DEBUG = False


class Edge(Serializable):
    def __init__(self, scene, source=None, target=None, type_edge=1):
        super().__init__()
        self.scene = scene

        self._source = None
        self._target = None

        self.data = None

        self.source = source
        self.target = target
        self.type_edge = type_edge

        self.scene.add_edge(self)

    def __str__(self):
        return "<Edge %s>..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def get_other_socket(self, knob_socket):
        return self.source if knob_socket == self.target else self.target

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        if self._source:
            self._source.remove_edge(self)

        self._source = value
        if self.source:
            self.source.add_edge(self)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        if self.target:
            self._target.remove_edge(self)
        self._target = value
        if self.target:
            self.target.add_edge(self)

    @property
    def type_edge(self):
        return self._type_edge

    @type_edge.setter
    def type_edge(self, value):
        if hasattr(self, 'gr_edge') and self.gr_edge:
            self.scene.scene.removeItem(self.gr_edge)

        self._type_edge = value
        if self.type_edge == EDGE_DIRECT:
            self.gr_edge = EdgeGraphicsEdgeDirect(self)
        elif self.type_edge == EDGE_CURVE:
            self.gr_edge = EdgeGraphicsEdgeCurve(self)
        else:
            self.gr_edge = EdgeGraphicsEdgeCurve(self)

        self.scene.scene.addItem(self.gr_edge)

        if self.source:
            self.update_pos()

    def update_pos(self):
        source_pos = self.source.get_socket_pos()
        source_pos[0] += self.source.node.gr_node.pos().x()
        source_pos[1] += self.source.node.gr_node.pos().y()
        if DEBUG: print("the x source position is", source_pos[0])
        if DEBUG: print("the y source position is", source_pos[1])
        self.gr_edge.set_source(*source_pos)
        if self.target:
            target_pos = self.target.get_socket_pos()
            target_pos[0] += self.target.node.gr_node.pos().x()
            target_pos[1] += self.target.node.gr_node.pos().y()
            self.gr_edge.set_target(*target_pos)
        else:
            self.gr_edge.set_target(*source_pos)
        """
        when we start dragging the edge the target is in some random position
        to fix that we will say that when we start dragging the edge
        the end position will be the source position.
        """

        if DEBUG: print(f"Source: {self.source}")
        if DEBUG: print(f"target: {self.target}")
        self.gr_edge.update()

    def remove_from_socket(self):
        self.source = None
        self.target = None

    def remove(self):
        old_sockets = [self.source, self.target]

        if DEBUG: print("Removing edge")
        if DEBUG: print("Removing edge from all sockets")
        self.remove_from_socket()
        if DEBUG: print("Remove gr_edge")
        self.scene.scene.removeItem(self.gr_edge)
        self.gr_edge = None
        if DEBUG: print("Remove edge from scene")

        """
        when we select for example, two nodes and two edges that are connected to those
        nodes, we are deleting those edges from the node, but also we are deleting 
        those edges by themself, but keeping in mind that the edges have already deleted
        it raises an exception error 'the item x is no in list' in that case we should ask first
        if the edge is in the scene if so, we delete it, otherwise we dont do anything
        """
        try:
            if self in self.scene.edges:
                self.scene.remove_edge(self)
        except Exception as e:
            if DEBUG: print("Exception", e, "Type of error", type(e))

        if DEBUG: print("Edge remove complete")

        # notify nodes from old sockets
        try:
            for socket in old_sockets:
                if socket and socket.node:
                    socket.node.on_edge_connection_changed(self)
                    if socket.is_input:
                        socket.node.on_input_changed(self)
        except Exception as e:
            dump_exception(e)

    def serialize(self):
        return {
            'id': self.id,
            'edge_type': self.type_edge,
            'start': self.source.id,
            'end': self.target.id
        }

    def deserialize(self, data, dictionary=None, restore_id=True):
        if dictionary is None:
            dictionary = {}

        if restore_id:
            self.id = data['id']

        self.source = dictionary[data['start']]
        self.target = dictionary[data['end']]
        self.type_edge = data['edge_type']
        return True
