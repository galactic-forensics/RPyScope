"""GUI for RPyMicroscope."""

from datetime import datetime
import os
from pathlib import Path
import sys

from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QPushButton,
    QCheckBox,
    QMessageBox,
    QLabel,
    QLineEdit,
    QSlider,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QFrame,
    QShortcut,
    QErrorMessage,
    QComboBox,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QDoubleValidator, QKeySequence

from add_widgets import LineEditHistory
from pyqtconfig import ConfigManager, ConfigDialog, QSettingsManager
from microscope import Microscope


class MainWindowControls(QMainWindow):
    """Main Window with adjustments, etc. for Microscope GUI"""

    def __init__(self):
        # info variables
        self.version = "0.0.1"
        self.author = "Reto Trappitsch and Louis Linder"
        self.link = "https://github.com/galactic-forensics/RPyScope"

        print(
            f"Welcome to RPyScope!\n"
            f"Version: {self.version}\n"
            f"Authors: {self.author}\n"
            f"License: GPLv3\n"
            f"See {self.link} for more information."
        )

        # init and sizing
        super().__init__()
        self.left = 0
        self.top = 75
        self.width = 300
        self.height = 700
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("RPyScope")

        # Quit shortcut
        self.quit_sc = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.quit_sc.activated.connect(self.close)

        # Error messages
        self.error_dialog = QErrorMessage()
        self.error_dialog.setGeometry(5, 80, 300, 200)

        # Load Microscope interactions
        self.scope = Microscope()
        self.cam = self.scope.cam

        # Load settings
        self.load_settings()

        # colors
        self.col_green = "#DBFFD4"
        self.col_red = "#FFB6B6"

        # recording timer
        self.rec_timer_interval = 100  # interval of timing in msec
        self.rec_time_elapsed = 0
        self.rec_timer = QTimer()
        self.rec_timer.setInterval(self.rec_timer_interval)
        self.rec_timer.timeout.connect(self.recording_timer_check)

        # main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # layout
        layout = QVBoxLayout()  # main vbox layout
        main_widget.setLayout(layout)

        # Settings button
        self.settings_button = QPushButton("Settings [S]")
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setToolTip("Change some settings")
        self.settings_button.setShortcut("S")
        layout.addWidget(self.settings_button)

        # Brightness
        layout.addWidget(QLabel("Brightness [B]"))

        self.bright_slider = QSlider(Qt.Horizontal)
        self.bright_slider.setMinimum(0)
        self.bright_slider.setMaximum(100)
        self.bright_slider.valueChanged.connect(self.brightness_changed)

        self.bright_reset_button = QPushButton("default")
        self.bright_reset_button.clicked.connect(self.reset_bright)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.bright_slider)
        h_layout.addWidget(self.bright_reset_button)

        layout.addLayout(h_layout)

        self.bright_sc = QShortcut(QKeySequence("B"), self)
        self.bright_sc.activated.connect(self.bright_slider.setFocus)

        self.config.add_handler("brightness", self.bright_slider)

        # Contrast
        layout.addWidget(QLabel("Contrast [C]"))

        self.contr_slider = QSlider(Qt.Horizontal)
        self.contr_slider.setMinimum(-100)
        self.contr_slider.setMaximum(100)
        self.contr_slider.valueChanged.connect(self.contrast_changed)

        self.contr_reset_button = QPushButton("default")
        self.contr_reset_button.clicked.connect(self.reset_contr)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.contr_slider)
        h_layout.addWidget(self.contr_reset_button)

        layout.addLayout(h_layout)

        self.contr_sc = QShortcut(QKeySequence("C"), self)
        self.contr_sc.activated.connect(self.contr_slider.setFocus)

        self.config.add_handler("contrast", self.contr_slider)

        # Automatic exposure
        lbl = QLabel("Auto exposure:")
        self.auto_exp_checkbox = QCheckBox()
        self.auto_exp_checkbox.toggled.connect(self.auto_exposure)
        self.auto_exp_checkbox.setToolTip(
            "Enable or disable automatic exposure.\n"
            "See Section 3.5 in PiCamera documentation."
        )
        layout.addLayout(layout_horizontal([lbl, self.auto_exp_checkbox], align=True))

        self.config.add_handler("auto_exp", self.auto_exp_checkbox)

        # Resolution
        layout.addWidget(QLabel("Resolution (w x h) [Alt+R]"))

        self.res_input = QLineEdit()
        self.res_input.setToolTip("Set the resolution (width x height)")
        self.res_input.returnPressed.connect(self.res_input.clearFocus)

        self.res_reset_button = QPushButton("default")
        self.res_reset_button.clicked.connect(self.reset_resolution)

        layout.addLayout(
            layout_horizontal(
                [
                    self.res_input,
                    self.res_reset_button,
                ],
                align=True,
            )
        )
        self.reset_resolution()

        self.res_sc = QShortcut(QKeySequence("Alt+R"), self)
        self.res_sc.activated.connect(self.res_input.setFocus)

        self.config.add_handler("resolution", self.res_input)

        # Framerate
        layout.addWidget(QLabel("Framerate (fps) [Alt+F]"))

        self.fps_input = QLineEdit()
        self.fps_input.setToolTip(
            "Set the framerate for video\n" "recordings in frames per second."
        )
        self.fps_input.returnPressed.connect(self.fps_input.clearFocus)

        self.fps_reset_button = QPushButton("default")
        self.fps_reset_button.clicked.connect(self.reset_framerate)

        layout.addLayout(
            layout_horizontal(
                [
                    self.fps_input,
                    self.fps_reset_button,
                ],
                align=True,
            )
        )
        self.reset_framerate()

        self.res_sc = QShortcut(QKeySequence("Alt+F"), self)
        self.res_sc.activated.connect(self.fps_input.setFocus)

        self.config.add_handler("framerate", self.fps_input)

        # command window
        self.cmd_window_button = QPushButton("Command window [Alt+C]")
        self.cmd_window_button.clicked.connect(self.open_cmd_window)
        self.cmd_window_button.setToolTip("Open a command window")
        self.cmd_window_button.setShortcut("Alt+C")
        layout.addWidget(self.cmd_window_button)

        layout_hline(layout)

        # File path
        self.path_label = QLabel("File path [Alt+P]:")
        layout.addWidget(self.path_label)

        self.path_button = QPushButton("Browse")
        self.path_button.clicked.connect(self.set_path)

        layout.addLayout(
            layout_horizontal([self.path_label, self.path_button], align=True)
        )

        self.path_input = QLineEdit()
        self.path_input.setText(self.config.get("default_directory"))
        self.path_input.setToolTip(
            "Enter the path to your working directory. Files will be saved here."
        )
        self.path_input.returnPressed.connect(self.path_input.clearFocus)
        layout.addWidget(self.path_input)

        self.path_sc = QShortcut(QKeySequence("Alt+P"), self)
        self.path_sc.activated.connect(self.path_input.setFocus)

        self.config.add_handler("path", self.path_input)

        # File name date prefix
        self.date_prefix = False
        lbl = QLabel("Date prefix [D]:")
        self.date_prefix_checkbox = QCheckBox()
        self.date_prefix_checkbox.setChecked(False)
        self.date_prefix_checkbox.toggled.connect(self.set_date_prefix)
        self.date_prefix_checkbox.setToolTip(
            "Prefix all filenames with date and time\n"
            "yyyy-mm-dd_hh_mm_ss_microseconds_yourfilename.jpeg"
        )
        self.date_prefix_checkbox.setShortcut("D")
        layout.addLayout(
            layout_horizontal([lbl, self.date_prefix_checkbox], align=True)
        )

        self.config.add_handler("date_prefix", self.date_prefix_checkbox)

        # File name label
        self.fname_label = QLabel("File name [F]:")
        layout.addWidget(self.fname_label)

        # File name input
        self.fname_input = QLineEdit()
        self.fname_input.setToolTip(
            "Select a filename for your photo or video.\n"
            "The appropriate extension will be appended."
        )
        self.fname_input.returnPressed.connect(self.fname_input.clearFocus)
        layout.addWidget(self.fname_input)

        # File name shortcut
        self.fname_sc = QShortcut(QKeySequence("F"), self)
        self.fname_sc.activated.connect(self.fname_input.setFocus)

        self.config.add_handler("fname", self.fname_input)

        layout_hline(layout)

        # preview

        self.preview_button = QPushButton("Start Preview [P]")
        self.preview_button.clicked.connect(self.preview_cam)
        self.is_preview = False
        self.preview_button.setStyleSheet(f"background-color:{self.col_green}")
        self.preview_button.setToolTip(
            "Start / Stop the camera preview. The preview\n"
            "is directly drawn onto the display, bypassing\n"
            "the window manager. If it covers this program,\n"
            "you can change preview size and position in the\n"
            "settings."
        )
        self.preview_button.setShortcut("P")
        layout.addWidget(self.preview_button)

        layout_hline(layout)

        # video recording time

        layout.addWidget(QLabel("Recording Time in seconds [T]:"))
        self.rec_time = QLineEdit()
        self.rec_time.setValidator(QDoubleValidator(bottom=0))
        self.rec_time.setAlignment(Qt.AlignRight)
        self.rec_time.setToolTip(
            "Video recording time in seconds. If set\n"
            "to 0, will record until button is pressed again."
        )
        self.rec_time.returnPressed.connect(self.rec_time.clearFocus)
        layout.addWidget(self.rec_time)
        self.rec_time_sc = QShortcut(QKeySequence("T"), self)
        self.rec_time_sc.activated.connect(lambda: self.rec_time.setFocus())

        self.config.add_handler("rec_time", self.rec_time)

        # video recording

        self.rec_button = QPushButton("Start Recording [R]")
        self.rec_button.clicked.connect(self.record_video)
        self.rec_button.setStyleSheet(f"background-color:{self.col_green}")
        self.rec_button.setToolTip(
            "Record a video. Click to start and stop\n" "or set a timer (see above)."
        )
        self.rec_button.setShortcut("R")
        self.is_recording = False
        layout.addWidget(self.rec_button)

        layout_hline(layout)

        # image recording
        self.capture_button = QPushButton("Capture Image [Space]")
        self.capture_button.setShortcut("Space")
        self.capture_button.clicked.connect(self.capture_image)
        self.capture_button.setToolTip(
            "Capture an image. Can only\n" "be done when video is not recording."
        )
        self.capture_button.setShortcut("Space")
        layout.addWidget(self.capture_button)

        # open command line interface
        if self.config.get("open_cmd_startup"):
            self.open_cmd_window()

        # open preview
        if self.config.get("open_preview_startup"):
            self.preview_cam()

    # FUNCTIONS #
    def load_settings(self):
        default_settings = {
            "open_preview_startup": True,
            "open_cmd_startup": False,
            "preview_x": "310",
            "preview_y": "40",
            "preview_h": "900",
            "image_format": "jpeg",
            "video_format": "h264",
            "rotation": "0",
            "vflip": False,
            "hflip": False,
            # hidden settings
            "brightness": 50,
            "contrast": 0,
            "auto_exp": True,
            "resolution": "1920x1080",
            "framerate": "30",
            "path": os.path.expanduser("~/Desktop"),
            "date_prefix": False,
            "fname": "",
            "rec_time": "0",
        }

        default_settings_metadata = {
            "image_format": {
                "preferred_handler": QComboBox,
                "preferred_map_dict": {
                    "jpeg": "jpeg",
                    "png": "png",
                    "gif": "gif",
                    "bmp": "bmp",
                    "yuv": "yuv",
                    "rgb": "rgb",
                    "rgba": "rgba",
                    "bgr": "bgr",
                    "bgra": "bgra",
                },
            },
            "video_format": {
                "preferred_handler": QComboBox,
                "preferred_map_dict": {
                    "h264": "h264",
                    "mjpeg": "mjpeg",
                    "yuv": "yuv",
                    "rgb": "rgb",
                    "rgba": "rgba",
                    "bgr": "bgr",
                    "bgra": "bgra",
                },
            },
            "rotation": {
                "preferred_handler": QComboBox,
                "preferred_map_dict": {
                    "0": 0,
                    "90": 90,
                    "180": 180,
                    "270": 270,
                },
            },
            "brightness": {"prefer_hidden": True},
            "contrast": {"prefer_hidden": True},
            "auto_exp": {"prefer_hidden": True},
            "resolution": {"prefer_hidden": True},
            "framerate": {"prefer_hidden": True},
            "path": {"prefer_hidden": True},
            "date_prefix": {"prefer_hidden": True},
            "fname": {"prefer_hidden": True},
            "rec_time": {"prefer_hidden": True},
        }

        self.config = ConfigManager(
            default_settings,
            filename=os.path.expanduser("~/.config/rpyscope-config.json"),
        )
        self.config.set_many_metadata(default_settings_metadata)
        # apply rotations and flips
        self.update_config(self.config)

    def open_settings(self):
        config_dialog = ConfigDialog(self.config, self, cols=1)
        config_dialog.setWindowTitle("Settings")
        config_dialog.accepted.connect(lambda: self.update_config(config_dialog.config))
        config_dialog.exec()

    def update_config(self, update):
        self.config.set_many(update.as_dict())
        self.cam.rotation = update.get("rotation")
        self.cam.vflip = update.get("vflip")
        self.cam.hflip = update.get("hflip")
        self.config.save()

    def open_cmd_window(self):  # , top, height):
        cli = CommandLineScope(
            parent=self, top=self.top + self.height + 50, cam=self.cam
        )
        cli.show()

    def set_increment(self):
        if self.increment == True:
            self.increment = False
        else:
            self.increment = True

    def set_date_prefix(self):
        if self.date_prefix == True:
            self.date_prefix = False
        else:
            self.date_prefix = True

    def auto_exposure(self):
        """Turns automatic exposure of the camera on and off."""
        if self.auto_exp_checkbox.isChecked():
            self.scope.auto_exposure = True
        else:
            self.scope.auto_exposure = False

    def brightness_changed(self, val):
        """Change brightness to value"""
        self.cam.brightness = val

    def capture_image(self):
        fmt = self.config.get("image_format")
        if self.fname_ok() and self.path_ok():
            fname = self.make_filename_with_path() + "." + str(fmt)
            if not os.path.isfile(fname):
                self.set_resolution()
                self.cam.capture(
                    str(fname), format=fmt
                )  # specifying the format double checks that it is possible
                print("Image captured: " + str(fname))
            else:
                self.error_dialog.showMessage("Error: " + fname + "  already exists")

    def contrast_changed(self, val):
        """Change brightness to value"""
        self.cam.contrast = val

    def preview_cam(self):
        """Preview camera."""
        if not self.is_preview:  # not preview
            self.set_resolution()
            self.set_framerate()
            self.preview_button.setText("Stop Preview [P]")
            self.preview_button.setStyleSheet(f"background-color:{self.col_red}")
            (w_camera, h_camera) = self.cam.resolution
            aspect_ratio = w_camera / h_camera
            x = int(self.config.get("preview_x"))
            y = int(self.config.get("preview_y"))
            h = int(self.config.get("preview_h"))
            w = int(h * aspect_ratio)
            self.cam.start_preview(fullscreen=False, window=(x, y, w, h))
            self.is_preview = True
        else:
            self.preview_button.setText("Start Preview [P]")
            self.preview_button.setStyleSheet(f"background-color:{self.col_green}")
            self.cam.stop_preview()
            self.is_preview = False
        # Anytime text is changed, the shortcut is cleared. So specify it again.
        self.preview_button.setShortcut("P")

    def record_video(self):
        """Start and stop recording."""
        if not self.is_recording:  # not recording
            if self.fname_ok() and self.path_ok:
                fmt = self.config.get("video_format")
                fname = self.make_filename_with_path() + "." + str(fmt)
                if not os.path.isfile(fname):
                    self.set_resolution()
                    self.set_framerate()
                    self.rec_button.setText("Stop Recording [R]")
                    self.rec_button.setStyleSheet(f"background-color:{self.col_red}")
                    self.capture_button.setDisabled(True)

                    self.cam.start_recording(fname, format=fmt)

                    if (
                        self.rec_time.text().replace(" ", "") != ""
                    ):  # make sure not empty
                        if float(self.rec_time.text()) > 0:
                            self.rec_timer.start()

                    self.is_recording = True
                else:
                    self.error_dialog.showMessage(
                        "Error: " + fname + "  already exists"
                    )
        else:
            self.rec_button.setText("Start Recording [R]")
            self.rec_button.setStyleSheet(f"background-color:{self.col_green}")
            self.capture_button.setEnabled(True)

            self.cam.stop_recording()

            self.rec_timer.stop()
            self.rec_time_elapsed = 0.0  # reset elapsed time
            self.is_recording = False
        # Anytime text is changed, the shortcut is cleared. So specify it again.
        self.rec_button.setShortcut("R")

    def make_filename_with_path(self):
        fname_inp = self.fname_input.text()
        if self.date_prefix == True:
            prefix = str(datetime.now())
            fname_inp = prefix + "_" + fname_inp
        fname_inp = fname_inp.replace(".", "_")
        fname_inp = fname_inp.replace(":", "_")
        fname_inp = fname_inp.replace(" ", "_")
        path = Path(self.path_input.text())
        fname_inp = Path.joinpath(path, fname_inp)
        return str(fname_inp)

    def fname_ok(self):
        # check if the filename is not empty
        fname = self.fname_input.text()
        if len(fname) == 0 and self.date_prefix == False:
            self.error_dialog.showMessage(
                "Error: File name can't be empty if date prefix \
                is unchecked."
            )
            return False
        else:
            return True

    def path_ok(self):
        dir = self.path_input.text()
        if not os.path.isdir(dir):
            self.error_dialog.showMessage(
                "Error: The directory " + dir + " does not exist"
            )
            return False
        else:
            return True

    def recording_timer_check(self):
        """Check and stop the recording if elapsed time larger than total time."""
        self.rec_time_elapsed += self.rec_timer_interval / 1000  # add to elapsed time
        if self.rec_time_elapsed >= float(self.rec_time.text()):
            # click record video to stop it, since it is started right now...
            self.record_video()

    def reset_bright(self):
        self.bright_slider.setValue(self.config._get_default("brightness"))

    def reset_contr(self):
        self.contr_slider.setValue(self.config._get_default("contrast"))

    def set_path(self):
        """Set the recording path via QFileDialogue."""
        path = QFileDialog.getExistingDirectory(
            self, "Select Directory", self.path_input.text()
        )
        if path != "":
            self.path_input.setText(str(path))

    def reset_resolution(self):
        self.res_input.setText(self.config._get_default("resolution"))

    def set_resolution(self):
        new_res = self.res_input.text()
        if str(self.cam.resolution) != new_res:
            previous_resolution = self.cam.resolution
            try:
                self.cam.resolution = new_res
                print(f"resolution set to {new_res}.")
            except:
                print(f"resolution {new_res} not supported.")
                self.res_input.setText(str(previous_resolution))
                self.cam.resolution = previous_resolution

    def reset_framerate(self):
        self.fps_input.setText(self.config._get_default("framerate"))

    def set_framerate(self):
        new_fps = float(self.fps_input.text())
        if float(self.cam.framerate) != new_fps:
            previous_framerate = self.cam.framerate
            try:
                self.cam.framerate = new_fps
                print(f"framerate set to {new_fps} fps.")
            except:
                print(f"framerate {new_fps} fps not supported.")
                self.fps_input.setText(str(previous_framerate))
                self.cam.framerate = previous_framerate

    def closeEvent(self, event):
        print("\nHave a nice day :)")
        self.config.save()


class CommandLineScope(QMainWindow):
    """Command line interface for camera, which must be a PiCamera Interface."""

    def __init__(self, parent=None, top=0, cam=None):
        """Initialize the CLI.

        :param parent: parent class, defaults to None
        :type parent: Class
        :param top: Top adjuster, where to start, in px, defaults to 0
        :type top: int
        """
        super().__init__(parent)

        self.parent = parent
        self.cam = cam

        # Exit shortcut
        self.quit_sc = QShortcut(QKeySequence("Ctrl+W"), self)
        self.quit_sc.activated.connect(self.close)

        # CLI _history
        self.history = []
        self.history_counter = 0

        left = 0
        width = 800
        height = 0
        self.setGeometry(left, top, width, height)
        self.setWindowTitle("PiCamera CLI")

        self.cli_edit = LineEditHistory()
        self.cli_edit.returnPressed.connect(self.cli_return_pressed)
        self.cli_edit.setToolTip(
            "Command Line Interface for camera settings.\n"
            "Please refer to PiCamera documentation. Here,\n"
            "if `cam = PiCamera()`, then you would enter\n"
            "the command you would attach to `cam.`.\n\n"
            "For example, if you would like to change `iso`,\n"
            "type `iso = 100` and the microscope software\n"
            "will send the command `cam.iso = 100`."
        )

        self.setCentralWidget(self.cli_edit)

        if cam is None:
            print("No camera defined!")

    def cli_return_pressed(self):
        """Return pressed in CLI."""
        # get command and clear
        cmd = self.cli_edit.text()

        # no command given
        if cmd == "":
            return

        # camera directly is called `cam` -> add a `self`
        oldcmd = str(cmd)
        cmd = cmd.replace("cam.", "rpyscope_app.cam.")

        try:
            exec(f"{cmd}")
            # append to _history and clear field
            self.cli_edit.add_to_history(oldcmd)  # attach the old, unmodified command
            self.cli_edit.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)


#  HELPER FUNCTIONS #


def layout_hline(layout):
    """Add a horizontal line to a layout."""
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Sunken)
    layout.addWidget(line)


def layout_horizontal(items, align):
    """Add items to QHBoxLayout and return the layout.

    :param items: List of all Widgets
    :type items: List(QtWidgets)

    :return: Layout Hertically aligned
    :rtype: Qt.QHBoxLayout
    """
    layout = QHBoxLayout()
    if align == True:
        for i in range(len(items) - 1):
            layout.addWidget(items[i])
            layout.addStretch()
        layout.addWidget(items[-1])
    else:
        layout.addStretch()
        for item in items:
            layout.addWidget(item)
            layout.addStretch()
    return layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    rpyscope_app = MainWindowControls()
    rpyscope_app.show()

    sys.exit(app.exec_())
