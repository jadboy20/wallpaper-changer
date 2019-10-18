import os
import sys
import ctypes
import traceback
import time


VALID_PATH = "C:\\users\\james\\pictures"
INVALID_PATH = "C:\\hello"


class Wallpaper(object):
    def __init__(self):
        if __debug__:
            print("Wallpaper object created!")

        self.images = []
        self.load_images_from_folder(VALID_PATH)

        for image in self.images:
            self.loadImage(image)
            time.sleep(5)

    def load_images_from_folder(self, folder_path):
        """Loads folder images."""
        self.images = []
        img_list = []
        try:
            img_list = os.listdir(folder_path)
        except FileNotFoundError:
            print("Can't find directory {}".format(folder_path))
        else:
            for img in img_list:
                if self.is_valid_image_format(img):
                    self.images.append(os.path.join(folder_path, img))

    @staticmethod
    def is_valid_image_format(imgpath):
        """Check if image ends with correct file format.
        """
        return (imgpath.endswith(".jpg") or imgpath.endswith(".png") or imgpath.endswith(".bmp")) and not os.path.isdir(imgpath)

    def _image_exists(self, img_path):
        """Check that file exists"""
        return os.path.exists(img_path)

    def loadImage(self, img_path):
        """Load image.

        path: Path to image => str
        """
        SPI_SETDESKWALLPAPER = 20
        # First check that file exists.
        if self._image_exists(img_path):
            try:
                print("{} loaded.".format(img_path))
                ctypes.windll.user32.SystemParametersInfoW(
                    SPI_SETDESKWALLPAPER, 0, img_path, 3)
            except Exception:
                print(traceback.format_exc())
        else:
            print("{} does not exist!".format(img_path))
