import os
import sys
from . import wallpaper
import argparse


class App(object):

    def __init__(self, args):
        # Print received arguments.
        self.params = args
        self.run()


    def run(self):
        wp = wallpaper.Wallpaper(self.params)
        wp.run()


