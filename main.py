import functools
import random

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import cv2 as cv
import sys


class Main(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super(Main, self).__init__()

        uic.loadUi('./UI/main.ui', self)

        self.UI_action_open = self.findChild(QAction, "actionOpen")
        self.UI_image_view = self.findChild(QLabel, "imageView")
        self.UI_z = self.findChild(QSlider, "horizontalSlider")
        self.UI_image_view.setMinimumSize(426, 240)

        self.UI_action_open.triggered.connect(self.open_image)
        self.resized.connect(self._render_image)
        self.UI_z.valueChanged.connect(self._process_image)

        self.image_path = None
        self.image = None
        self.original_image = None

        self.show()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Main, self).resizeEvent(event)

    def render_image(func):
        @functools.wraps(func)
        def wrapper(self, **kwargs):
            result = func(self, **kwargs)
            self._render_image()
            return result

        return wrapper

    def _render_image(self):
        if self.image is not None:
            frame = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image).scaled(self.UI_image_view.width(),
                                                     self.UI_image_view.height(),
                                                     QtCore.Qt.KeepAspectRatio,
                                                     QtCore.Qt.SmoothTransformation)
            self.UI_image_view.setPixmap(pixmap)

    @render_image
    def _process_image(self, **kwargs):
        processing_functions = [self.change_brightness]
        for processor in processing_functions:
            self.image = processor(**kwargs)

    @render_image
    def open_image(self, **kwargs):
        image_path = QFileDialog.getOpenFileName(self, 'Open Image', './', "Image files (*.jpg *.gif *.png)")
        if image_path[0]:
            self.image_path = image_path[0]
            self.image = cv.imread(self.image_path)
            self.original_image = self.image.copy()

    @render_image
    def change_brightness(self, **kwargs):
        value = self.UI_z.value()
        hsv = cv.cvtColor(self.original_image, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv.merge((h, s, v))
        return cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)


app = QApplication(sys.argv)
MainWindow = Main()
app.exec_()
