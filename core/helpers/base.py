from PyQt5.QtWidgets import QMessageBox


def copy_to_clipboard():
    msg = QMessageBox()
    msg.setText("Copied to Clipboard")
    msg.exec_()