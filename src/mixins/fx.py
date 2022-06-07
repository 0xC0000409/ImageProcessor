import cv2 as cv
import numpy as np
import pytesseract
from PyQt5.QtWidgets import QPushButton, QMessageBox

from src.helpers.generic import GenericHelper
from src.helpers.message_box import QtMessageBox, QtMessageBoxVariant


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
        if not self.toolsWidget.align_image["execute"]:
            return image

        if not self.toolsWidget.align_image["opened"]:
            self.toolsWidget.align_image["opened"] = GenericHelper.open_image(self)

        opened = self.toolsWidget.align_image["opened"]

        if not opened:
            return image

        src_grayscale = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        target_grayscale = cv.cvtColor(opened['image'], cv.COLOR_RGB2GRAY)

        orb = cv.ORB_create(500)
        src_keypoints, src_descriptors = orb.detectAndCompute(src_grayscale, None)
        target_keypoints, target_descriptors = orb.detectAndCompute(target_grayscale, None)

        if self.DEBUG_MODE:
            GenericHelper.show_img(cv.drawKeypoints(image, src_keypoints, outImage=np.array([]), color=(255, 0, 0),
                                                    flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
            GenericHelper.show_img(
                cv.drawKeypoints(opened["image"], target_keypoints, outImage=np.array([]), color=(255, 0, 0),
                                 flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))

        matcher = cv.DescriptorMatcher_create(cv.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(src_descriptors, target_descriptors, None)

        matches = sorted(matches, key=lambda x: x.distance, reverse=False)
        good_matches = int(len(matches) * 0.1)
        matches = matches[:good_matches]

        if self.DEBUG_MODE:
            GenericHelper.show_img(
                cv.drawMatches(image, src_keypoints, opened['image'], target_keypoints, matches, None))

        points_1 = np.zeros((len(matches), 2), dtype=np.float32)
        points_2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points_1[i, :] = src_keypoints[match.queryIdx].pt
            points_2[i, :] = target_keypoints[match.trainIdx].pt

        h, mask = cv.findHomography(points_1, points_2, cv.RANSAC)
        height, width, channels = opened["image"].shape

        return cv.warpPerspective(image, h, (width, height))

    def fx_detect_faces(self, image, **kwargs):
        if not self.toolsWidget.detect_faces:
            return image

        face_cascade = cv.CascadeClassifier("./data/haarcascade_frontalface_alt.xml")
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return image

    def fx_detect_objects(self, image, **kwargs):
        if not self.toolsWidget.detect_objects:
            return image

        FONTFACE = cv.FONT_HERSHEY_SIMPLEX
        FONT_SCALE = 0.7
        THICKNESS = 1

        dimension = 300
        threshold = 0.25

        net = self.object_detection.get("net")
        labels = self.object_detection.get("labels")

        def _draw_text(text, _x, _y):
            text_size = cv.getTextSize(text, FONTFACE, FONT_SCALE, THICKNESS)

            dim = text_size[0]
            baseline = text_size[1]

            cv.rectangle(image, (_x, _y - dim[1] - baseline), (_x + dim[0], _y + baseline), (0, 0, 0), cv.FILLED)
            cv.putText(image, text, (_x, _y - 5), FONTFACE, FONT_SCALE, (0, 255, 255), THICKNESS, cv.LINE_AA)

        blob = cv.dnn.blobFromImage(image, 1.0, size=(dimension, dimension), mean=(0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)

        objects = net.forward()

        rows = image.shape[0]
        cols = image.shape[1]

        for i in range(objects.shape[2]):
            class_id = int(objects[0, 0, i, 1])
            score = float(objects[0, 0, i, 2])

            x = int(objects[0, 0, i, 3] * cols)
            y = int(objects[0, 0, i, 4] * rows)
            w = int(objects[0, 0, i, 5] * cols - x)
            h = int(objects[0, 0, i, 6] * rows - y)

            if score > threshold:
                _draw_text("{}".format(labels[class_id]), x, y)
                cv.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)

        return image
