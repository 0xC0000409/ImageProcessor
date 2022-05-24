import cv2 as cv
import numpy as np
import pytesseract
from PyQt5.QtWidgets import QPushButton, QMessageBox

from core.helpers.generic import GenericHelper
from core.helpers.message_box import QtMessageBox, QtMessageBoxVariant


class FxMixin(object):
    def fx_brightness(self, image, **kwargs):
        value = self.editWidget.brightnessSlider.value()
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv.merge((h, s, v))
        return cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)

    def fx_blur(self, image, **kwargs):
        value = self.editWidget.blurSlider.value()
        return cv.blur(image, (value + 1, value + 1))

    def fx_detect_edges(self, image, **kwargs):
        if not self.toolsWidget.detect_edges:
            return image

        return cv.cvtColor(cv.Canny(image, 70, 150), cv.COLOR_GRAY2RGB)

    def fx_contrast(self, image, **kwargs):
        alpha = float(self.editWidget.contrastSlider.value()) / 10
        return cv.convertScaleAbs(image, alpha=alpha)

    def fx_rotate(self, image, **kwargs):
        angle = -(self.editWidget.rotationDial.value() - 180)
        (height, width) = image.shape[:2]
        rotation_point = (width // 2, height // 2)
        rotation_matrix = cv.getRotationMatrix2D(rotation_point, angle, 1.0)

        return cv.warpAffine(image, rotation_matrix, (width, height))

    def fx_flip(self, image, **kwargs):
        flip_mode = self.editWidget.flip_mode
        if not flip_mode:
            return image

        return cv.flip(image, flip_mode)

    def fx_extract_text(self, image, **kwargs):
        generate = self.toolsWidget.extract_text
        if not generate:
            return image

        grayscale = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        threshold = cv.adaptiveThreshold(grayscale, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 7)

        if self.DEBUG_MODE:
            GenericHelper.show_img(threshold)

        rect_kernel = cv.getStructuringElement(cv.MORPH_RECT, (18, 18))

        dilation = cv.dilate(threshold, rect_kernel)

        contours, hierarchy = cv.findContours(dilation, cv.RETR_EXTERNAL,
                                              cv.CHAIN_APPROX_NONE)

        extracted_text = ""
        img_copy = image.copy()
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if self.DEBUG_MODE:
                GenericHelper.show_img(img_copy)

            cropped = img_copy[y:y + h, x:x + w]
            text = pytesseract.image_to_string(cropped)
            extracted_text = extracted_text + text

        text_extracted = len(extracted_text) > 0

        message_box = QtMessageBox(self, {
            'icon': QtMessageBoxVariant.INFORMATION if text_extracted else QtMessageBoxVariant.WARNING,
            'title': "Detected Text:",
            'text': extracted_text if text_extracted else "Text couldn't be extracted from the given image."
        })

        if text_extracted:
            def _clicked():
                self.clipboard.setText(extracted_text)
                QtMessageBox(self, {
                    'icon': QtMessageBoxVariant.INFORMATION,
                    'title': "Information",
                    'text': "Text copied to clipboard"
                }).show()

            btn = QPushButton("Copy to Clipboard")
            btn.clicked.connect(_clicked)
            message_box.msg_box.addButton(btn, QMessageBox.NoRole)

        message_box.show()

        self.toolsWidget.extract_text = False

        return image

    def fx_align_image(self, image, **kwargs):
        if not self.toolsWidget.align_image:
            return image

        opened = GenericHelper.open_image(self)

        if not opened:
            return image

        grayscale = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        orb = cv.ORB_create(500)
        keypoints, descriptors = orb.detectAndCompute(grayscale, None)

        if self.DEBUG_MODE:
            GenericHelper.show_img(cv.drawKeypoints(image, keypoints, outImage=np.array([]), color=(255, 0, 0),
                                                    flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))

        self.toolsWidget.align_image = False

        return image
