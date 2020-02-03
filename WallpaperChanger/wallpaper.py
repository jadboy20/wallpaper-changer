import os
import sys
import ctypes
import traceback
import time
import random
import logging
from . import config
from . import WALLPAPER_DEFAULT_DIR, WALLPAPER_DEFAULT_CACHE
from .scraper import scraper

VALID_PATH = "C:\\users\\james\\pictures"
INVALID_PATH = "C:\\hello"

DEFAULT_GALLERY = os.path.join("c:\\", "users", "james", "pictures")


class Wallpaper(object):
    def __init__(self, params):
        # Copy over argument parameters.
        self.verbose = params.verbose
        self.gallery_directory = params.gallery_directory
        self.randomise = params.randomise
        self.config = config.Config()

        # Load the config file.
        if params.configuration_path is None:
            # Load the config file from the filename "./wallpaper.conf"
            try:
                self.config.filename = r".\wallpaper.conf"
                self.config.load_config()

                # Copy over the parameters from the config to the class
                # members
                self.randomise = self.config.randomise
                self.gallery_directory = self.config.gallery_directory
                self.online_mode = self.config.online_mode
                self.query = self.config.query
                self.download_cap = self.config.download_cap

            except EnvironmentError as e:
                logging.warning("{}. Creating a default configuration file at '{}'".format(str(e), self.config.filename))
                self.config.save_config()

        # Set cycle_speed from argument if available. Otherwise, set it to 5 seconds.
        if params.cycle_speed is None:
            self.vprint("Cycle speed not defined. Setting to 5 seconds.", level=logging.WARNING)
            self.cycle_speed = self.config.cycle_speed
        else:
            try:
                self.cycle_speed = int(params.cycle_speed)
            except ValueError:
                print("{} is not a valid cycle speed. Setting to default 5 seconds.".format(params.cycle_speed))

        # Default gallery directory to C:/users/user/pictures if no parameter is given.
        if self.gallery_directory is None:
            self.vprint("Gallery directory not defined. Setting gallery directory to '{}' ".format(DEFAULT_GALLERY), level=logging.WARNING)
            self.gallery_directory = self.config.gallery_directory

        # Check if directory exists.
        if not os.path.isdir(self.gallery_directory):
            self.vprint("Could not find '{}'! Check the gallery directory. Exiting program!".format(self.gallery_directory), level=logging.WARNING)
            sys.exit(1)

        # Check if in online mode. This will use images obtain from online rather than images in custom gallery.
        if self.online_mode:
            self.vprint("Online mode has been enabled. Online images will be stored in {}".format(WALLPAPER_DEFAULT_DIR))
            self.gallery_directory = WALLPAPER_DEFAULT_DIR

            # Get the images from online first and store them to the cache
            s = scraper.HipWallpaperScraper()
            results = s.search(self.query, num_results=self.download_cap)
            s.write_images_to_file(results, WALLPAPER_DEFAULT_CACHE)

            # Start downloading images from the cache.
            s.download_images(WALLPAPER_DEFAULT_CACHE, WALLPAPER_DEFAULT_DIR)

        # Start program
        self.images = []
        self.load_images_from_folder(self.gallery_directory)

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
                self.vprint("'{}' loaded.".format(img_path))
                ctypes.windll.user32.SystemParametersInfoW(
                    SPI_SETDESKWALLPAPER, 0, img_path, 3)
            except Exception:
                print(traceback.format_exc())
        else:
            self.vprint("'{}' does not exist!".format(img_path), level=logging.WARNING)

    def vprint(self, message, level=logging.INFO):
        """Prints out the message only if program is run in verbose mode.

        Always prints to log.
        """
        message = str(message)
        if self.verbose:
            print(message)

        # Print as string incase message is passed as a non-string.
        logging.log(level=level, msg=str(message))

    def run(self):
        if self.randomise:
            self.vprint("Random playback selected.")
            # Seed a random selection.
            random.seed()

            # Pick images out randomly, rather than in the order they are
            # in the directory.
            prev_num = -1

            while True:
                # Pick a number, any number!
                rand_num = random.randint(0, len(self.images) - 1)
                # Only pick number if its not the same as the last.
                # This will prevent similar images being displayed
                # consecutively, thus giving the illusion of randomness.
                if prev_num != rand_num:
                    # Possibly (but very unlikely) that will be out of range!
                    try:
                        self.loadImage(self.images[rand_num])
                    except IndexError:
                        self.vprint("Random number {} not in array range!".format(rand_num), level=logging.WARNING)
                    else:
                        time.sleep(self.cycle_speed)
                    prev_num = rand_num
        else:
            self.vprint("Standard playback selected.")
            while True:
                for image in self.images:
                    self.loadImage(image)
                    self.vprint("Waiting for {} seconds".format(self.cycle_speed))
                    time.sleep(self.cycle_speed)
