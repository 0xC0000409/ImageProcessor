import cv2 as cv


class FxMixin(object):
    def fx_brightness(self, image, **kwargs):
        value = self.UI_z.value()
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)

        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value

        final_hsv = cv.merge((h, s, v))
        return cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)

    def fx_blur(self, image, **kwargs):
        value = self.UI_y.value()
        return cv.blur(image, (value + 1, value + 1))
