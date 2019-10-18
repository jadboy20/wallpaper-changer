import os
import sys
import ctypes
import traceback


class Wallpaper(object):
    def __init__(self):
        if __debug__:
            print("Wallpaper object created!")

        img_path = os.path.join("C:\\", "users", "james", "pictures", "borderlands3_wallpaper.jpg")
        self.loadImage(img_path)


    def loadImage(self, img_path):
        """Load image.

        path: Path to image => str
        """
        SPI_SETDESKWALLPAPER = 20
        try:
            print("{} loaded.".format(img_path))
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_path , 3)
        except Exception:
            print(traceback.format_exc())
