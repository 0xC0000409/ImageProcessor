import os
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import cv2 as cv

from core.mixins.base import BaseMixin
from core.mixins.fx import FxMixin
from core.ui.edit import Edit
from core.ui.tools import Tools


class Main(QMainWindow, BaseMixin, FxMixin):
    resized = QtCore.pyqtSignal()
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

    def __init__(self):
        super(Main, self).__init__()

        uic.loadUi('./ui/main.ui', self)
        self.mount_ui(Edit, self.tabEditWidget, "editWidget")
        self.mount_ui(Tools, self.tabToolsWidget, "toolsWidget")

        self.tabWidget.hide()

        self.resized.connect(self._render_image)

        # ----------------- Menubar -----------------
        self.actionOpen.triggered.connect(self.open_image)
        self.actionUndo.triggered.connect(self.undo)
        self.actionExit.triggered.connect(self.close)
        # ----------------- End of Menubar -----------------
        self.imageView.setMinimumSize(426, 240)

        self.image_path = None
        self.image = None
        self.original_image = None
        self.state_stack = []

        self.show()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Main, self).resizeEvent(event)

    def mount_ui(self, ui_class, mount_point, widget_name):
        setattr(self, widget_name, ui_class(mount_point, self))
        mount_point.layout().addWidget(getattr(self, widget_name))

    @BaseMixin.render_image
    def open_image(self, **kwargs):
        image_path = QFileDialog.getOpenFileName(self, 'Open Image', './', "Image files (*.jpg *.jpeg *.png)")[0]
        if image_path and os.path.splitext(image_path)[1] in self.IMAGE_EXTENSIONS:
            self.image_path = image_path
            self.setWindowTitle(image_path)
            self.image = cv.imread(self.image_path)
            self.image = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
            self.original_image = self.image.copy()
            self.tabWidget.show()

    @BaseMixin.render_image
    def undo(self, **kwargs):
        print('Undo')
