import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class Gui(object):
    def __init__(self):
        pass

    def run(self):
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())


class App(QWidget):
    def __init__(self):
        super().__init__()
        logging.info("In Gui constructor")
        self.title = "Wallpaper Changer GUI"
        self.left = 50
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
