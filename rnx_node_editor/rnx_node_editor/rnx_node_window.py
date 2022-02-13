from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QLabel, QApplication, QMessageBox
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import QSettings, QPoint, QSize
from .rnx_ne_widget import RnxNodeEditorWidget

import json
import os


class RnxNodeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name_company = "Universidad_Cesmag"
        self.name_product = "Node_Editor"
        self.setWindowIcon(QtGui.QIcon('../examples/example_calculator/icons/rnx.png'))
        self.status_mouse_pos = None
        self.init_ui()

    def create_status_bar(self):
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.rnx_node_editor.view.scene_pos_changed.connect(self.on_scene_pos_changed)

    def init_ui(self):
        self.create_actions()

        # Init menu
        self.create_menus()

        self.rnx_node_editor = RnxNodeEditorWidget(self)
        self.rnx_node_editor.gr_scene.add_has_been_modified_listener(self.set_title)
        self.setCentralWidget(self.rnx_node_editor)

        # status bar
        self.create_status_bar()

        # Set windows properties
        self.setGeometry(200, 200, 800, 600)
        self.set_title()
        self.show()

    def create_actions(self):
        self.act_new = QAction('Nuevo', self, shortcut='Ctrl+N', statusTip='Create new project', triggered=self.on_file_new)
        self.act_open = QAction('Abrir', self, shortcut='Ctrl+O', statusTip='Open file', triggered=self.on_file_open)
        self.act_save = QAction('Guardar', self, shortcut='Ctrl+S', statusTip='Save project', triggered=self.on_file_save)
        self.act_save_as = QAction('Guardar como...', self, shortcut='Ctrl+Shift+S', statusTip='Save project as...', triggered=self.on_file_save_as)
        self.act_exit = QAction('Salir', self, shortcut='Ctrl+Q', statusTip='Exit', triggered=self.close_app)
        self.act_undo = QAction('Undo', self, shortcut='Ctrl+Z', statusTip='Undo last', triggered=self.on_edit_undo)
        self.act_redo = QAction('Redo', self, shortcut='Ctrl+Y', statusTip='Redo last', triggered=self.on_edit_redo)
        self.act_cut = QAction('Cut', self, shortcut='Ctrl+X', statusTip='Cut to clipboard', triggered=self.on_edit_cut)
        self.act_copy = QAction('Copy', self, shortcut='Ctrl+C', statusTip='Copy to clipboard', triggered=self.on_edit_copy)
        self.act_paste = QAction('Paste', self, shortcut='Ctrl+V', statusTip='Paste to clipboard', triggered=self.on_edit_paste)
        self.act_delete = QAction('Delete', self, shortcut='Del', statusTip='Delete selected item', triggered=self.on_edit_delete)

    def create_menus(self):
        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu("Archivo")

        self.file_menu.addAction(self.act_new)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.act_open)
        self.file_menu.addAction(self.act_save)
        self.file_menu.addAction(self.act_save_as)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.act_exit)

        self.edit_menu = menu_bar.addMenu("Editar")
        self.edit_menu.addAction(self.act_undo)
        self.edit_menu.addAction(self.act_redo)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.act_cut)
        self.edit_menu.addAction(self.act_copy)
        self.edit_menu.addAction(self.act_paste)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.act_delete)

    def set_title(self):
        title = "Rnx Node Editor -"
        title += self.get_current_rnx_node_editor_widget().user_friendly_current_file()

        self.setWindowTitle(title)

    def on_scene_pos_changed(self, x, y):
        self.status_mouse_pos.setText("Scene pos: [%d, %d]" % (x, y))

    def on_file_new(self):
        if self.may_be_save():
            self.get_current_rnx_node_editor_widget().gr_scene.clear()
            self.get_current_rnx_node_editor_widget().file_name = None
            self.set_title()

    def on_file_open(self):
        if self.may_be_save():
            file_name, _ = QFileDialog.getOpenFileName(self, "Open project from file")
            if not file_name:
                return

            if os.path.isfile(file_name):
                self.get_current_rnx_node_editor_widget().file_load(file_name)
                self.get_current_rnx_node_editor_widget().file_name = file_name
                self.set_title()

    def on_file_save(self):
        current_rnx_node_editor = self.get_current_rnx_node_editor_widget()
        if current_rnx_node_editor:
            if not current_rnx_node_editor.is_file_name_set():
                return self.on_file_save_as()

            current_rnx_node_editor.file_save()
            # support for mdi app
            if hasattr(current_rnx_node_editor, 'set_title'):
                current_rnx_node_editor.set_title()
            else:
                self.set_title()

            self.statusBar().showMessage("Successfully saved: %s" % current_rnx_node_editor.file_name, 5000)
            return True

    def on_file_save_as(self):
        current_rnx_node_editor = self.get_current_rnx_node_editor_widget()
        if current_rnx_node_editor:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save project to file")
            if not file_name:
                return False

            current_rnx_node_editor.file_save(file_name)

            # support for mdi app
            if hasattr(current_rnx_node_editor, 'set_title'):
                current_rnx_node_editor.set_title()
            else:
                self.set_title()
            self.statusBar().showMessage("Successfully saved as %s" % current_rnx_node_editor.file_name, 5000)
            return True

    def is_modified(self):
        return self.get_current_rnx_node_editor_widget().gr_scene.is_modified()

    def get_current_rnx_node_editor_widget(self):
        return self.centralWidget()

    def may_be_save(self):
        if not self.is_modified():
            return True

        # The second parameter is a label which is white, and therefore in the style file it has been changed
        res = QMessageBox.warning(self, "Estas por perder tu progreso",
                                  "El proyecto tiene cambios sin guardar \n ¿Te gustaría guardarlos?",
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if res == QMessageBox.Save:
            return self.on_file_save()
        elif res == QMessageBox.Cancel:
            return False
        return True

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.may_be_save():
            event.accept()
        else:
            event.ignore()

    def close_app(self):
        print("closing app...")

    def on_edit_undo(self):
        if self.get_current_rnx_node_editor_widget():
            self.get_current_rnx_node_editor_widget().gr_scene.history.undo()

    def on_edit_redo(self):
        if self.get_current_rnx_node_editor_widget():
            self.get_current_rnx_node_editor_widget().gr_scene.history.redo()

    def on_edit_delete(self):
        if self.get_current_rnx_node_editor_widget():
            self.get_current_rnx_node_editor_widget().gr_scene.get_view().delete_item()

    def on_edit_cut(self):
        if self.get_current_rnx_node_editor_widget():
            data = self.get_current_rnx_node_editor_widget().gr_scene.clipboard.serialize_selected(delete=True)
            data_str = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(data_str)

    def on_edit_copy(self):
        if self.get_current_rnx_node_editor_widget():
            data = self.get_current_rnx_node_editor_widget().gr_scene.clipboard.serialize_selected(delete=False)
            data_str = json.dumps(data, indent=4)
            print(data_str)
            QApplication.instance().clipboard().setText(data_str)

    def on_edit_paste(self):
        if self.get_current_rnx_node_editor_widget():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data)
            except ValueError as e:
                print("not valid json data to paste!", e)
                return

            # check if the json data is correct
            if 'nodes' not in data:
                print("JSON does not contain any node!")
                return

            self.get_current_rnx_node_editor_widget().gr_scene.clipboard.deserialize_from_clipboard(data)

    def read_settings(self):
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def write_settings(self):
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())