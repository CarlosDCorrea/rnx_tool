from PyQt5.QtWidgets import QFormLayout, QLabel, QPushButton
from rnx_node_editor.node_widget_node import NodeWidgetContent
from examples.example_calculator.data_class.FileSystemDataRepository import FileSystemRepository
from pandas import read_csv, read_excel
from rnx_node_editor.utils import dump_exception
from examples.example_calculator.data_class.DataClass import Data

class RealDataNodeContent(NodeWidgetContent):

    def __init__(self, node, config):
        super().__init__(node)
        self.config = config
        self.data_returned: Data = None
        self.repo = FileSystemRepository()

    def run(self):

        if self.is_not_a_valid_file(self.config.extention):
            return
        try:
            self.data_returned = self.repo.load(self.config.path)
            self.node.mark_invalid(False)
            self.node.mark_dirty(False)
        except Exception as e:
            dump_exception(e)


    def get_components(self):
        return self.data_returned

    def update(self):
        self.data_returned = None
        self.node.markdirty(True)

    def is_not_a_valid_file(self, extention):
        flag = False
        if extention != ("csv" or "xlsx" or "mat"):
            self.node.mark_dirty(True)
            self.node.gr_node.setToolTip("The file is not supported")
            return True

        return flag