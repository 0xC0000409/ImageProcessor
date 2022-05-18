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

    @AbstractUi.image_processed
    def _generate_binary_image(self):
        self.generate_binary_image = True

    @AbstractUi.image_processed
    def _detect_edges(self):
        self.detect_edges = True
