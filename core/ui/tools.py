from core.ui.abstract_ui import AbstractUi
from PyQt5 import uic


class Tools(AbstractUi):
    def __init__(self, parent, root):
        super().__init__(parent, root)
        uic.loadUi('./ui/tools.ui', self)

        self.generate_binary_image = False
        self.detect_edges = False

        self.buttonGenBinaryImage.clicked.connect(self._generate_binary_image)
        self.buttonDetectEdges.clicked.connect(self._detect_edges)

    def get_widget_state(self):
        return {
            'generate_binary_image': self.generate_binary_image,
            'detect_edges': self.detect_edges
        }

    def set_widget_state(self, state=None):
        if state is None:
            state = {}

        self.buttonGenBinaryImage.blockSignals(True)
        self.buttonDetectEdges.blockSignals(True)
        self.generate_binary_image = state.get('generate_binary_image', False)
        self.detect_edges = state.get('detect_edges', False)
        self.buttonGenBinaryImage.blockSignals(False)
        self.buttonDetectEdges.blockSignals(False)

    @AbstractUi.image_processed
    def _generate_binary_image(self):
        self.generate_binary_image = True

    @AbstractUi.image_processed
    def _detect_edges(self):
        self.detect_edges = True
