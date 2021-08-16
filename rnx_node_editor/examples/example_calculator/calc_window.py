from PyQt5.QtWidgets import (
    QWidget, QMdiArea, QDockWidget, QAction, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import QSignalMapper, QSettings, QPoint, QSize, Qt
from rnx_node_editor.rnx_node_window import RnxNodeWindow
from examples.example_calculator.rnx_sub_window import RnxSubWindow
from rnx_node_editor.utils import load_style_sheet
import qss.nodeeditor_dark_resources
from rnx_node_editor.utils import pp
from rnx_drag_listbox import DragListWidget
from rnx_conf import *
from rnx_conf_nodes import *
import os


DEBUG = False


class CalcWindow(RnxNodeWindow):

    def init_ui(self):
        self.name_company = "Universidad_Cesmag"
        self.name_product = "Rnx_Node_Editor"

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/node_style.qss")
        load_style_sheet(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
            self.stylesheet_filename
        )

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registration Node")
            pp(RNX_NODES)

        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setViewMode(QMdiArea.TabbedView)
        self.mdi_area.setDocumentMode(True)
        self.mdi_area.setTabsClosable(True)
        self.mdi_area.setTabsMovable(True)
        self.setCentralWidget(self.mdi_area)

        self.mdi_area.subWindowActivated.connect(self.update_menus)
        self.window_mapper = QSignalMapper(self)
        self.window_mapper.mapped[QWidget].connect(self.set_active_sub_window)

        self.create_nodes_dock()
        self.create_actions()
        self.create_menus()
        self.create_tool_bars()
        self.create_status_bar()
        self.update_menus()

        self.read_settings()

        self.setWindowTitle("Calculator node editor example")

    def get_current_rnx_node_editor_widget(self):
        active_sub_window = self.mdi_area.activeSubWindow()
        if active_sub_window:
            return active_sub_window.widget()
        return None

    def create_nodes_dock(self):
        self.list_widget_methods = DragListWidget(1)

        self.list_widget_metrics = DragListWidget(2)

        self.list_widget_data = DragListWidget(3)

        self.list_widget_visuals = DragListWidget(4)

        self.items_methods = QDockWidget("Methods")
        self.items_methods.setWidget(self.list_widget_methods)
        self.items_methods.setFloating(False)
        self.items_metrics = QDockWidget("Metrics")
        self.items_metrics.setWidget(self.list_widget_metrics)
        self.items_metrics.setFloating(False)
        self.items_data = QDockWidget("Data")
        self.items_data.setWidget(self.list_widget_data)
        self.items_data.setFloating(False)
        self.items_visuals = QDockWidget("Visuals")
        self.items_visuals.setWidget(self.list_widget_visuals)
        self.items_visuals.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.items_methods)
        self.addDockWidget(Qt.RightDockWidgetArea, self.items_metrics)
        self.addDockWidget(Qt.RightDockWidgetArea, self.items_data)
        self.addDockWidget(Qt.RightDockWidgetArea, self.items_visuals)

    def closeEvent(self, event):
        self.mdi_area.closeAllSubWindows()
        if self.mdi_area.currentSubWindow():
            event.ignore()
        else:
            self.write_settings()
            event.accept()

    def update_window(self):
        pass

    def create_menus(self):
        super().create_menus()

        self.window_menu = self.menuBar().addMenu("&Window")
        self.update_window_menu()
        self.window_menu.aboutToShow.connect(self.update_window_menu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

        self.edit_menu.aboutToShow.connect(self.update_edit_menu)

    def update_menus(self):
        active = self.get_current_rnx_node_editor_widget()
        has_mdi_child = (active is not None)

        self.act_save.setEnabled(has_mdi_child)
        self.act_save_as.setEnabled(has_mdi_child)
        self.act_close.setEnabled(has_mdi_child)
        self.all_act_close.setEnabled(has_mdi_child)
        self.act_title.setEnabled(has_mdi_child)
        self.act_cascade.setEnabled(has_mdi_child)
        self.act_previous.setEnabled(has_mdi_child)
        self.act_separator.setVisible(has_mdi_child)

        self.update_edit_menu()

    def update_edit_menu(self):
        try:
            #  print("Update edit menu")
            active = self.get_current_rnx_node_editor_widget()
            has_mdi_child = (active is not None)

            self.act_paste.setEnabled(has_mdi_child)

            self.act_cut.setEnabled(has_mdi_child and active.has_selected_item())
            self.act_copy.setEnabled(has_mdi_child and active.has_selected_item())
            self.act_delete.setEnabled(has_mdi_child and active.has_selected_item())

            self.act_undo.setEnabled(has_mdi_child and active.can_undo())
            self.act_redo.setEnabled(has_mdi_child and active.can_redo())
        except Exception as e:
            print(e)

    def on_window_nodes_toolbar(self):
        if self.items_methods.isVisible():
            self.items_methods.hide()
        else:
            self.items_methods.show()

    def update_window_menu(self):
        self.window_menu.clear()

        toolbar_nodes = self.window_menu.addAction("Nodes toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.on_window_nodes_toolbar)
        toolbar_nodes.setChecked(self.items_methods.isVisible())

        self.window_menu.addAction(self.act_close)
        self.window_menu.addAction(self.all_act_close)
        self.window_menu.addSeparator()
        self.window_menu.addAction(self.act_title)
        self.window_menu.addAction(self.act_cascade)
        self.window_menu.addSeparator()
        self.window_menu.addAction(self.nextAct)
        self.window_menu.addAction(self.act_previous)
        self.window_menu.addAction(self.act_separator)

        windows = self.mdi_area.subWindowList()
        self.act_separator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):

            child = window.widget()
            text = "%d %s" % (i + 1, child.user_friendly_current_file())
            if i < 9:
                text = '&' + text

            action = self.window_menu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.get_current_rnx_node_editor_widget())
            action.triggered.connect(self.window_mapper.map)
            self.window_mapper.setMapping(action, window)

    def set_active_sub_window(self, window):
        if window:
            self.mdi_area.setActiveSubWindow(window)

    def create_actions(self):
        super().create_actions()

        self.act_close = QAction("Cl&ose", self,
                                 statusTip="Close the active window",
                                 triggered=self.mdi_area.closeActiveSubWindow)

        self.all_act_close = QAction("Close &All", self,
                                     statusTip="Close all the windows",
                                     triggered=self.mdi_area.closeAllSubWindows)

        self.act_title = QAction("&Tile", self, statusTip="Tile the windows",
                                 triggered=self.mdi_area.tileSubWindows)

        self.act_cascade = QAction("&Cascade", self,
                                   statusTip="Cascade the windows",
                                   triggered=self.mdi_area.cascadeSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.mdi_area.activateNextSubWindow)

        self.act_previous = QAction("Pre&vious", self,
                                    shortcut=QKeySequence.PreviousChild,
                                    statusTip="Move the focus to the previous window",
                                    triggered=self.mdi_area.activatePreviousSubWindow)

        self.act_separator = QAction(self)
        self.act_separator.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

    def on_file_new(self):
        sub_window = self.create_mdi_child()
        sub_window.show()

    def on_file_open(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Open project from file")
        try:
            for f_name in file_names:
                if f_name:
                    existing = self.find_mdi_child(f_name)
                    if existing:
                        self.mdi_area.setActiveSubWindow(existing)
                    else:
                        # we need to create a new sub window and open the file
                        rnx_node_editor = RnxSubWindow()
                        if rnx_node_editor.file_load(f_name):
                            self.statusBar().showMessage(f"file {f_name} loaded", 5000)
                            rnx_node_editor.set_title()
                            sub_window = self.create_mdi_child(rnx_node_editor)
                            sub_window.show()
                        else:
                            rnx_node_editor.close()
        except Exception as e:
            print(e)

    def about(self):
        QMessageBox.about(self, "About MDI",
                          "The <b>MDI</b> example demonstrates how to write multiple "
                          "document interface applications using Qt.")

    def create_tool_bars(self):
        pass

    def create_mdi_child(self, child_widget=None):
        rnx_node_editor = child_widget if child_widget else  RnxSubWindow()
        sub_window = self.mdi_area.addSubWindow(rnx_node_editor)
        sub_window.setWindowIcon(self.empty_icon)
        rnx_node_editor.gr_scene.history.add_history_modified_listeners(self.update_edit_menu)
        rnx_node_editor.add_close_event_listeners(self.on_sub_window_close)
        return sub_window

    def on_sub_window_close(self, widget, event):
        existing = self.find_mdi_child(widget.file_name)
        self.mdi_area.setActiveSubWindow(existing)

        if self.may_be_save():
            event.accept()
        else:
            event.ignore()

    def find_mdi_child(self, file_name):
        for window in self.mdi_area.subWindowList():
            if window.widget().file_name == file_name:
                return window
        return None

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

    def read_settings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def write_settings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
