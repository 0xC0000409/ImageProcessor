import os
import sys

import pytesseract
from PyQt5.QtWidgets import QApplication
from dotenv import load_dotenv

from core.core import Main

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_EXECUTABLE")
app = QApplication(sys.argv)
MainWindow = Main()
MainWindow.clipboard = app.clipboard()
app.exec_()
