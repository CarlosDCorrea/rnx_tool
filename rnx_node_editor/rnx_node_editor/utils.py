from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile
from pprint import PrettyPrinter
import traceback


pp = PrettyPrinter(indent=4).pprint

def dump_exception(e):
    print("%s EXCEPTION::" % e.__class__.__name__, e)
    traceback.print_tb(e.__traceback__)


def load_style_sheet(filename):
    print("STYLE loaded: ", filename)
    file = QFile(filename)
    file.open(QFile.ReadOnly or QFile.Text)
    style_sheet = file.readAll()
    QApplication.instance().setStyleSheet(str(style_sheet, encoding="utf-8"))


def load_style_sheet(*args):
    res = ''

    for arg in args:
        file = QFile(arg)
        file.open(QFile.ReadOnly or QFile.Text)
        style_sheet = file.readAll()
        res += '\n' + str(style_sheet, encoding="utf-8")

    QApplication.instance().setStyleSheet(res)
