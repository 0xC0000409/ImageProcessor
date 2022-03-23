import functools
import os

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

    def render_image(func):
        @functools.wraps(func)
        def wrapper(self, **kwargs):
            result = func(self, **kwargs)
            self._render_image()
            return result

        return wrapper

    def _render_image(self):
        if self.image is None:
            return

        frame = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image).scaled(self.UI_image_view.width(),
                                                 self.UI_image_view.height(),
                                                 QtCore.Qt.KeepAspectRatio,
                                                 QtCore.Qt.SmoothTransformation)
        self.UI_image_view.setPixmap(pixmap)

    @render_image
    def _process_image(self, **kwargs):
        if self.image is None:
            return

        def apply_effects(fx_functions, current_image):
            return current_image if len(fx_functions) == 0\
                else apply_effects(fx_functions[1:], fx_functions[0](current_image))

        self.image = apply_effects([getattr(self, attr) for attr in dir(self) if attr.startswith('fx')], self.original_image)

    @render_image
    def open_image(self, **kwargs):
        image_path = QFileDialog.getOpenFileName(self, 'Open Image', './', "Image files (*.jpg *.jpeg *.png)")[0]
        if image_path and os.path.splitext(image_path)[1] in ['.jpg', '.jpeg' '.png']:
            self.image_path = image_path
            self.setWindowTitle(image_path)
            self.image = cv.imread(self.image_path)
            self.original_image = self.image.copy()

    def fx_brightness(self, image, **kwargs):
        value = self.UI_z.value()
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv.merge((h, s, v))
        return cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)

    def fx_blur(self, image, **kwargs):
        value = self.UI_y.value()
        return cv.blur(image, (value + 1, value + 1))


app = QApplication(sys.argv)
MainWindow = Main()
app.exec_()
