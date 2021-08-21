from PyQt5.QtWidgets import QFormLayout, QVBoxLayout
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from rnx_node_editor.node_widget_node import NodeWidgetContent
from pandas import  DataFrame

class TableOfDataNode(NodeWidgetContent):


    def init_ui(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.table = QTableWidget()

    def createTable(self, data):

        components = data
        if type(components) == DataFrame:
            components = components.values

        self.table.setRowCount(components.shape[0])
        self.table.setColumnCount(components.shape[1])
        self.table.setLayout(QVBoxLayout())
        self.table.clearContents()
        for i in range(components.shape[0]):
            for j in range(components.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(components[i, j])))

        self.table.move(0, 0)

        self.table.show()


