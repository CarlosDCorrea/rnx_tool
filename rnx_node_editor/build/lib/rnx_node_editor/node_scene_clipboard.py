from .edge_graphical_edge import EdgeGraphicsEdge
from .node_node import Node
from .node_edge import Edge


DEBUG = True


class SceneClipboard:
    def __init__(self, scene):
        self.scene = scene

    def serialize_selected(self, delete=False):
        if DEBUG: print("--- COPY TO CLIPBOARD -- ")

        sel_nodes, sel_edges, sel_sockets = [], [], {}

        # sort nodes and edges
        for item in self.scene.scene.selectedItems():
            if hasattr(item, 'node'):
                sel_nodes.append(item.node.serialize())
                for socket in (item.node.inputs + item.node.outputs):
                    sel_sockets[socket.id] = socket
            elif isinstance(item, EdgeGraphicsEdge):
                sel_edges.append(item.edge)

        if DEBUG:
            print("NODES:", sel_nodes)
            print("EDGES:", sel_edges)
            print("SOCKETS", sel_sockets)

        # Remove all edges which are not connected to a node in our list
        for edge in sel_edges:
            if (edge.source.id and edge.target.id) in sel_sockets:
                if DEBUG:
                    print("both sockets copy")
            else:
                if DEBUG:
                    print("one or both socket/s not copy")
                sel_edges.remove(edge)

        if DEBUG:
            print("EDGES_AGAIN", sel_edges)

        edges_final = [edge.serialize() for edge in sel_edges]

        data = {
            'nodes': sel_nodes,
            'edges': edges_final
        }

        print("final data", data)

        # if cut (aka delete) remove selected items
        if delete:
            self.scene.scene.view()[0].delete_item()
            # store our history
            self.scene.history.store_history("Cut out elements from the scene", set_modified=True)

        return data

    def deserialize_from_clipboard(self, data):

        dictionary = {}

        # Calculate mouse pointers
        view = self.scene.scene.views()[0]
        mouse_scene_pos = view.last_scene_mouse_position

        # Calculate selected objects bbox and center
        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        for node_data in data['nodes']:
            x, y = node_data['pos_x'], node_data['pos_y']
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        bbox_center_x = (min_x + max_x) / 2
        bbox_center_y = (min_y + max_y) / 2

        # Calculate the offset of the new created nodes

        offset_x = mouse_scene_pos.x() - bbox_center_x
        offset_y = mouse_scene_pos.y() - bbox_center_y

        # create each node
        for node_data in data['nodes']:
            new_node = Node(self.scene)
            new_node.deserialize(node_data, dictionary, restore_id=False)

            # readjust the new node´s position
            pos = new_node.get_pos()
            new_node.set_pos(pos.x() + offset_x, pos.y() + offset_y)

        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, dictionary, restore_id=False)

        # store history
        self.scene.history.store_history("Pasted elements in scene", set_modified=True)






