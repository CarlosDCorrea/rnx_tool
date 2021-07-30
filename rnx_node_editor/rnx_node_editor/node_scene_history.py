from .edge_graphical_edge import EdgeGraphicsEdge
from rnx_node_editor.utils import dump_exception


DEBUG = False


class SceneHistory:
    def __init__(self, scene):
        self.scene = scene

        self.clear()
        self.history_limit = 32

        self._history_modified_listeners = []

    def clear(self):
        self.history_stack = []
        self.history_current_step = -1

    def store_initial_history_stamp(self):
        self.store_history("Initial history stamp")

    def can_undo(self):
        return self.history_current_step > 0

    def undo(self) -> None:
        if self.can_undo():
            self.history_current_step -= 1
            self.restore_history()
            self.scene.has_been_modified = True

    def can_redo(self):
        return self.history_current_step + 1 < len(self.history_stack)

    def redo(self):
        if self.can_redo():
            self.history_current_step += 1
            self.restore_history()
            self.scene.has_been_modified = True

    def add_history_modified_listeners(self, callback):
        self._history_modified_listeners.append(callback)

    def restore_history(self):
        if DEBUG: print("Restoring history ... current_step: @%d" % self.history_current_step,
                        "(%d)" % len(self.history_stack))
        self.restore_history_stamp(self.history_stack[self.history_current_step])

        for callback in self._history_modified_listeners:
            callback()

    def store_history(self, desc, set_modified=False):
        if set_modified:
            self.scene.has_been_modified = True
        if DEBUG: print("Storing history", '"%s"' % desc,
                        "... current_step: @%d" % self.history_current_step,
                        "(%d)" % len(self.history_stack))

        if self.history_current_step + 1 < len(self.history_stack):
            self.history_stack.pop(-1)

        if self.history_current_step + 1 >= self.history_limit:
            self.history_stack.pop(0)
            self.history_current_step -= 1

        history = self.create_history_stamp(desc)
        self.history_stack.append(history)
        self.history_current_step += 1
        if DEBUG: print(" --- setting step to:", self.history_current_step)

        #  Always trigger history modified (for i.eg update_edit_menu)
        for callback in self._history_modified_listeners:
            callback()

    def create_history_stamp(self, desc):
        sel_obj = {
            'nodes': [],
            'edges': []
        }

        for item in self.scene.scene.selectedItems():
            if hasattr(item, 'node'):
                sel_obj['nodes'].append(item.node.id)
            elif isinstance(item, EdgeGraphicsEdge):
                sel_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj
        }

        return history_stamp

    def restore_history_stamp(self, history_stamp):
        if DEBUG: print("RHS::", history_stamp['desc'])

        try:
            self.scene.deserialize(history_stamp['snapshot'])

            # restore selection
            for edge_id in history_stamp['selection']['edges']:
                for edge in self.scene.edges:
                    if edge.id == edge_id:
                        edge.gr_edge.setSelected(True)

            for node_id in history_stamp['selection']['nodes']:
                for node in self.scene.nodes:
                    if node.id == node_id:
                        node.gr_node.setSelected(True)
        except Exception as e:
            dump_exception(e)

