import os
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import cv2 as cv

from core.mixins.base import BaseMixin
from core.mixins.fx import FxMixin


class Main(QMainWindow, BaseMixin, FxMixin):
    resized = QtCore.pyqtSignal()
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

    def __init__(self):
        super(Main, self).__init__()

        uic.loadUi('./UI/main.ui', self)

        self.resized.connect(self._render_image)

        # ----------------- Menubar -----------------
        self.UI_action_open = self.findChild(QAction, "actionOpen")
        self.UI_action_open.triggered.connect(self.open_image)

        self.UI_action_save = self.findChild(QAction, "actionSave")

        self.UI_action_save_as = self.findChild(QAction, "actionSaveAs")

        self.UI_action_about = self.findChild(QAction, "actionAbout")

        self.UI_action_exit = self.findChild(QAction, "actionExit")
        self.UI_action_exit.triggered.connect(lambda: self.close())
        # ----------------- End of Menubar -----------------
        self.UI_image_view = self.findChild(QLabel, "imageView")
        self.UI_z = self.findChild(QSlider, "horizontalSlider")
        self.UI_y = self.findChild(QSlider, "horizontalSlider2")
        self.UI_image_view.setMinimumSize(426, 240)

        self.UI_z.valueChanged.connect(self._process_image)
        self.UI_y.valueChanged.connect(self._process_image)

        self.image_path = None
        self.image = None
        self.original_image = None

        self.show()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Main, self).resizeEvent(event)

    @BaseMixin.render_image
    def open_image(self, **kwargs):
        image_path = QFileDialog.getOpenFileName(self, 'Open Image', './', "Image files (*.jpg *.jpeg *.png)")[0]
        if image_path and os.path.splitext(image_path)[1] in self.IMAGE_EXTENSIONS:
            self.image_path = image_path
            self.setWindowTitle(image_path)
            self.image = cv.imread(self.image_path)
            self.original_image = self.image.copy()
