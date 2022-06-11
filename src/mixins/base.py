import functools

from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap


class BaseMixin(object):
    def render_image(func):
        @functools.wraps(func)
        def wrapper(self, **kwargs):
            result = func(self, **kwargs)
            self._render_image()
            return result

        return wrapper

    def show_status_bar_message(self, message, timeout=3000):
        self.statusBar().showMessage(message, timeout)

    def _render_image(self):
        if self.image is None:
            return

        image = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0],
                       QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image).scaled(self.imageView.width(),
                                                 self.imageView.height(),
                                                 QtCore.Qt.KeepAspectRatio,
                                                 QtCore.Qt.SmoothTransformation)
        self.imageView.setPixmap(pixmap)

    @render_image
    def _process_image(self, **kwargs):
        if self.image is None:
            return

        def apply_effects(fx_functions, current_image):
            return current_image if len(fx_functions) == 0 \
                else apply_effects(fx_functions[1:], fx_functions[0](current_image, **kwargs))

        fx_functions = [getattr(self, attr) for attr in dir(self) if attr.startswith('fx_')]
        self.image = apply_effects(fx_functions, self.original_image)
