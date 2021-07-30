from PyQt5.QtWidgets import QFormLayout, QLabel, QPushButton
from rnx_node_editor.node_widget_node import NodeWidgetContent


class RealDataNodeContent(NodeWidgetContent):
    def init_ui(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.text_real_data = QLabel(self.node.content_labels[0])
        self.button_open_data_set = QPushButton("...")

        self.button_open_data_set.setObjectName(self.node.content_label_obj_names[0])

        self.layout.addRow(self.text_real_data, self.button_open_data_set)
