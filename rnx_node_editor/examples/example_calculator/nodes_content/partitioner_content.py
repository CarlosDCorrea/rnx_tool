from rnx_node_editor.node_widget_node import NodeWidgetContent

class PartitionerContentNode(NodeWidgetContent):

    def __init__(self, node, config):
        super().__init__(node)
        self.config = config
        self.data_returned = None

    def run(self):

        data = self.node.get_input().get_node_components().copy()
        data.pop(self.config.column)
        self.data_returned = data
        self.node.mark_invalid(False)
        self.node.mark_dirty(False)

    def get_components(self):
        return self.data_returned

    def update(self):
        self.data_returned = None
        self.node.markdirty(True)
