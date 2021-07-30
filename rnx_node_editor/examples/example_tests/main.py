from PyQt5.QtWidgets import QApplication
import inspect
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


from rnx_node_editor.rnx_node_window import RnxNodeWindow
from rnx_node_editor.utils import load_style_sheet


"""
Here the app will be run
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RnxNodeWindow()
    window.rnx_node_editor.add_node()
    module_path = os.path.dirname(inspect.getfile(window.__class__))
    load_style_sheet(os.path.join(module_path, 'qss/node_style.qss'))

    sys.exit(app.exec())
