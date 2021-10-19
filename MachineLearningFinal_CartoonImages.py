import kivy
import cv2
import numpy as np
import sys
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.image import Image


# represent log in form
class MainWindow(Screen, Widget):

    def selected(self, filename):
        self.ids.my_image.source = filename[0]
        self.make_cartoon(filename)

    def thresh1_change(self, widget_name, value):
        filename = self.ids.my_image.source
        self.make_cartoon((filename, ))

    def make_cartoon(self, filename):
        self.ids.my_image.source = filename[0]
        cv2.waitKey(0)
        file_name = self.ids.my_image.source
        # originalmage = cv2.imread(r"C:\Users\ktbug\Test Images\katie-face.jpg", 1)
        originalmage = cv2.imread(file_name, 1)


        ReSized1 = cv2.resize(originalmage, (960, 540))

        # converting an image to grayscale
        grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
        ReSized2 = cv2.resize(grayScaleImage, (960, 540))

        # applying blur to smooth out the image
        smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
        ReSized3 = cv2.resize(smoothGrayScale, (960, 540))

        # retrieving the edges for cartoon effect
        # getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
        #                                 cv2.ADAPTIVE_THRESH_MEAN_C,
        #                                 cv2.THRESH_BINARY, 9, 9)

        getEdge = cv2.Canny(smoothGrayScale, self.ids.my_slides_dos.value, self.ids.my_slides.value)
        outline = cv2.threshold(getEdge, 64, 255, cv2.THRESH_BINARY_INV)

        ReSized4 = cv2.resize(getEdge, (960, 540))

        # applying filters to remove noise
        # and keep edge sharp as required
        colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
        ReSized5 = cv2.resize(colorImage, (960, 540))

        cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=outline[1])

        ReSized6 = cv2.resize(cartoonImage, (960, 540))

        cartoon_path = "Cartoon-" + os.path.basename(filename[0])
        cv2.imwrite(cartoon_path, cartoonImage)
        self.ids.my_image_dos.source = cartoon_path
        self.ids.my_image_dos.reload()
        # cv2.waitKey(0)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("Final.kv")


class FinalMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    FinalMainApp().run()
