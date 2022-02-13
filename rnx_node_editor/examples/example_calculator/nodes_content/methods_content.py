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


class NonParametricMethodsContent(NodeWidgetContent):
    def __init__(self, node, config):
        super().__init__(node)
        self.config = config
        self.result = None

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

    def reduce_dimensions(self, method, data):
        dimensions_value = self.config.d
        self.node.method = method(dimensions_value)
        print(method)
        return self.node.method.spectrum(data)

    def run(self):
        input_node = self.node.get_input()
        self.node.mark_dirty()
        if not input_node:
            self.node.gr_node.setToolTip("No hay ningún input conectado")
            self.node.mark_invalid()
            return

        if input_node.title not in self.node.available_nodes:
            self.node.mark_invalid()
            self.node.gr_node.setToolTip("El input conectado no es válido")
            return

        high_data = input_node.get_node_components()

        if high_data is None:
            self.node.gr_node.setToolTip("No hay datos en alta dimensión cargados")
            self.node.mark_invalid()
            return

        try:
            if self.node.title == 'PCA':
                self.apply_reduction(PCA, high_data)
            if self.node.title == 'MDS':
                self.apply_reduction(MDS, high_data)
            if self.node.title == 'KPCA':
                self.apply_reduction(KPCA, high_data)

        except Exception as e:
            dump_exception(e)
            self.node.mark_invalid()
            self.node.gr_node.setToolTip("El número de dimensiones debe ser menor a %d"
                                         % self.node.high_data.shape[1])

    def apply_reduction(self, method, data):
        self.result = self.reduce_dimensions(method, data)
        print(self.result)
        self.node.mark_invalid(False)
        self.node.mark_dirty(False)

    def update(self):
        self.node.mark_dirty()


class ParametricMethodsContent(NodeWidgetContent):
    def __init__(self, node, config):
        super().__init__(node)
        self.config = config
        self.result = None

    def reduce_dimensions(self, method, data):
        dimensions_value = self.config.d
        neighbours_value = self.config.n
        self.node.method = method(dimensions_value, neighbours_value)
        return self.node.method.spectrum(data)

    def run(self):
        input_node = self.node.get_input()
        self.node.mark_dirty()
        if not input_node:
            self.node.gr_node.setToolTip("No hay inputs conectados")
            self.node.mark_invalid()
            return

        if input_node.title not in self.node.available_nodes:
            self.node.mark_invalid()
            self.node.gr_node.setToolTip("El input conectado no es válido")
            return

        high_data = input_node.get_node_components()

        if high_data is None:
            self.node.gr_node.setToolTip("Los datos en alta dimensión no han sido cargados")
            self.node.mark_invalid()
            return

        try:
            if self.node.title == 'LE':
                self.apply_reduction(LE, high_data)
            if self.node.title == 'ISOMAP':
                print("executing ISOMAP")
                self.apply_reduction(ISOMAP, high_data)
            if self.node.title == 'LLE':
                self.apply_reduction(LLE, high_data)

        except Exception as e:
            dump_exception(e)
            self.node.mark_invalid()
            self.node.gr_node.setToolTip("The number of dimensions must be lower than %d"
                                         % self.node.high_data.shape[1])

    def apply_reduction(self, method, data):
        self.result = self.reduce_dimensions(method, data)
        self.node.mark_invalid(False)
        self.node.mark_dirty(False)

    def update(self):
        self.node.mark_dirty(True)
