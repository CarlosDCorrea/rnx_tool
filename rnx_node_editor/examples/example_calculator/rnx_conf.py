LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_PCA = 1
OP_NODE_MDS = 2
OP_NODE_LLE = 3
OP_NODE_LE = 4
OP_NODE_ISOMAP = 5
OP_NODE_KPCA = 6
OP_NODE_RNX = 7
OP_NODE_LDA = 8
OP_NODE_ARTIFICIAL_DATA = 9
OP_NODE_REAL_DATA = 10
OP_NODE_PARTITIONER = 11
OP_NODE_SCATTER_PLOT = 12
OP_NODE_LINE_CHART = 13
OP_NODE_DATA_TABLE = 14


########################################################################

RNX_NODES = {

}


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


def register_node_now(op_code, class_reference):
    if op_code in RNX_NODES:
        raise InvalidNodeRegistration("Duplicated node registration of %s, There "
                                      "already %s" % (op_code, RNX_NODES[op_code]))

    RNX_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator


def get_class_from_op_code(op_code):
    if op_code not in RNX_NODES:
        raise OpCodeNotRegistered("OpCode %d not registered" % op_code)
    return RNX_NODES[op_code]
