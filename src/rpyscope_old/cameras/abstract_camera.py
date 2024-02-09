"""Abstract class for camera."""

import abc


class AbsCamera(metaclass=abc.ABCMeta):
    """Abstract camera class that has functions implemented.

    All cameras should inherit from this class.
    """

    # PROPERTIES #

    @property
    @abc.abstractmethod
    def brightness(self):
        """Get / set brightness of camera.

        :return: Brightness setting
        :rtype: float
        """

    @brightness.setter
    @abc.abstractmethod
    def brightness(self, value):
        pass

    @property
    @abc.abstractmethod
    def contrast(self):
        """Get / set contrast of camera.

        :return: Contrast setting
        :rtype: float
        """

    @contrast.setter
    @abc.abstractmethod
    def contrast(self, value):
        pass

    @property
    @abc.abstractmethod
    def framerate(self):
        """Get / set framerate of camera.

        # todo docstring
        """

    @framerate.setter
    @abc.abstractmethod
    def framerate(self, value):
        pass

    @property
    @abc.abstractmethod
    def resolution(self):
        """Get / set resolution of camera.

        :return: Resolution.
        :rtype: str
        """

    @resolution.setter
    @abc.abstractmethod
    def resolution(self, value):
        pass

    # METHODS #

    @abc.abstractmethod
    def auto_exposure(self, value):
        """Turn auto exposure on or off.

        :param value: True for on, False for off.
        :type value: bool
        """
        pass

    @abc.abstractmethod
    def capture(self, fname, format):
        """Capture an image.

        :param fname: Filename
        :type fname: str
        :param format: Format
        :type format: str
        """
        pass

    @abc.abstractmethod
    def close(self):
        """Close the camera connection."""
        pass

    @abc.abstractmethod
    def start_preview(self):
        """Start camera preview."""
        pass

    @abc.abstractmethod
    def start_recording(self, fname, format):
        """Record a video.

        :param fname: Filename
        :type fname: str
        :param format: Format
        :type format: str
        """

    @abc.abstractmethod
    def stop_preview(self):
        """Stop camera preview."""
        pass

    @abc.abstractmethod
    def stop_recording(self):
        """Stop video recording."""
        pass
