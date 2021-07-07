from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QLabel, QApplication, QMessageBox
from PyQt5.QtGui import QCloseEvent
from .rnx_ne_widget import RnxNodeEditorWidget
import json
import os


class RnxNodeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = None
        self.status_mouse_pos = None
        self.init_ui()

    def create_action(self, name, shortcut, tooltip, callback):
        action = QAction(name, self)
        action.setShortcut(shortcut)
        action.setToolTip(tooltip)
        action.triggered.connect(callback)
        return action

    def init_ui(self):
        menu_bar = self.menuBar()

        # Init menu
        file_menu = menu_bar.addMenu("File")

        file_menu.addAction(self.create_action('New', 'Ctrl+N', 'Create new project', self.on_file_new))
        file_menu.addSeparator()
        file_menu.addAction(self.create_action('Open', 'Ctrl+O', 'Open file', self.on_file_open))
        file_menu.addAction(self.create_action('Save', 'Ctrl+S', 'Save project', self.on_file_save))
        file_menu.addAction(self.create_action('Save As...', 'Ctrl+Shift+S', 'Save project as...', self.on_file_save_as))
        file_menu.addSeparator()
        file_menu.addAction(self.create_action('Exit', 'Ctrl+Q', 'Exit', self.close_app))

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction(self.create_action('Undo', 'Ctrl+Z', 'Undo last', self.on_edit_undo))
        edit_menu.addAction(self.create_action('Redo', 'Ctrl+Y', 'Redo last', self.on_edit_redo))
        edit_menu.addSeparator()
        edit_menu.addAction(self.create_action('Cut', 'Ctrl+X', 'Cut to clipboard', self.on_edit_cut))
        edit_menu.addAction(self.create_action('Copy', 'Ctrl+C', 'Copy to clipboard', self.on_edit_copy))
        edit_menu.addAction(self.create_action('Paste', 'Ctrl+V', 'Paste to clipboard', self.on_edit_paste))
        edit_menu.addSeparator()
        edit_menu.addAction(self.create_action('Delete', 'Del', 'Delete selected item', self.on_edit_delete))

        rnx_node_editor = RnxNodeEditorWidget(self)
        rnx_node_editor.gr_scene.add_has_been_modified_listener(self.change_title)
        self.setCentralWidget(rnx_node_editor)

        # status bar
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        rnx_node_editor.view.scene_pos_changed.connect(self.on_scene_pos_changed)

        # Set windows properties
        self.setGeometry(200, 200, 800, 600)
        self.change_title()
        self.show()

    def change_title(self):
        title = "Rnx Node Editor -"
        if not self.file_name:
            title += "New"
        else:
            title += os.path.basename(self.file_name)

        if self.centralWidget().gr_scene.has_been_modified:
            title += "*"

        self.setWindowTitle(title)

    def on_scene_pos_changed(self, x, y):
        self.status_mouse_pos.setText("Scene pos: [%d, %d]" % (x, y))

    def on_file_new(self):
        if self.may_be_save():
            self.centralWidget().gr_scene.clear()
            self.file_name = None
            self.change_title()

    def on_file_open(self):
        if self.may_be_save():
            file_name, _ = QFileDialog.getOpenFileName(self, "Open project from file")
            if not file_name:
                return

            if os.path.isfile(file_name):
                self.centralWidget().gr_scene.load_from_file(file_name)
                self.file_name = file_name
                self.change_title()

    def on_file_save(self):
        if not self.file_name:
            return self.on_file_save_as()

        self.centralWidget().gr_scene.save_to_file(self.file_name)
        self.statusBar().showMessage("Succesfully saved: %s" % self.file_name)
        return True

    def on_file_save_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save project to file")
        if not file_name:
            return False

        self.file_name = file_name
        self.on_file_save()
        return True

    def is_modified(self):
        return self.centralWidget().gr_scene.has_been_modified

    def may_be_save(self):
        if not self.is_modified():
            return True

        # The second parameter is a label which is white, and therefore in the style file it has been changed
        res = QMessageBox.warning(self, "About to loose your progress",
                                  "The project has changes without \n save, would you like to save it?",
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
        self.centralWidget().gr_scene.history.undo()

    def on_edit_redo(self):
        self.centralWidget().gr_scene.history.redo()

    def on_edit_delete(self):
        self.centralWidget().gr_scene.scene.views()[0].delete_item()

    def on_edit_cut(self):
        data = self.centralWidget().gr_scene.clipboard.serialize_selected(delete=True)
        data_str = json.dumps(data, indent=4)
        QApplication.instance().clipboard().setText(data_str)

    def on_edit_copy(self):
        data = self.centralWidget().gr_scene.clipboard.serialize_selected(delete=False)
        data_str = json.dumps(data, indent=4)
        print(data_str)
        QApplication.instance().clipboard().setText(data_str)

    def on_edit_paste(self):
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

        self.centralWidget().gr_scene.clipboard.deserialize_from_clipboard(data)
