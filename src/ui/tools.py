import os
from os.path import isfile

from src.helpers.generic import GenericHelper
from src.ui.abstract_ui import AbstractUi
from PyQt5 import uic, QtGui


class Tools(AbstractUi):
    def __init__(self, parent, root):
        super().__init__(parent, root)
        uic.loadUi(GenericHelper.get(__file__, '../../ui/tools.ui'), self)

        self.extract_text = False
        self.detect_edges = False

        self.align_image = {
            'execute': False,
            'opened_image': None
        }

        self.detect_faces = False
        self.detect_objects = False

        if isfile(os.getenv("TESSERACT_EXECUTABLE_PATH")):
            self.buttonExtractText.clicked.connect(self._extract_text)
        else:
            self.buttonExtractText.setStyleSheet("background-color:grey;")

        self.buttonExtractText.setIcon(
            QtGui.QIcon(GenericHelper.get(__file__, "../../icons/widgets/extract_text.png")))

        self.buttonDetectEdges.clicked.connect(self._detect_edges)
        self.buttonDetectEdges.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../../icons/widgets/detect_edges.png")))

        self.buttonAlignImage.clicked.connect(self._align_image)
        self.buttonAlignImage.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../../icons/widgets/align_image.png")))

        self.buttonDetectFaces.clicked.connect(self._detect_faces)
        self.buttonDetectFaces.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../../icons/widgets/detect_faces.png")))

        self.buttonDetectObjects.clicked.connect(self._detect_objects)
        self.buttonDetectObjects.setIcon(
            QtGui.QIcon(GenericHelper.get(__file__, "../../icons/widgets/detect_objects.png")))

    def get_widget_state(self):
        return {
            'extract_text': self.extract_text,
            'detect_edges': self.detect_edges,
            'align_image': self.align_image,
            'detect_faces': self.detect_faces,
            'detect_objects': self.detect_objects,
        }

    def set_widget_state(self, state=None):
        if state is None:
            state = {}

        self.buttonExtractText.blockSignals(True)
        self.buttonDetectEdges.blockSignals(True)
        self.buttonAlignImage.blockSignals(True)
        self.buttonDetectFaces.blockSignals(True)

        self.extract_text = state.get('extract_text', False)
        self.detect_edges = state.get('detect_edges', False)
        self.align_image = state.get('align_image', {
            'execute': False,
            'opened_image': None
        })
        self.detect_faces = False
        self.detect_objects = False

        self.buttonExtractText.blockSignals(False)
        self.buttonDetectEdges.blockSignals(False)
        self.buttonAlignImage.blockSignals(False)
        self.buttonDetectFaces.blockSignals(False)

    @AbstractUi.image_processed
    def _extract_text(self):
        self.extract_text = not self.extract_text

    @AbstractUi.image_processed
    def _detect_edges(self):
        self.detect_edges = not self.detect_edges

    @AbstractUi.image_processed
    def _align_image(self):
        self.align_image["execute"] = True
        self.align_image["opened"] = None

    @AbstractUi.image_processed
    def _detect_faces(self):
        self.detect_faces = not self.detect_faces

    @AbstractUi.image_processed
    def _detect_objects(self):
        self.detect_objects = not self.detect_objects
