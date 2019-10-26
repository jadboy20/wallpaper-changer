import os
import sys
import ctypes
import traceback
import time


VALID_PATH = "C:\\users\\james\\pictures"
INVALID_PATH = "C:\\hello"


class Wallpaper(object):
    def __init__(self, params):
        if __debug__:
            print("Wallpaper object created!")

        self.images = []
        self.load_images_from_folder(VALID_PATH)
        self.verbose = params.verbose

        if params.cycle_speed is None:
            self.vprint("Cycle speed not defined. Setting to 5 seconds.")
            self.cycle_speed = 5
        else:
            try:
                self.cycle_speed = int(params.cycle_speed)
            except ValueError:
                print("{} is not a valid cycle speed. Setting to default 5 seconds.".format(params.cycle_speed))

        for image in self.images:
            self.loadImage(image)
            self.vprint("Waiting for {} seconds".format(self.cycle_speed))
            time.sleep(self.cycle_speed)

    def load_images_from_folder(self, folder_path):
        """Loads folder images."""
        img_list = []

        try:
            img_list = os.listdir(folder_path)
        except FileNotFoundError:
            print("Can't find directory {}".format(folder_path))
        else:
            self.images = [os.path.join(folder_path, image) for image in img_list if self.is_valid_image_format(image)]

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

    def vprint(self, message):
        """Prints out the message only if program is run in verbose mode."""
        if self.verbose:
            print(message)