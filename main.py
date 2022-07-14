import os
import sys

import pytesseract
from PyQt5.QtWidgets import QApplication
from dotenv import load_dotenv

from src.core import Main
from src.helpers.generic import GenericHelper

load_dotenv(dotenv_path=GenericHelper.get(__file__, '.env'))

pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_EXECUTABLE_PATH")

app = QApplication(sys.argv)

MainWindow = Main()
MainWindow.clipboard = app.clipboard()
MainWindow.DEBUG_MODE = (os.getenv("DEBUG_MODE") in ('1', 'true'))

app.exec_()
