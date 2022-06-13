from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import cv2 as cv

from src.helpers.generic import GenericHelper
from src.mixins.base import BaseMixin
from src.mixins.fx import FxMixin
from src.ui.edit import Edit
from src.ui.tools import Tools


class Main(QMainWindow, BaseMixin, FxMixin):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super(Main, self).__init__()

        self.image_path = None
        self.image = None
        self.original_image = None

        self.child_widgets = []

        uic.loadUi(GenericHelper.get(__file__, '../ui/main.ui'), self)
        self.mount_ui(Edit, self.tabEditWidget, "editWidget")
        self.mount_ui(Tools, self.tabToolsWidget, "toolsWidget")

        self.tabWidget.setTabIcon(0, QtGui.QIcon(GenericHelper.get(__file__, "../icons/widgets/edit_tab.png")))
        self.tabWidget.setTabIcon(1, QtGui.QIcon(GenericHelper.get(__file__, "../icons/widgets/tools_tab.png")))

        self.setWindowIcon(QtGui.QIcon(GenericHelper.get(__file__, "../icons/base/main.png")))

        self.tabWidget.hide()

        self.resized.connect(self._render_image)

        # ----------------- Menubar -----------------
        self.actionOpen.triggered.connect(self.open_image)
        self.actionOpen.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../icons/base/open.png")))

        self.actionSave.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../icons/base/save.png")))
        self.actionSave.triggered.connect(self.save_image)
        self.actionSaveAs.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../icons/base/save-as.png")))
        self.actionSaveAs.triggered.connect(self.save_image_as)

        self.actionRestoreImage.triggered.connect(self.restore_image)
        self.actionRestoreImage.setEnabled(False)
        self.actionRestoreImage.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../icons/base/reset.png")))

        self.actionExit.triggered.connect(self.close)
        self.actionExit.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../icons/base/exit.png")))

        self.actionAbout.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../icons/base/about.png")))
        self.actionAboutQt.triggered.connect(lambda: QMessageBox.aboutQt(self, "About"))
        self.actionAboutQt.setIcon(QtGui.QIcon(GenericHelper.get(__file__, "../icons/base/qt.png")))
        # ----------------- End of Menubar -----------------
        self.imageView.setMinimumSize(426, 240)

        self.object_detection = {
            "net": cv.dnn.readNetFromTensorflow(GenericHelper.get(__file__, GenericHelper.OBJECT_DETECTION_MODEL_FILE),
                                                GenericHelper.get(__file__,
                                                                  GenericHelper.OBJECT_DETECTION_CONFIG_FILE)),
            "labels": None
        }

        with open(GenericHelper.get(__file__, GenericHelper.OBJECT_DETECTION_CLASS_FILE)) as fp:
            self.object_detection["labels"] = fp.read().split("\n")

        self.show()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Main, self).resizeEvent(event)

    def mount_ui(self, ui_class, mount_point, widget_name):
        setattr(self, widget_name, ui_class(mount_point, self))
        child_widget = getattr(self, widget_name)
        mount_point.layout().addWidget(child_widget)
        self.child_widgets.append(child_widget)

    @BaseMixin.render_image
    def open_image(self, **kwargs):
        opened = GenericHelper.open_image(self)

        if opened:
            self.image_path = opened['path']
            self.setWindowTitle(self.image_path)
            self.image = opened['image']
            self.original_image = self.image.copy()

            self.tabWidget.show()
            self.actionRestoreImage.setEnabled(True)
            self.actionSave.setEnabled(True)
            self.actionSaveAs.setEnabled(True)
            self.restore_image()

    def save_image(self, **kwargs):
        cv.imwrite(self.image_path, cv.cvtColor(self.image, cv.COLOR_BGR2RGB))
        self.show_status_bar_message(f'Image: {self.image_path.split("/")[-1]} saved.')

    def save_image_as(self, **kwargs):
        image_name = self.image_path.split("/")[-1]
        directory = QFileDialog.getSaveFileName(self, "Save Image as", image_name, "Image files (*.jpg *.jpeg *.png)")[
            0]

        if directory:
            cv.imwrite(directory, cv.cvtColor(self.image, cv.COLOR_BGR2RGB))
            self.show_status_bar_message(f'Image: {image_name} saved.')

    @BaseMixin.render_image
    def restore_image(self, **kwargs):
        for child in self.child_widgets:
            child.set_widget_state()
        self.image = self.original_image
