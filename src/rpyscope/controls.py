# Main Control GUI

from pathlib import Path

from qtpy import QtCore, QtGui, QtWidgets
import pyqtconfig

from rpyscope.camera import PiCamHQ
from rpyscope.preview import PreviewWindow
import rpyscope.utils as ut


class MicroscopeControls(QtWidgets.QMainWindow):
    """Main window for controls of the microscope."""

    def __init__(self) -> None:
        """Initialize the control GUI."""
        super().__init__(parent=None)

        # Styling

        # GUI widgets
        self.img_timelapse_duration_unit = None
        self.img_timelapse_duration = None
        self.img_record_button = None
        self.img_timelapse_time_unit = None
        self.img_timelapse_time = None
        self.img_resolution = None
        self.mov_record_button = None
        self.mov_rec_time_unit = None
        self.file_name_input = None
        self.path_label = None
        self.mov_rec_time = None
        self.mov_framerate = None
        self.mov_resolution = None

        # Window styling
        left = 0
        top = 0
        width = 300
        height = 500
        self.setWindowTitle("Control")

        # settings manager for the program
        self.config = None
        self.settings_load()

        # setup defaults for program
        self._date_prefix = True
        self._timelapse = False
        self._movie_is_recording = False
        self._timelapse_is_recording = False
        self._timelapse_counter = 0

        # timers
        self._movie_timer = QtCore.QTimer()
        self._movie_timer.timeout.connect(self.record_movie)
        self._timelapse_timer = QtCore.QTimer()
        self._timelapse_timer.timeout.connect(self._capture_timelapse_image)

        # setup camera and start preview
        self.cam = PiCamHQ(
            control=self,
            hflip=self.config.get("Flip horizontally"),
            vflip=self.config.get("Flip vertically"),
        )

        self.preview = PreviewWindow(
            self.cam.cam,
            parent=self,
        )
        self.preview.qpicamera2.done_signal.connect(self.cam.capture_done)
        self.cam.cam.start()

        self.init_ui()

        self.preview.show()
        self.setGeometry(left, top, width, height)
        self.show()

    def init_ui(self):
        """Initialize the user interface."""
        title_font = QtGui.QFont()
        title_font.setBold(True)

        def center_me(element) -> QtWidgets.QHBoxLayout:
            """Takes an element and centers it in a QHbBoxLayout."""
            tmp = QtWidgets.QHBoxLayout()
            tmp.addStretch()
            tmp.addWidget(element)
            tmp.addStretch()
            return tmp

        def label_element_layout(
            label: str, element: [list, any]
        ) -> QtWidgets.QHBoxLayout:
            """Create a label on left, element(s) on right layout.

            :param label: String to label on the right with. If None, omit.
            :param element(s): One or multiple elements (as list) to add on left.
            """
            tmp = QtWidgets.QHBoxLayout()
            if label is not None:
                tmp.addWidget(QtWidgets.QLabel(label))
                tmp.addStretch()
            if isinstance(element, list):
                for ele in element:
                    tmp.addWidget(ele)
            else:
                tmp.addWidget(element)
            return tmp

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(layout)

        # set quit shortcut to Ctrl+Q
        quit_sc = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
        quit_sc.activated.connect(self.close)

        title_lbl = QtWidgets.QLabel("RPyScope")
        title_lbl.setFont(title_font)
        layout.addLayout(center_me(title_lbl))

        # SETTINGS AND INFO
        htmp = QtWidgets.QHBoxLayout()

        info_button = QtWidgets.QPushButton("Info")
        info_button.setToolTip("Display info about the camera.")
        info_button.clicked.connect(lambda: ut.CameraInfo(self.cam, self).exec)
        htmp.addWidget(info_button)
        htmp.addStretch()

        preview_button = QtWidgets.QPushButton("Preview")
        preview_button.setToolTip("Show preview again if it was closed.")
        preview_button.clicked.connect(self.preview.show)
        htmp.addWidget(preview_button)
        htmp.addStretch()

        settings_button = QtWidgets.QPushButton("Settings")
        settings_button.clicked.connect(self.settings_dialog)
        settings_button.setToolTip("Change program settings")
        htmp.addWidget(settings_button)
        layout.addLayout(htmp)

        # FILE NAME
        fn_lbl = QtWidgets.QLabel("Filename and path")
        fn_lbl.setFont(title_font)
        layout.addLayout(center_me(fn_lbl))

        self.path_label = QtWidgets.QLabel(self.config.get("user_path"))
        self.path_label.setToolTip("Current path files are stored in.")
        path_set_button = QtWidgets.QPushButton("Set Path", maximumWidth=150)
        path_set_button.clicked.connect(self.set_user_path)
        path_set_button.setToolTip("Set path to store files to.")
        tmp_layout = QtWidgets.QHBoxLayout()
        tmp_layout.addWidget(path_set_button)
        tmp_layout.addStretch()
        tmp_layout.addWidget(self.path_label)
        layout.addLayout(tmp_layout)

        self.file_name_input = QtWidgets.QLineEdit(minimumWidth=200)
        layout.addLayout(label_element_layout("Filename", self.file_name_input))
        date_prefix_chkbox = QtWidgets.QCheckBox()
        date_prefix_chkbox.setToolTip("Prefix the filename with current date?")
        date_prefix_chkbox.setChecked(self._date_prefix)
        date_prefix_chkbox.stateChanged.connect(lambda x: self._set_date_prefix(x))
        layout.addLayout(label_element_layout("Date prefix", date_prefix_chkbox))

        self._layout_hline_separator(layout)

        # MOVIE RECORDING

        mov_lbl = QtWidgets.QLabel("Record a movie")
        mov_lbl.setFont(title_font)
        layout.addLayout(center_me(mov_lbl))

        self.mov_resolution = QtWidgets.QComboBox(minimumWidth=120)
        self.mov_resolution.insertItems(
            0, [f"{w}x{h}" for w, h in self.cam.resolutions_video_mode]
        )
        self.mov_resolution.setToolTip(
            "Resolution of the movie in pixels (width x height)"
        )
        self.mov_resolution.currentIndexChanged.connect(self.mov_resolution_changed)
        layout.addLayout(label_element_layout("Resolution movie", self.mov_resolution))

        self.mov_framerate = QtWidgets.QDoubleSpinBox(decimals=3)
        layout.addLayout(label_element_layout("Framerate (fps)", self.mov_framerate))

        # set default resolution: must be after frame rate is initialized
        self.mov_resolution.setCurrentText(self.cam.resolution_str_video_mode)

        self.mov_rec_time = QtWidgets.QSpinBox(minimum=0, maximum=9999)
        self.mov_rec_time.setToolTip(
            "Recording length (s), set to zero for infinite length."
        )
        self.mov_rec_time_unit = QtWidgets.QComboBox()
        self.mov_rec_time_unit.insertItems(0, [n.name for n in ut.TimeUnits])
        layout.addLayout(
            label_element_layout(
                "Recording time", [self.mov_rec_time, self.mov_rec_time_unit]
            )
        )

        self.mov_record_button = QtWidgets.QPushButton("Start recording movie")
        self.mov_record_button.clicked.connect(self.record_movie)
        self._set_button_state(self.mov_record_button, is_on=False)
        layout.addWidget(self.mov_record_button)

        self._layout_hline_separator(layout)

        # IMAGE CAPTURE AND TIMELAPSE
        img_lbl = QtWidgets.QLabel("Capture an image & timelapse")
        img_lbl.setFont(title_font)
        layout.addLayout(center_me(img_lbl))

        self.img_resolution = QtWidgets.QComboBox(minimumWidth=120)
        self.img_resolution.insertItems(
            0, [f"{w}x{h}" for w, h in self.cam.resolutions_image_mode]
        )
        self.img_resolution.setCurrentText(self.cam.resolution_str_image_mode)
        self.img_resolution.setToolTip(
            "Resolution of the image in pixels (width x height)"
        )
        layout.addLayout(label_element_layout("Resolution image", self.img_resolution))

        timelapse_checkbox = QtWidgets.QCheckBox()
        timelapse_checkbox.setChecked(
            self._timelapse
        )  # connect after time stuff is set!
        timelapse_checkbox.stateChanged.connect(lambda x: self.timelapse_changed(x))
        layout.addLayout(label_element_layout("Timelapse imaging", timelapse_checkbox))

        self.img_timelapse_time = QtWidgets.QSpinBox(minimum=1, maximum=9999)
        self.img_timelapse_time.setEnabled(self._timelapse)
        self.img_timelapse_time.setToolTip("Time step between images to be taken.")
        self.img_timelapse_time_unit = QtWidgets.QComboBox()
        self.img_timelapse_time_unit.setEnabled(self._timelapse)
        self.img_timelapse_time_unit.insertItems(0, [n.name for n in ut.TimeUnits])
        layout.addLayout(
            label_element_layout(
                "Time between images",
                [self.img_timelapse_time, self.img_timelapse_time_unit],
            )
        )

        self.img_timelapse_duration = QtWidgets.QSpinBox(minimum=0, maximum=9999)
        self.img_timelapse_duration.setEnabled(self._timelapse)
        self.img_timelapse_duration.setToolTip(
            "Total duration of time lapse. Set to zero for infinite duration."
        )
        self.img_timelapse_duration_unit = QtWidgets.QComboBox()
        self.img_timelapse_duration_unit.setEnabled(self._timelapse)
        self.img_timelapse_duration_unit.insertItems(0, [n.name for n in ut.TimeUnits])
        layout.addLayout(
            label_element_layout(
                "Total duration",
                [self.img_timelapse_duration, self.img_timelapse_duration_unit],
            )
        )

        self.img_record_button = QtWidgets.QPushButton("Capture image")
        self.img_record_button.clicked.connect(self.capture_image)
        self._set_button_state(self.img_record_button, is_on=False)
        self.timelapse_changed(self._timelapse)  # to set tooltip and shortcut
        layout.addWidget(self.img_record_button)

    def capture_image(self):
        """Handle image capture single and timelapse."""
        # todo: dump to numpy array and then from numpy save as tiff.
        if self._timelapse:
            if not self._timelapse_is_recording:
                self._timelapse_is_recording = True

                self.img_record_button.setText("Stop timelapse")
                self.img_record_button.setToolTip("Stop timelapse.")

                self.mov_record_button.setEnabled(False)
                self._set_button_state(self.img_record_button, True)

                interval_s = (
                    self.img_timelapse_time.value()
                    * ut.TimeUnits[self.img_timelapse_time_unit.currentText()]
                )
                duration_s = (
                    self.img_timelapse_duration.value()
                    * ut.TimeUnits[self.img_timelapse_duration_unit.currentText()]
                )

                if duration_s == 0:
                    self._timelapse_counter = -1
                else:
                    self._timelapse_counter = duration_s // interval_s + 1

                self._capture_timelapse_image()

                self._timelapse_timer.start(interval_s * 1000)
            else:
                self._timelapse_is_recording = False

                self.img_record_button.setText("Start timelapse")
                self.img_record_button.setToolTip("Start timelapse.")

                self.mov_record_button.setEnabled(True)
                self._set_button_state(self.img_record_button, False)

                self._timelapse_timer.stop()
        else:
            self._capture_single_image()

    def _capture_single_image(self):
        """Capture a single image."""
        filename = ut.filename_increment(
            self.config.get("user_path"),
            self.file_name_input.text(),
            "tiff",
            date_prefix=self._date_prefix,
        )
        self.cam.my_capture_image(filename)

    def _capture_timelapse_image(self):
        """Capture a timelapse image."""
        if self._timelapse_counter > 0:
            self._timelapse_counter -= 1  # we have a limited number of images

        self._capture_single_image()

        if self._timelapse_counter == 0:  # stop right after taking last image
            self.capture_image()

    def mov_resolution_changed(self):
        """Set framerate when movie resolution was changed."""
        print("mov resolution changed")
        res_w, res_h = self.mov_resolution.currentText().split("x")
        self.cam.resolution_video_mode = int(res_w), int(res_h)
        frame_rate_limits = self.cam.limits_frame_rate
        self.mov_framerate.setMinimum(frame_rate_limits[0])
        self.mov_framerate.setMaximum(frame_rate_limits[1])
        self.mov_framerate.setToolTip(
            f"Frame rate limits: {frame_rate_limits[0]} to {frame_rate_limits[1]}"
        )

    def record_movie(self):
        """Start/stop recording a movie, depending on current state."""
        if not self._movie_is_recording:
            self._movie_is_recording = True

            self.mov_record_button.setText("Stop recording movie")
            self.mov_record_button.setToolTip("Stop recording movie.")
            self._set_button_state(self.mov_record_button, True)

            self.img_record_button.setEnabled(False)

            recording_time = (
                self.mov_rec_time.value()
                * ut.TimeUnits[self.mov_rec_time_unit.currentText()]
            )

            if recording_time > 0:
                self._movie_timer.start(recording_time * 1000)

            print("start recording movie")
        else:
            self._movie_is_recording = False

            self.mov_record_button.setText("Start recording movie")
            self.mov_record_button.setToolTip("Start recording movie.")

            self._set_button_state(self.mov_record_button, False)
            self.img_record_button.setEnabled(True)

            self._movie_timer.stop()
            print("stop recording movie")

    def set_user_path(self):
        """Set user path to a chosen value.

        Bring up a QFileDialog to choose a path, then set it to the user path as a
        Path object.
        """
        new_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select directory", self.config.get("user_path")
        )
        if new_path:
            self.config.set("user_path", str(Path(new_path)))
            self.config.save()
            self.path_label.setText(self.config.get("user_path"))

    def settings_dialog(self):
        """Display a settings dialog."""
        config_dialog = pyqtconfig.ConfigDialog(self.config, self, cols=1)
        config_dialog.setWindowTitle("Settings")
        config_dialog.accepted.connect(
            lambda: self.settings_update(config_dialog.config)
        )
        config_dialog.exec()

    def settings_load(self):
        """Load settings and setup the ConfigManager using pyqtconfig."""
        default_settings = {
            "Flip horizontally": False,
            "Flip vertically": False,
            "user_path": str(Path.home().joinpath("Desktop")),
        }

        default_settings_metadata = {
            "user_path": {"prefer_hidden": True},
        }

        self.config = pyqtconfig.ConfigManager(
            default_settings, filename=Path.home().joinpath(".config/rpyscope.json")
        )
        self.config.set_many_metadata(default_settings_metadata)

    def settings_update(self, new_settings):
        """Update settings from the settings dialog."""
        new_dict = new_settings.as_dict()

        # if transforms have changed, tell user to restart software
        # if new_dict["Flip horizontally"] != self.config.get(
        #         "Flip horizontally"
        # ) or new_dict["Flip vertically"] != self.config.get("Flip vertically"):
        #     QtWidgets.QMessageBox.warning(
        #         self,
        #         "Restart required",
        #         "You have changed the flip settings. "
        #         "Please restart the software for the changes to take effect.",
        #         QtWidgets.QMessageBox.Ok,
        #     )

        self.cam.update_preview_configuration(
            hflip=new_dict["Flip horizontally"], vflip=new_dict["Flip vertically"]
        )
        self.cam.switch_to_preview()

        self.config.set_many(new_dict)
        self.config.save()

    def timelapse_changed(self, state):
        """Act on change in timelapse settings."""
        widgets_active = [
            self.img_timelapse_time,
            self.img_timelapse_time_unit,
            self.img_timelapse_duration,
            self.img_timelapse_duration_unit,
        ]
        [k.setEnabled(state != 0) for k in widgets_active]
        if state == 0:
            self.img_record_button.setText("Capture image")
            self.img_record_button.setToolTip(
                "Capture image. Keyboard shortcut: Spacebar"
            )
            self.img_record_button.setShortcut(QtGui.QKeySequence("space"))
            self._timelapse = False
        else:
            self.img_record_button.setText("Start timelapse")
            self.img_record_button.setToolTip("Start timelapse.")
            self.img_record_button.setShortcut(QtGui.QKeySequence())
            self._timelapse = True

    @staticmethod
    def _set_button_state(button: QtWidgets.QPushButton, is_on=False):
        """Set button state is_on state.

        Red if it's on, green if it's off.

        :param button: Button to change color on.
        :param is_on: Bool if it's on (red) or off (green)
        """
        if is_on:
            # if darkdetect.isDark():
            #     color = "#690000"
            # else:
            color = "#FFB6B6"

        else:
            # if darkdetect.isDark():
            #     color = "#0d4f00"
            # else:
            color = "#DBFFD4"
        button.setStyleSheet(f"background-color:{color}")

    def _set_date_prefix(self, value):
        """Set date prefix based on the state of the toggle."""
        self._date_prefix = value != 0

    @staticmethod
    def _layout_hline_separator(layout: QtWidgets.QVBoxLayout) -> None:
        """Add stretches and a horizontal line to a vertical layout."""
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addStretch()
        layout.addWidget(line)
        layout.addStretch()
