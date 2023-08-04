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
    QShortcut
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
        self.author = "Reto Trappitsch"

        # init and sizing
        super().__init__()
        self.left = 0
        self.top = 75
        self.width = 300
        self.height = 700
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("RPyScope")

        # Quit shortcut
        self.quit_sc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quit_sc.activated.connect(sys.exit)

        # Load settings
        default_settings = {
            "open_preview_startup": True,
            "open_cmd_startup": False,
            "preview_x" : "310",
            "preview_y" : "40",
            "preview_h" : "900"
        }

        # note: the filename is relative to your location,
        # where you are executing gui_qt.py from
        self.config = ConfigManager(default_settings, filename="rpyscope-config.json")

        # Load Microscope interactions
        self.scope = Microscope()
        self.cam = self.scope.cam

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

        # Brightness & Contrast Labels
        blabel = QLabel("Brightness")
        font_center_bold(blabel)
        clabel = QLabel("Contrast")
        font_center_bold(clabel)
        layout.addLayout(layout_horizontal([blabel, clabel], align=False))

        # Sliders
        self.bright_slider = QSlider(Qt.Vertical)
        self.contr_slider = QSlider(Qt.Vertical)
        self.setup_sliders()
        layout.addLayout(layout_horizontal([self.bright_slider, self.contr_slider], align=False))
        self.reset_bright_contr_button = QPushButton("Reset B/C")
        self.reset_bright_contr_button.clicked.connect(self.reset_bright_contr)
        self.reset_bright_contr_button.setToolTip("Reset brightness and contrast.")
        layout.addWidget(self.reset_bright_contr_button)

        # automatic exposure
        lbl = QLabel("Auto exposure:")
        self.auto_exp_checkbox = QCheckBox()
        self.auto_exp_checkbox.setChecked(True)
        self.auto_exp_checkbox.toggled.connect(self.auto_exposure)
        self.auto_exp_checkbox.setToolTip(
            "Enable or disable automatic exposure.\n"
            "See Section 3.5 in PiCamera documentation."
        )
        layout.addLayout(layout_horizontal([lbl, self.auto_exp_checkbox], align=True))

        # command window
        self.cmd_window_button = QPushButton("Command window [C]")
        self.cmd_window_button.clicked.connect(self.open_cmd_window)
        self.cmd_window_button.setToolTip("Open a command window")
        self.cmd_window_button.setShortcut("C")
        layout.addWidget(self.cmd_window_button)

        layout_hline(layout)

        # File path
        self.path_button = QPushButton("Set Recording Path [Ctrl+P]")
        self.path_button.clicked.connect(self.set_path)
        self.path_button.acceptDrops()
        self.path_button.setToolTip(
            "Select the path where images and videos\n" "will be stored."
        )
        self.path_button.setShortcut("Ctrl+P")
        layout.addWidget(self.path_button)
        
        # File name increment
        self.increment = False
        lbl = QLabel("Increment filename [I]:")
        self.increment_checkbox = QCheckBox()
        self.increment_checkbox.setChecked(False)
        self.increment_checkbox.toggled.connect(self.set_increment)
        self.increment_checkbox.setToolTip(
            "If the filename ends with a number\n"
            "increment that number after every picture or recording"
        )
        self.increment_checkbox.setShortcut("I")
        layout.addLayout(layout_horizontal([lbl, self.increment_checkbox], align=True))

        # File name date prefix
        self.date_prefix = False
        lbl = QLabel("Date prefix [D]:")
        self.date_prefix_checkbox = QCheckBox()
        self.date_prefix_checkbox.setChecked(False)
        self.date_prefix_checkbox.toggled.connect(self.set_date_prefix)
        self.date_prefix_checkbox.setToolTip(
            "Prefix all filenames with date and time\n"
            "yyyy-mm-dd_time.microseconds_yourfilename.jpeg"
        )
        self.date_prefix_checkbox.setShortcut("D")
        layout.addLayout(layout_horizontal([lbl, self.date_prefix_checkbox], align=True))

        # File name label
        self.fname_label = QLabel("File name [F]:")
        layout.addWidget(self.fname_label)

        # File name input
        self.fname_input = QLineEdit()
        self.fname_input.setToolTip(
            "Select a filename. This will be appended\n" "to a time and date stamp."
        )
        self.fname_input.returnPressed.connect(self.fname_input.clearFocus)
        layout.addWidget(self.fname_input)

        # File name shortcut
        self.fname_sc = QShortcut(QKeySequence('F'), self)
        self.fname_sc.activated.connect(self.fname_input.setFocus)

        layout_hline(layout)

        # preview

        self.preview_button = QPushButton("Start Preview [P]")
        self.preview_button.clicked.connect(self.preview_cam)
        self.is_preview = False
        self.preview_button.setStyleSheet(f"background-color:{self.col_green}")
        self.preview_button.setToolTip(
            "Start / Stop the video preview. The preview\n"
            "is directly managed by the RPi and is sent\n"
            "directly to your GPU. You might not see this\n"
            "program anymore, which could be an issue."
        )
        self.preview_button.setShortcut("P")
        layout.addWidget(self.preview_button)

        layout_hline(layout)

        # video recording time

        layout.addWidget(QLabel("Recording Time in seconds [T]:"))
        self.rec_time = QLineEdit()
        self.rec_time.setValidator(QDoubleValidator(bottom=0))
        self.rec_time.setAlignment(Qt.AlignRight)
        self.rec_time.setText("0")
        self.rec_time.setToolTip(
            "Video recording time in seconds. If set\n"
            "to 0, will record until button is pressed again."
        )
        self.rec_time.returnPressed.connect(self.rec_time.clearFocus)
        layout.addWidget(self.rec_time)
        self.rec_time_sc = QShortcut(QKeySequence('T'), self)
        self.rec_time_sc.activated.connect(lambda : self.rec_time.setFocus())

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
            "Capture an image. Can currently only\n" "be done if video is not recorded."
        )
        self.capture_button.setShortcut("Space")
        layout.addWidget(self.capture_button)

        # open command line interface
        if self.config.get("open_cmd_startup"):
            self.open_cmd_window()
        
        # open preview
        if self.config.get("open_preview_startup"):
            self.preview_cam()

    # SETUP #

    def setup_sliders(self):
        """Setup for the sliders and all connects, etc."""
        # brightness slider
        self.bright_slider.setMinimum(0)
        self.bright_slider.setMaximum(100)
        self.bright_slider.setValue(50)
        self.bright_slider.valueChanged.connect(lambda x: self.brightness_changed(x))

        # contrast slider
        self.contr_slider.setMinimum(-100)
        self.contr_slider.setMaximum(100)
        self.contr_slider.setValue(0)
        self.contr_slider.valueChanged.connect(lambda x: self.contrast_changed(x))

    # FUNCTIONS #

    def open_settings(self):
        config_dialog = ConfigDialog(self.config, self, cols=1)
        config_dialog.setWindowTitle("Settings")
        config_dialog.accepted.connect(lambda: self.update_config(config_dialog.config))
        config_dialog.exec()
    
    def update_config(self, update):
        self.config.set_many(update.as_dict())
        self.config.save()

    def open_cmd_window(self):#, top, height):
            cli = CommandLineScope(parent=self, top=self.top + self.height + 50, cam=self.cam)
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
        fmt = self.scope.image_format
        fname = self.make_filename() + "." + str(fmt)
        self.cam.capture(
            str(fname), format=fmt
        )  # specifying the format double checks that it is possible

    def contrast_changed(self, val):
        """Change brightness to value"""
        self.cam.contrast = val

    def preview_cam(self):
        """Preview camera."""
        if not self.is_preview:  # not preview
            self.preview_button.setText("Stop Preview [P]")
            self.preview_button.setStyleSheet(f"background-color:{self.col_red}")
            (w_camera,h_camera) = self.cam.resolution
            aspect_ratio = w_camera / h_camera
            x = int(self.config.get("preview_x"))
            y = int(self.config.get("preview_y"))
            h = int(self.config.get("preview_h"))
            w = int(h * aspect_ratio)
            self.cam.start_preview(fullscreen=False, window=(x,y,w,h))
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
            self.rec_button.setText("Stop Recording [R]")
            self.rec_button.setStyleSheet(f"background-color:{self.col_red}")
            self.capture_button.setDisabled(True)

            fmt = self.scope.video_format
            fname = self.make_filename() + "." + str(fmt)
            self.cam.start_recording(str(fname), format=fmt)

            if self.rec_time.text().replace(" ", "") != "":  # make sure not empty
                if float(self.rec_time.text()) > 0:
                    self.rec_timer.start()

            self.is_recording = True
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
    
    def make_filename(self):
        #fname_inp = self.fname_input.text()
        fname_inp = self.fname_input.text()
        if self.increment:
            #discard extension
            initial_fname = fname_inp.split('.')[0]
            try:
                n = int(initial_fname[-1])
                new_file = initial_fname[0:-1] + str(n+1)
                self.fname_input.setText(new_file)
            except:
                pass
        # if fname_inp != "":
        #     fname_inp = f"_{fname_inp}"  # add underscore
        #if the filename is empty, add a date anyway
        if self.date_prefix == True or fname_inp == "":
            fname_inp = f"{str(datetime.now())}_{fname_inp}"
        fname_inp = Path.joinpath(
            self.scope.home_folder,
            fname_inp.replace(" ", "_"),
        )
        return str(fname_inp)


    def recording_timer_check(self):
        """Check and stop the recording if elapsed time larger than total time."""
        self.rec_time_elapsed += self.rec_timer_interval / 1000  # add to elapsed time
        if self.rec_time_elapsed >= float(self.rec_time.text()):
            # click record video to stop it, since it is started right now...
            self.record_video()

    def reset_bright_contr(self):
        """Reset brightness and contrast slider."""
        self.bright_slider.setValue(50)
        self.contr_slider.setValue(0)

    def set_path(self):
        """Set the recording path via QFileDialogue."""
        path = QFileDialog.getExistingDirectory(self, "Select Directory", "~")
        if path != "":
            self.scope.home_folder = Path(path)


class CommandLineScope(QMainWindow):
    """Command line interface for camera, which must be a PiCamera Interface."""

    def __init__(self, parent=None, top=0, cam=None):
        """Initialize the CLI.

        :param parent: parent class, defaults to None
        :type parent: Class
        :param top: Top adjuster, where to start, in px, defaults to 0
        :type top: int
        """
        super(CommandLineScope, self).__init__(parent)

        self.parent = parent
        self.cam = cam

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


def font_center_bold(lbl):
    """Sets a QLabel Centered and bold.

    :param lbl: Label
    :type lbl: QLabel

    :return: None
    """
    font = QFont()
    font.setBold(True)
    lbl.setAlignment(Qt.AlignCenter)
    lbl.setFont(font)


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
    if align==True:
        for i in range(len(items)-1):
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
