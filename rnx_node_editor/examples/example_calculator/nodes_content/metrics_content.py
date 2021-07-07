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
        input_nodes = self.node.get_inputs()
        if not input_nodes or len(input_nodes) == 1:
            self.node.gr_node.setToolTip("There are missing inputs")
            self.node.mark_invalid()
            return

        methods_nodes = ['PCA', 'MDS', 'KPCA', 'LE', 'LLE', 'ISOMAP']

        for node in input_nodes:
            if node.title in methods_nodes:
                self.node.method_data = node.low_data
                self.node.previous_method = node.title
            else:
                self.node.high_data = node.get_node_components()

        if self.node.high_data is None or self.node.method_data is None:
            self.node.gr_node.setToolTip("Input is NaN")
            self.node.mark_invalid()
            return

        try:
            self.rnx = ScoreRnx(self.node.high_data, self.node.method_data)
            self.rnx.run()
            self.node.score = self.rnx.get_rnx()[0]
            self.node.rnx = self.rnx.get_rnx()[1]
            self.node.mark_invalid(False)
            self.node.mark_dirty(False)
        except Exception as e:
            dump_exception(e)
            self.node.mark_invalid()
