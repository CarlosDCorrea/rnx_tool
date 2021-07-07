from PyQt5.QtWidgets import QApplication, QStyleFactory
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


from calc_window import CalcWindow


"""
Here the app will be run
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    print(QStyleFactory.keys())  # With this we can see the different styles that come with pyqt5
    app.setStyle('Fusion')
    window = CalcWindow()
    window.show()
    sys.exit(app.exec())
