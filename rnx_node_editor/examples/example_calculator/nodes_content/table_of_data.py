from PyQt5.QtWidgets import QFormLayout, QVBoxLayout
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from rnx_node_editor.node_widget_node import NodeWidgetContent


class TableOfDataNode(NodeWidgetContent):


    def init_ui(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.table = QTableWidget()

    def createTable(self, data):

        self.table.setRowCount(data.shape[0])
        self.table.setColumnCount(data.shape[1])
        self.table.setLayout(QVBoxLayout())
        self.table.clearContents()

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(data[i, j])))

        self.table.move(0, 0)

        self.table.show()



