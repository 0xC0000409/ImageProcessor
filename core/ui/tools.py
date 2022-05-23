from core.ui.abstract_ui import AbstractUi
from PyQt5 import uic


class Tools(AbstractUi):
    def __init__(self, parent, root):
        super().__init__(parent, root)
        uic.loadUi('./ui/tools.ui', self)

        self.extract_text = False
        self.detect_edges = False

        self.buttonExtractText.clicked.connect(self._extract_text)
        self.buttonDetectEdges.clicked.connect(self._detect_edges)

    def get_widget_state(self):
        return {
            'extract_text': self.extract_text,
            'detect_edges': self.detect_edges
        }

    def set_widget_state(self, state=None):
        if state is None:
            state = {}

        self.buttonExtractText.blockSignals(True)
        self.buttonDetectEdges.blockSignals(True)
        self.extract_text = state.get('extract_text', False)
        self.detect_edges = state.get('detect_edges', False)
        self.buttonExtractText.blockSignals(False)
        self.buttonDetectEdges.blockSignals(False)

    @AbstractUi.image_processed
    def _extract_text(self):
        self.extract_text = True

    @AbstractUi.image_processed
    def _detect_edges(self):
        self.detect_edges = True
