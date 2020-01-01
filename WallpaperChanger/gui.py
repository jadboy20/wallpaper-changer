import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QFileDialog, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from . import config


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
        self.config = config.Config()
        print(str(self.config))

        self.form = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create a vbox
        vbox = QVBoxLayout()

        # Create the cycle speed text box
        vbox.addLayout(self.create_label_lineedit_pair("cycle-speed",
                                                       "Cycle Speed",
                                                       tool_tip="Number of seconds each image stays as the background."))

        vbox.addLayout(self.create_label_lineedit_pair("gallery-directory",
                                                       "Gallery Directory",
                                                       has_file_dialog=True,
                                                       read_only=True))

        vbox.addWidget(self.create_checkbox("randomise-checkbox",
                                            "Randomise?",
                                            tool_tip="Randomly select each image in the gallery directory.",
                                            callback=self.randomise_checkbox_callback))

        vbox.addWidget(self.create_button("set-button", "Set Configuration",
                                          self.button_callback))

        vbox.addWidget(self.create_error_text("error-text"))


        self.setLayout(vbox)
        self.show()

    def create_label_lineedit_pair(self, name, title, tool_tip="", has_file_dialog=False, read_only=False):
        hbox = QHBoxLayout()
        self.form[name] = {}
        self.form[name]["label"] = QLabel(title)
        self.form[name]["textbox"] = QLineEdit()
        self.form[name]["textbox"].setToolTip(tool_tip)

        hbox.addWidget(self.form[name]["label"])
        hbox.addWidget(self.form[name]["textbox"])

        if has_file_dialog:
            open_file_dialog_btn = self.create_button("open-file-dialog-btn", "...", self.get_directory_name)
            hbox.addWidget(open_file_dialog_btn)

        if read_only:
            self.form[name]["textbox"].setDisabled(True)

        return hbox

    def create_checkbox(self, name, title, tool_tip="", callback=None):
        self.form[name] = QCheckBox(title)
        self.form[name].setToolTip(tool_tip)

        if callback is not None:
            self.form[name].stateChanged.connect(callback)

        return self.form[name]

    def randomise_checkbox_callback(self, state):
        self.config.randomise = state

    def create_button(self, name, title, callback=None):
        button = QPushButton(title)
        self.form[name] = button
        if callback is not None:
            button.clicked.connect(callback)

        return button

    def create_error_text(self, name):
        error_text = QLabel()
        self.form[name] = error_text

        return error_text

    def set_error_text(self, text):
        self.form["error-text"].setText(text)

    def get_directory_name(self):
        directory = str(QFileDialog.getExistingDirectory())
        self.form['gallery-directory']['textbox'].setText(directory)

    def validate_input(self):
        """Validate form input.

        :return:    Nothing
        """
        # Cycle Speed
        errors = []
        error_msg = self.validate_cycle_speed()
        if error_msg is not None:
            errors.append(error_msg)

        # Gallery Directory
        error_msg = self.validate_gallery_directory()
        if error_msg is not None:
            errors.append(error_msg)

        return errors

    def validate_cycle_speed(self):
        """Check that cycle speed is valid.

        :return:    None if valid. Error string if not valid. Error string contains message to suggest what the user
                    should correct.
        """
        try:
            value = int(self.form["cycle-speed"]["textbox"].text())
        except ValueError:
            return "Cycle speed is not a valid integer."

        try:
            self.config.cycle_speed = value
        except ValueError as e:
            return str(e)

        return None

    def validate_gallery_directory(self):
        """Check that gallery directory exits

        :return:
        """
        value = self.form['gallery-directory']['textbox'].text()
        if len(value) == 0:
            return "No gallery directory was chosen!"

        self.config.gallery_directory = value

    @pyqtSlot()
    def button_callback(self):
        errors = self.validate_input()
        if len(errors) > 0:
            self.set_error_text(errors[0])
        else:
            self.send_config()

    def send_config(self):
        """Send the config to the wallpaper changer.

        :return:
        """
        print(str(self.config))
