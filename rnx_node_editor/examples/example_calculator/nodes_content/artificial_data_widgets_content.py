from PyQt5.QtWidgets import QFormLayout, QComboBox, QLabel
from rnx_node_editor.node_widget_node import NodeWidgetContent
from rnx_node_editor.utils import dump_exception
from examples.example_calculator.data_class.FileSystemDataRepository import FileSystemRepository
from examples.example_calculator.data_class.DataClass import Data
from examples.example_calculator.config.ArtificialDataConfig import TypesConfig
import os


DEBUG = True


class ArtificialDataNodeContent(NodeWidgetContent):

    def __init__(self, node, config):
        super().__init__(node)
        self.repo = FileSystemRepository()
        self.config = config
        self.data_returned = None  # This is the data we will return once the node is executed

    def run(self):
        self.HD = None
        self.current_directory = os.getcwd()

        if self.config.status == TypesConfig.Select.value:
            if DEBUG:
                print("you should load a data set")

            self.node.mark_invalid()
            self.node.gr_node.setToolTip(str("Select a data set"))
            self.node.mark_descendents_dirty()

        if self.config.status == TypesConfig.Sphere.value:
            if DEBUG:
                print("Loading Sphere...")

            self.load_data("\\data\\esfera.mat", "X")

        if self.config.status == TypesConfig.Swiss_Roll.value:
            if DEBUG:
                print("Loading Swiss Roll...")

            #  Load the data
            self.load_data("\\data\\data_swissroll.mat", "X")


        if self.config.status == TypesConfig.Toroid.value:
            if DEBUG:
                print("Loading Toroid...")

            self.load_data("\\data\\toroide.mat", "X")


        if hasattr(self.HD, 'getComponents'):
            self.data_returned = self.HD.getComponents() if self.HD else None
        else:
            self.data_returned = self.HD

        print(self.HD)

    def get_components(self):
        return self.data_returned

    def load_data(self, path, label):
        try:
            self.HD: Data = self.repo.load(self.current_directory + path, label)
            self.node.mark_invalid(False)
            self.node.mark_dirty(False)
        except Exception as e:
            dump_exception(e)


    def update(self):
        self.data_returned = None
        self.node.mark_dirty(True)


