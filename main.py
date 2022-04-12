import sys

from PyQt5.QtWidgets import QApplication

from core.core import Main

app = QApplication(sys.argv)
MainWindow = Main()
app.exec_()
