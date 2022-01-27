from PyQt5.QtWidgets import QFormLayout, QLabel
from rnx_node_editor.node_widget_node import NodeWidgetContent
from rnx.score_rnx import ScoreRnx
from rnx_node_editor.utils import dump_exception
from timeit import default_timer as timer

class RnxMetricContent(NodeWidgetContent):
    
    def __init__(self, node):
        super().__init__(node)
        self.node.methods_dict_output = []
        self.nodes_current_executed: [] = []


    # it give us a list of two lists
    # method_descriptor = {'title': '', 'components': [], 'score': 0.0, 'rnx': []}

    def run(self):

        print(self.nodes_current_executed)

        inputs = [ method_nodes, data_node ] = self.node.get_inputs() # this function return  a array with two arrays in it

        if self.connections_are_not_available(inputs):
            return

        if self.nodes_are_not_ready_yet(inputs):
            return

        self.node.mark_invalid(False)
        self.node.mark_dirty()
        self.node.gr_node.setToolTip("Nodo ejecutandose...")

        for node in data_node: # is a array with one data RnxNodeBase object
            self.node.high_data = node.get_node_components()

        # Esta variable representa los nodos que se van a ejecutar
        nodes = None

        # si ya hay evaluaciones de nodos listas, extraer nodos que no han sido ejecutados previamente
        if  not self.is_empty(self.nodes_current_executed):
            nodes = self.extract_nodes(self.nodes_current_executed, method_nodes)

        else:
            nodes = method_nodes

        print("Nodos que se ejecutaran =>", self.createListId(nodes))

        # Si no hay nodos para ejecutar termina el proceso
        if self.is_empty(nodes):
            self.update_current_list(self.createListId(method_nodes))
            self.update_dict_output()
            self.node.mark_invalid(False)
            self.node.mark_dirty(False)
            return

        self.execute_nodes(nodes)

        # actualizar lista de los nodos ejecutados
        self.update_current_list(self.createListId(method_nodes))
        #actualizar dicionario
        self.update_dict_output()


    def connections_are_not_available(self, input_nodes):
        flag = False
        if not input_nodes[0] or not input_nodes[-1]:
            self.node.gr_node.setToolTip("There are missing inputs")
            self.node.mark_invalid()
            flag = True

        return  flag

    def nodes_are_not_ready_yet(self, input_nodes):
        flag = False
        for node in input_nodes[0] + input_nodes[-1]:
            print("Node =>",node, " Is invalid =>", node.is_invalid(), "Is dirty =>",node.is_dirty())

            if node.is_invalid() or node.is_dirty():
                self.node.mark_invalid()
                self.node.gr_node.setToolTip("Puede que uno o más de los nodos conectados, no esté ejecutado")
                flag = True
        return flag

    def execute_nodes(self, input_nodes):

        try:
            for node in input_nodes:
                self.rnx = ScoreRnx(self.node.high_data, node.get_node_components())
                start = timer()
                self.rnx.run()
                print(f"Nodo {id(node)} Evaluado en =>, {timer() - start:0.4f} sec")
                self.node.score = self.rnx.get_rnx()[0]
                self.node.rnx = self.rnx.get_rnx()[1]
                self.node.methods_dict_output.append({'id': id(node),
                                                'title': node.title,
                                              'score': self.node.score,
                                              'rnx': self.node.rnx})
                #añadir id de nodos ejecutados en este ciclo

                self.node.mark_invalid(False)
                self.node.mark_dirty(False)
                self.node.gr_node.setToolTip("")

        except Exception as e:
            dump_exception(e)
            self.node.mark_invalid()

    def extract_nodes(self, nodes_executed, input_nodes):

        extract = []

        for i in input_nodes:
            if not self.element_in_list(id(i), nodes_executed):
                extract.append(i)

        return  extract

    def element_in_list(self, e, list):
        flag = False
        for i in list:
            if i == e:
                flag = True
        return flag

    def is_empty(self, list):
        if list:
            return False
        else:
            return True

    def createListId(self, list):
        n = []
        for i in list:
            n.append(id(i))

        return  n

    def update_dict_output(self):

        n = []

        for i in self.node.methods_dict_output:
            if self.element_in_list(i["id"], self.nodes_current_executed):
                n.append(i)

        self.node.methods_dict_output = n

    def update_current_list(self, list):

        self.nodes_current_executed = list







