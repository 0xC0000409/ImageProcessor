import os

import cv2 as cv
from PyQt5.QtWidgets import QFileDialog

from src.helpers.message_box import QtMessageBox, QtMessageBoxVariant


class GenericHelper:
    IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

    @staticmethod
    def show_img(image):
        cv.namedWindow("output", cv.WINDOW_NORMAL)
        cv.imshow("output", image)
        cv.waitKey(0)

    @staticmethod
    def open_image(parent_window):
        image_path =\
            QFileDialog.getOpenFileName(parent_window, 'Open Image', './', "Image files (*.jpg *.jpeg *.png)")[0]

        if image_path and os.path.splitext(image_path)[1].lower() in GenericHelper.IMAGE_EXTENSIONS:
            return {
                'image': cv.cvtColor(cv.imread(image_path), cv.COLOR_BGR2RGB),
                'path': image_path
            }

        if image_path:
            QtMessageBox(parent_window, {
                'icon': QtMessageBoxVariant.CRITICAL,
                'title': "Error",
                'text': "Image couldn't be opened."
            }).show()

        return None
