from .socket_graphics_socket import SocketGraphicsSocket
from .node_serializable import Serializable


LEFT_TOP = 1
LEFT_CENTER = 2
LEFT_BOT = 3
RIGHT_TOP = 4
RIGHT_BOT = 5
RIGHT_CENTER = 6


class Socket(Serializable):
    def __init__(self, node,
                 index=0,
                 position=LEFT_TOP,
                 socket_type=1,
                 multi_edges=True,
                 count_on_this_node_site=1,
                 is_input=False):
        super().__init__()
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type
        self.count_on_this_node_site = count_on_this_node_site
        self.is_input = is_input
        self.is_output = not self.is_input
        # print(f"the Socket is being created with index: {self.index}, position: {self.position}, "
        #      f"and its node is {self.node.title}")
        self.gr_socket = SocketGraphicsSocket(self, self.socket_type)
        self.set_socket_position()

        self.edges = []
        self.is_multi_edges = multi_edges

    def __str__(self):
        return "<socket main class %s %s>..%s>" % ("ME" if self.is_multi_edges else "SE", hex(id(self))[2:5], hex(id(self))[-3:])

    def set_socket_position(self):
        self.gr_socket.setPos(*self.node.get_socket_position(self.index, self.position, self.count_on_this_node_site))

    def get_socket_pos(self):
        # print(f"GSP: {self.index}, {self.position}, node: {self.node}")
        res = self.node.get_socket_position(self.index, self.position, self.count_on_this_node_site)
        # print(f"res: {res}")
        return res

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_all_edges(self):
        while self.edges:
            edge = self.edges.pop(0)
            edge.remove()

        # self.edges.clear()

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
        else:
            print("The edge", edge, "you are trying to remove from socket", self, "is not in the list")

    # def has_edge(self):
    #    return self.edges

    def determine_multi_edges(self, data):
        if 'multi_edges' in data:
            return data['multi_edges']
        else:
            return data['position'] in (RIGHT_BOT, RIGHT_TOP)

    def serialize(self):
        return {
            'id': self.id,
            'index': self.index,
            'multi_edges': self.is_multi_edges,
            'position': self.position,
            'socket_type': self.socket_type
        }

    def deserialize(self, data, dictionary=None, restore_id=True):
        if dictionary is None:
            dictionary = {}

        if restore_id:
            self.id = data['id']

        self.is_multi_edges = self.determine_multi_edges(data)
        dictionary[data['id']] = self
        return True
