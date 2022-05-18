import cv2
import cv2 as cv


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

    def fx_detect_edges(self, image):
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

    def fx_binary_image(self, image, **kwargs):
        generate = self.toolsWidget.generate_binary_image
        if not generate:
            return image

        greyscale = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        threshold = cv.adaptiveThreshold(greyscale, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 7)
        return cv.cvtColor(threshold, cv.COLOR_GRAY2BGR)
