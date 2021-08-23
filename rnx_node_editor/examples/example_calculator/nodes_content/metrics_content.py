from PyQt5.QtWidgets import QFormLayout, QLabel
from rnx_node_editor.node_widget_node import NodeWidgetContent
from rnx.score_rnx import ScoreRnx
from rnx_node_editor.utils import dump_exception


class RnxMetricContent(NodeWidgetContent):
    def init_ui(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.text_method = QLabel(self.node.content_labels[0])
        self.text_rnx = QLabel(self.node.content_labels[1])
        self.layout.addRow(self.text_method, self.text_rnx)

    def run(self):
        input_nodes = self.node.get_inputs()  # it give us a list of two lists
        # method_descriptor = {'title': '', 'components': [], 'score': 0.0, 'rnx': []}
        if not input_nodes[0] and not input_nodes[1]:
            self.node.gr_node.setToolTip("There are missing inputs")
            self.node.mark_invalid()
            return

        for node in input_nodes[-1]:
            self.node.high_data = node.get_node_components()

        for node in input_nodes[0] + input_nodes[-1]:
            if node.is_invalid or node.is_dirty:
                self.node.mark_invalid()
                self.node.gr_node.setToolTip("Puede que uno o más de los nodos conectados, no esté ejecutado")
                return

        # if self.node.high_data is None or self.node.method_data is None:
        #     self.node.gr_node.setToolTip("Input is NaN")
        #     self.node.mark_invalid()
        #     return

        try:
            for node in input_nodes[0]:
                self.rnx = ScoreRnx(self.node.high_data, node.get_node_components())
                self.rnx.run()
                self.node.score = self.rnx.get_rnx()[0]
                self.node.rnx = self.rnx.get_rnx()[1]
                self.node.methods_dict_output.append({'title': node.title,
                                                      'score': self.node.score,
                                                      'rnx': self.node.rnx})

            self.node.mark_invalid(False)
            self.node.mark_dirty(False)
        except Exception as e:
            dump_exception(e)
            self.node.mark_invalid()
