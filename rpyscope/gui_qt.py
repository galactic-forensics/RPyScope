"""GUI for RPyMicroscope."""

import time
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
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QDoubleValidator


class MainWindowControls(QMainWindow):
    """Main Window with adjustments, etc. for Microscope GUI"""

    def __init__(self):
        # info variables
        self.version = "0.0.1"
        self.author = "Reto Trappitsch"

        # init and sizing
        super().__init__()
        left = 0
        top = 75
        width = 180
        height = 500
        self.setGeometry(left, top, width, height)
        self.setWindowTitle("RPyScope")

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

        # Brightness & Contrast Labels
        blabel = QLabel("Brightness")
        font_center_bold(blabel)
        clabel = QLabel("Contrast")
        font_center_bold(clabel)
        layout.addLayout(layout_horizontal([blabel, clabel]))

        # Sliders
        self.bright_slider = QSlider(Qt.Vertical)
        self.contr_slider = QSlider(Qt.Vertical)
        self.setup_sliders()
        layout.addLayout(layout_horizontal([self.bright_slider, self.contr_slider]))
        self.reset_bright_contr_button = QPushButton("Reset B/C")
        self.reset_bright_contr_button.clicked.connect(self.reset_bright_contr)
        self.reset_bright_contr_button.setToolTip("Reset brightness and contrast.")
        layout.addWidget(self.reset_bright_contr_button)

        # automatic exposure
        lbl = QLabel("Auto exposure:")
        self.auto_exp_checkbox = QCheckBox()
        self.auto_exp_checkbox.setChecked(True)
        self.auto_exp_checkbox.toggled.connect(self.set_auto_exposure)
        self.auto_exp_checkbox.setToolTip(
            "Enable or disable automatic exposure.\n"
            "See Section 3.5 in PiCamera documentation."
        )
        layout.addLayout(layout_horizontal([lbl, self.auto_exp_checkbox]))

        layout_hline(layout)

        # file management
        self.path_button = QPushButton("Set Recording Path")
        self.path_button.clicked.connect(self.select_path)
        self.path_button.acceptDrops()
        self.path_button.setToolTip(
            "Select the path where images and videos\n" "will be stored."
        )
        layout.addWidget(self.path_button)
        layout.addWidget(QLabel("File name:"))
        self.fname_input = QLineEdit()
        self.fname_input.setToolTip(
            "Select a filename. This will be appended\n" "to a time and date stamp."
        )
        layout.addWidget(self.fname_input)

        layout_hline(layout)

        # preview

        self.preview_button = QPushButton("Start Preview")
        self.preview_button.clicked.connect(self.preview_cam)
        self.is_preview = False
        self.preview_button.setStyleSheet(f"background-color:{self.col_green}")
        self.preview_button.setToolTip(
            "Start / Stop the video preview. The preview\n"
            "is directly managed by the RPi and is sent\n"
            "directly to your GPU. You might not see this\n"
            "program anymore, which could be an issue."
        )
        layout.addWidget(self.preview_button)

        layout_hline(layout)

        # video recording

        layout.addWidget(QLabel("Recording Time (s):"))
        self.rec_time = QLineEdit()
        self.rec_time.setValidator(QDoubleValidator(bottom=0))
        self.rec_time.setAlignment(Qt.AlignRight)
        self.rec_time.setText("0")
        self.rec_time.setToolTip(
            "Video recording time in seconds. If set\n"
            "to 0, will record until button is pressed again."
        )
        layout.addWidget(self.rec_time)
        self.rec_button = QPushButton("Start Recording")
        self.rec_button.clicked.connect(self.record_video)
        self.rec_button.setStyleSheet(f"background-color:{self.col_green}")
        self.rec_button.setToolTip(
            "Record a video. Click to start and stop\n" "or set a timer (see above)."
        )
        self.is_recording = False
        layout.addWidget(self.rec_button)

        layout_hline(layout)

        # image recording
        self.capture_button = QPushButton("Capture Image")
        self.capture_button.clicked.connect(self.capture_image)
        self.capture_button.setToolTip(
            "Capture an image. Can currently only\n" "be done if video is not recorded."
        )
        layout.addWidget(self.capture_button)

        # open command line interface
        cli = CommandLineScope(parent=self, top=top + height + 50)
        cli.show()

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

    def brightness_changed(self, val):
        """Change brightness to value"""
        # todo
        print(val)

    def capture_image(self):
        """Capture an image."""
        pass
        # todo capture an image

    def contrast_changed(self, val):
        """Change brightness to value"""
        # todo
        print(val)

    def preview_cam(self):
        """Preview camera."""
        if not self.is_preview:  # not preview
            self.preview_button.setText("Stop Preview")
            self.preview_button.setStyleSheet(f"background-color:{self.col_red}")
            # todo action
            self.is_preview = True
        else:
            self.preview_button.setText("Start Preview")
            self.preview_button.setStyleSheet(f"background-color:{self.col_green}")
            # todo action
            self.is_preview = False

    def record_video(self):
        """Start and stop recording."""
        if not self.is_recording:  # not recording
            self.rec_button.setText("Stop Recording")
            self.rec_button.setStyleSheet(f"background-color:{self.col_red}")
            self.capture_button.setDisabled(True)

            # todo action to start recording

            if self.rec_time.text().replace(" ", "") != "":  # make sure not empty
                if float(self.rec_time.text()) > 0:
                    self.rec_timer.start()

            self.is_recording = True
        else:
            self.rec_button.setText("Start Recording")
            self.rec_button.setStyleSheet(f"background-color:{self.col_green}")
            self.capture_button.setEnabled(True)

            # todo action to stop recording

            self.rec_timer.stop()
            self.rec_time_elapsed = 0.0  # reset elapsed time
            self.is_recording = False

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

    def select_path(self):
        """Set the recording path via QFileDialogue."""
        path = QFileDialog.getExistingDirectory(self, "Select Directory", "~")
        print(path)
        # todo set path to class

    def set_auto_exposure(self):
        """Turns automatic exposure of the camera on and off."""
        if self.auto_exp_checkbox.isChecked():
            # todo action
            print("auto_exp on")
        else:
            print("auto_exp off")


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

        # CLI history
        self.history = []
        self.history_counter = 0

        left = 0
        width = 800
        height = 0
        self.setGeometry(left, top, width, height)
        self.setWindowTitle("PiCamera CLI")

        self.cli_edit = QLineEdit()
        # todo implement command line history
        # self.cli_edit.keyPressEvent().connect(lambda x: self.key_press_event(x))
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

    def browse_history(self):
        """Browse the history."""
        # todo
        pass

    def cli_return_pressed(self):
        """Return pressed in CLI."""
        # get command and clear
        cmd = self.cli_edit.text()
        self.cli_edit.clear()

        # camera directly is called `cam` -> add a `self`
        if cmd[:4] == "cam.":
            cmd = f"rpyscope_app.{cmd}"

        try:
            eval(f"{cmd}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e), QMessageBox.Ok)

    def key_press_event(self, val):
        """Handle key press events -> go to history for arrow up and down."""
        print(val)
        # todo for command line history


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


def layout_horizontal(items):
    """Add items to QHBoxLayout and return the layout.

    :param items: List of all Widgets
    :type items: List(QtWidgets)

    :return: Layout Hertically aligned
    :rtype: Qt.QHBoxLayout
    """
    layout = QHBoxLayout()
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
