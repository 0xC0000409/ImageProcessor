from enum import Enum

from PyQt5.QtWidgets import QMessageBox, QSizePolicy, QPushButton


class QtMessageBoxVariant(Enum):
    INFORMATION = "information"
    WARNING = "warning"
    QUESTION = "question"
    CRITICAL = "critical"


class QtMessageBox:
    icon = {
        QtMessageBoxVariant.INFORMATION: QMessageBox.Information,
        QtMessageBoxVariant.WARNING: QMessageBox.Warning,
        QtMessageBoxVariant.QUESTION: QMessageBox.Question,
        QtMessageBoxVariant.CRITICAL: QMessageBox.Critical,
    }

    def __init__(self, parent, config):
        self.msg_box = QMessageBox(parent)

        self.msg_box.setIcon(QtMessageBox.icon[config.get('icon')])
        self.msg_box.setText(config.get('text'))
        self.msg_box.setWindowTitle(config.get('title'))
        self.msg_box.setStandardButtons(config.get('buttons', QMessageBox.Ok))

    def show(self):
        self.msg_box.exec_()
