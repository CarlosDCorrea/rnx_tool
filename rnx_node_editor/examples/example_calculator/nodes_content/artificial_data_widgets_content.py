from PyQt5.QtWidgets import QFormLayout, QComboBox, QLabel
from rnx_node_editor.node_widget_node import NodeWidgetContent
from rnx_node_editor.utils import dump_exception
from examples.example_calculator.data_class.FileSystemDataRepository import FileSystemRepository
from examples.example_calculator.data_class.DataClass import Data
import os


DEBUG = True


class ArtificialDataNodeContent(NodeWidgetContent):
    def init_ui(self):
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.combo_data = QComboBox()

        self.repo = FileSystemRepository()

        self.data_returned = None   # This is the data we will return once the node is executed

        self.is_object = None
        self.state_procces_sphere = False
        self.state_procces_swiss_roll = False
        self.state_procces_toroid = False

        """
        Combo box Data insert
        """
        self.combo_data.addItem("Seleccionar")
        self.combo_data.addItem("Sphere")
        self.combo_data.addItem("Swiss Roll")
        self.combo_data.addItem("Toroid")

        self.combo_data.currentIndexChanged.connect(self.define_object)
        self.combo_data.currentIndexChanged.connect(self.node.on_input_changed)
        #  self.combo_data.activated.connect(self.define_object)  # I think it is not necessary, read Qt docs

        self.text_data = QLabel(self.node.content_labels[0], self)
        self.combo_data.setObjectName(self.node.content_label_obj_names[0])

        self.layout.addRow(self.text_data, self.combo_data)

    def define_object(self):
        object = self.combo_data.currentIndex()
        self.is_object = object
        if DEBUG:
            print("CURRENT OBJECT::", self.is_object)

    def run(self):
        self.HD = None
        self.current_directory = os.getcwd()
        if not self.is_object:
            if DEBUG:
                print("CURRENT OBJECT", self.is_object, "you should load a data set")

            self.node.mark_invalid()
            self.node.gr_node.setToolTip(str("Select a data set"))
            self.node.mark_descendents_dirty()
            self.reset_states()

        if self.is_object == 1 and not self.state_procces_sphere:
            if DEBUG:
                print("Loading Sphere...")

            self.load_data("\\data\\esfera.mat", "X")

            self.reset_states()
            self.state_procces_sphere = True

        if self.is_object == 2 and not self.state_procces_swiss_roll:
            if DEBUG:
                print("Loading Swiss Roll...")

            #  Load the data
            self.load_data("\\data\\data_swissroll.mat", "X")

            self.reset_states()
            self.state_procces_swiss_roll = True



        if self.is_object == 3 and not self.state_procces_toroid:
            if DEBUG:
                print("Loading Toroid...")

            self.load_data("\\data\\toroide.mat", "X")

            self.reset_states()
            self.state_procces_toroid = True

        if hasattr(self.HD, 'getComponents'):
            self.data_returned = self.HD.getComponents() if self.HD else None
        else:
            self.data_returned = self.HD

    def get_components(self):
        return self.data_returned

    def reset_states(self):
        self.state_procces_toroid = False
        self.state_procces_sphere = False
        self.state_procces_swiss_roll = False

    def load_data(self, path, label):
        try:
            self.HD: Data = self.repo.load(self.current_directory + path, label)
            self.node.mark_invalid(False)
            self.node.mark_dirty(False)
        except Exception as e:
            dump_exception(e)
