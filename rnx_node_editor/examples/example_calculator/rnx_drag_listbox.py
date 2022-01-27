from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtGui import QPixmap, QIcon, QDrag
from PyQt5.QtCore import (QSize, Qt, QByteArray, QDataStream, QMimeData, QIODevice,
                          QPoint)
from rnx_conf import *


METHODS = 1
METRICS = 2
DATA = 3
VISUALS = 4


class DragListWidget(QListWidget):
    def __init__(self, items=METHODS):
        super().__init__()
        self.items = items

        self.init_ui()

    def init_ui(self):
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)

        if self.items == METHODS:
            self.add_my_items_methods()
        if self.items == METRICS:
            self.add_my_items_metrics()
        if self.items == DATA:
            self.add_my_items_data()
        if self.items == VISUALS:
            self.add_my_items_visuals()

    def add_my_items_methods(self):
        self.init_items_listbox(0, 6)

    def add_my_items_metrics(self):
        self.init_items_listbox(6, 7)

    def add_my_items_data(self):
        self.init_items_listbox(7, 10)

    def add_my_items_visuals(self):
        self.init_items_listbox(10, None)

    def add_my_item(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self)   # can be (icon, text, parent, <int>type)
        pixi = QPixmap(icon if icon else ".")
        item.setIcon(QIcon(pixi))
        item.setSizeHint(QSize(32, 32))

        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        #  Setup data
        item.setData(Qt.UserRole, pixi)
        item.setData(Qt.UserRole + 1, op_code)

    def init_items_listbox(self, start, end):
        keys = list(RNX_NODES.keys())
        keys = sorted(keys[start:end])
        for key in keys:
            node = get_class_from_op_code(key)
            self.add_my_item(node.op_title, node.icon, node.op_code)

    def startDrag(self, *args, **kwargs) -> None:

        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)

            pixi = QPixmap(item.data(Qt.UserRole))

            item_data = QByteArray()
            data_stream = QDataStream(item_data, QIODevice.WriteOnly)
            data_stream << pixi
            data_stream.writeInt(op_code)
            data_stream.writeQString(item.text())

            mime_data = QMimeData()
            mime_data.setData(LISTBOX_MIMETYPE, item_data)

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setHotSpot(QPoint(pixi.width() / 2, pixi.height() / 2))
            drag.setPixmap(pixi)
            drag.exec_(Qt.MoveAction)

        except Exception as e:
            print(e)


