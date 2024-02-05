"""Python class that defines microscope operations."""

from enum import Enum
import os
from pathlib import Path

from rpyscope.cameras import rpi_cam
from rpyscope.cameras import simulation


class Cam(Enum):
    """Enum Class for Available / Implemented Cameras."""

    RPi_HQ = rpi_cam.RPiCam()
    Demo = simulation.SimCam()


class Microscope:
    """Microscope class

    This class defines the default microscope functions that are used for file
    interactions, and are super functions for taking photos and videos. Capture image
    and capture video classes inherit from Microscope class.
    """

    def __init__(self, default_cam=Cam.RPi_HQ):
        """Initialize the Microscope class."""
        self.cam = None
        self.default_cam = default_cam

        self.is_preview_on = False

        self.microscope_settings = {
            "auto_exposure": True,
            "home_folder": Path.home(),
            "image_format": "jpeg",
            "video_format": "h264",
        }

        # todo load settings

        # todo load startup script
        self.path_config = None
        self._setup_config_folder()

        self._load_camera()

    # PROPERTIES #

    @property
    def auto_exposure(self):
        """Set / get auto exposure.

        Follows PiCamera manual, section 3.5 and also turns auto white balance off.

        :param newval: Set it to on or off?
        :type newval: bool

        :return: Auto exposure status
        :rtype: bool

        :raises TypeError: Invalid type specified, need to specify bool.
        """
        return self.microscope_settings["auto_exposure"]

    @auto_exposure.setter
    def auto_exposure(self, newval):
        if not isinstance(newval, bool):
            raise TypeError(
                f"The value for auto exposure must be a bool but is a {type(newval)}."
            )
        if newval:
            self.microscope_settings["auto_exposure"] = newval
            self.cam.auto_exposure(True)
        else:
            self.microscope_settings["auto_exposure"] = False
            self.cam.auto_exposure(False)

    @property
    def select_camera(self):
        """Get / Set the camera.

        :return: Camera that was selected.
        :rtype: Microscope.Cam

        :raises TypeError: Invalid type was selected to set camera with.
        """
        return self.default_cam

    @select_camera.setter
    def select_camera(self, value):
        if not isinstance(value, type(self.Cam)):
            raise TypeError(
                "Camera to select must be an instance of Microscope.Cam " "enum."
            )
        self.default_cam = value
        self._load_camera()

    @property
    def home_folder(self):
        """Get / set the home folder.

        :param newval: New home folder, absolute path.
        :type newval: Path

        :return: Name of the set home folder
        :rtype: Path

        :raises TypeError: The passed value is not a pathlib path.
        :raises ValueError: The given path is not valid.
        """
        return self.microscope_settings["home_folder"]

    @home_folder.setter
    def home_folder(self, newval):
        if not isinstance(newval, Path):
            raise TypeError(
                f"The value for the path must be a Path but is a {type(newval)}."
            )
        if not os.path.exists(newval):
            raise ValueError(
                f"The selected path {newval} does not exists. Please create it first."
            )
        self.microscope_settings["home_folder"] = newval

    @property
    def image_format(self):
        """Get / set image format.

        ToDo: Enum class like in IK to have all image formats available.

        :param newval: New image format, valid format required.
        :type newval: str

        :return: Image format
        :rtype: str

        :raises TypeError: The passed value is not a string.
        """
        return self.microscope_settings["image_format"]

    @image_format.setter
    def image_format(self, newval):
        if not isinstance(newval, str):
            raise TypeError(
                f"The value for the image format must be a string but is a "
                f"{type(newval)}."
            )
        self.microscope_settings["image_format"] = newval

    @property
    def video_format(self):
        """Get / set video format.

        ToDo: Enum class like in IK to have all video formats available.

        :param newval: New video format, valid format required.
        :type newval: str

        :return: video format
        :rtype: str

        :raises TypeError: The passed value is not a string.
        """
        return self.microscope_settings["video_format"]

    @video_format.setter
    def video_format(self, newval):
        if not isinstance(newval, str):
            raise TypeError(
                f"The value for the video format must be a string but is a "
                f"{type(newval)}."
            )
        self.microscope_settings["video_format"] = newval

    # PRIVATE FUNCTIONS #

    def _load_camera(self):
        """Load a new camera, to be called when a default is set.

        If a camera is open, close it first.
        """
        if self.cam is not None:
            self.cam.close()
        self.cam = self.default_cam.value

    def _setup_config_folder(self):
        """Sets up a configuration folder and sets the according self.path_config.

        This folder is used for the `init.py` file that will initialize user settings
        and will be used to store settings later on. It is assumed that we are on
        a Posix system.
        """
        config_folder = Path.joinpath(Path.home(), ".config/RPyConf")
        if not Path.is_dir(config_folder):
            Path.mkdir(config_folder)
        self.path_config = config_folder
