from PyQt5.QtWidgets import QFormLayout, QLabel, QPushButton
from rnx_node_editor.node_widget_node import NodeWidgetContent
from examples.example_calculator.data_class.DataClass import Data
from pandas import read_csv, read_excel

class RealDataNodeContent(NodeWidgetContent):

    def __init__(self, node, config):
        super().__init__(node)
        self.config = config
        self.data_returned = None

    def run(self):
        self.HD = None
        print(self.config.extention)
        if self.config.extention != ("csv" or "xlsx" or "mat") : # Como es ?
            self.node.mark_dirty(True)
            print("Is here")
            return

        if self.config.extention == "csv":
            self.HD = read_csv(self.config.path)
            print(self.HD)
        if self.config.extention == "xlsx":
            self.HD = read_excel(self.config.path)
            print(self.HD)


    def get_components(self):
        return self.data_returned

    def update(self):
        self.node.markdirty(True)
