"""Python class that defines microscope operations."""

from datetime import datetime
import os

from picamera import PiCamera


class Microscope:
    """Microscope class

    This class defines the default microscope functions that are used for file
    interactions, and are super functions for taking photos and videos. Capture image
    and capture video classes inherit from Microscope class.
    """

    def __init__(self):
        """Initialize the Microscope class."""
        self.cam = PiCamera()

        self.is_preview_on = False

        self.microscope_settings = {
            "auto_exposure": True,
            "home_folder": "/home/pi",
            "image_format": "jpeg",
            "video_format": "h264",
        }

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
            self.cam.exposure_mode = "auto"
            self.cam.awb_mode = "auto"
        else:
            self.microscope_settings["auto_exposure"] = False
            self.cam.shutter_speed = self.cam.exposure_speed
            self.cam.exposure_mode = "off"
            g = self.cam.awb_gains
            self.cam.awb_mode = "off"
            self.cam.awb_gains = g

    @property
    def home_folder(self):
        """Get / set the home folder.

        :param newval: New home folder, absolute path.
        :type newval: str

        :return: Name of the set home folder
        :rtype: str

        :raises TypeError: The passed value is not a string.
        :raises ValueError: The given path is not valid.
        """
        return self.microscope_settings["home_folder"]

    @home_folder.setter
    def home_folder(self, newval):
        if not isinstance(newval, str):
            raise TypeError(
                f"The value for the path must be a string but is a {type(newval)}."
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
