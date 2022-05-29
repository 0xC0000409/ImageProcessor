import functools
from abc import abstractmethod

from PyQt5.QtWidgets import QWidget


class AbstractUi(QWidget):
    def image_processed(func):
        @functools.wraps(func)
        def wrapper(self, **kwargs):
            result = func(self, **kwargs)
            self.root._process_image(**kwargs)
            return result

        return wrapper

    def __init__(self, parent, root):
        super(AbstractUi, self).__init__(parent)
        self.root = root

    @abstractmethod
    def get_widget_state(self):
        pass

    @abstractmethod
    def set_widget_state(self, state):
        pass
