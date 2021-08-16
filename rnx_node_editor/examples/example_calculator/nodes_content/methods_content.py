from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIntValidator
from rnx_node_editor.utils import dump_exception
from rnx_node_editor.node_widget_node import NodeWidgetContent
from dimensionality_reduction_methods.pca import PCA
from dimensionality_reduction_methods.mds import MDS
from dimensionality_reduction_methods.kpca import KPCA
from dimensionality_reduction_methods.le import LE
from dimensionality_reduction_methods.isomap import ISOMAP
from dimensionality_reduction_methods.lle import LLE
from views.dialog_window import Dialog

class NonParametricMethodsContent(NodeWidgetContent):

    def __init__(self, node, config):
        super().__init__(node)
        self.config = config


    def serialize(self):
        res = super().serialize()
        res['value'] = self.config.d
        return res

    def deserialize(self, data, dictionary=None):
        res = super().deserialize(data, dictionary)
        try:
            value = data['value']
            self.config.d = int(value)
            return True and res
        except Exception as e:
            dump_exception(e)
        return res

    def reduce_dimensions(self, method):
        dimensions_value = self.config.d
        self.node.method = method(dimensions_value)

        return self.node.method.spectrum(self.node.high_data)

    def run(self):
        input_node = self.node.get_input()
        if not input_node:
            self.node.gr_node.setToolTip("There is not input connected")
            self.node.mark_invalid()
            return

        self.node.high_data = input_node.get_node_components()

        if self.node.high_data is None:
            self.node.gr_node.setToolTip("Input is NaN")
            self.node.mark_invalid()
            return

        try:
            if self.node.title == 'PCA':
                print("Executing PCA")
                self.apply_reduction(PCA)
            if self.node.title == 'MDS':
                print("Executing MDS")
                self.apply_reduction(MDS)
            if self.node.title == 'KPCA':
                print("Executing KPCA")
                self.apply_reduction(KPCA)

            return self.node.low_data
        except Exception as e:
            dump_exception(e)
            self.node.mark_invalid()

            self.node.gr_node.setToolTip("The number of dimensions must be lower than %d"
                                         % self.node.high_data.shape[1])

    def apply_reduction(self, method):
        self.node.low_data = self.reduce_dimensions(method)
        self.node.mark_invalid(False)
        self.node.mark_dirty(False)

    def update(self):
        self.node.mark_dirty(True)


class ParametricMethodsContent(NodeWidgetContent):

    def __init__(self, node, config):
        super().__init__(node)
        self.config = config

    def reduce_dimensions(self, method):
        dimensions_value = self.config.d
        neighbours_value = self.config.n
        self.node.method = method(dimensions_value, neighbours_value)
        return self.node.method.spectrum(self.node.high_data)

    def run(self):

        input_node = self.node.get_input()
        if not input_node:
            self.node.gr_node.setToolTip("There is not input connected")
            self.node.mark_invalid()
            return

        self.node.high_data = input_node.get_node_components()

        if self.node.high_data is None:
            self.node.gr_node.setToolTip("Input is NaN")
            self.node.mark_invalid()
            return

        try:
            if self.node.title == 'LE':
                self.apply_reduction(LE)
            if self.node.title == 'ISOMAP':
                print("executing ISOMAP")
                self.apply_reduction(ISOMAP)
            if self.node.title == 'LLE':
                self.apply_reduction(LLE)

            return self.node.low_data
        except Exception as e:
            dump_exception(e)
            self.node.mark_invalid()
            self.node.gr_node.setToolTip("The number of dimensions must be lower than %d"
                                         % self.node.high_data.shape[1])

    def apply_reduction(self, method):
        self.node.low_data = self.reduce_dimensions(method)
        self.node.mark_invalid(False)
        self.node.mark_dirty(False)

    def update(self):
        self.node.mark_dirty(True)
