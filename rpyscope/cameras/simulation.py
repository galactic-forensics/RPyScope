"""Class for Simulated Camera."""

from .abstract_camera import AbsCamera


class SimCam(AbsCamera):
    """Simulated Camera. Simply pipes commands through and returns them as strings."""

    def __init__(self):
        """Initialize."""
        pass

    # PROPERTIES #

    @property
    def brightness(self):
        """Get / set brightness of camera.

        :return: Brightness setting
        :rtype: float
        """
        print_return_call("brightness")
        return None

    @brightness.setter
    def brightness(self, value):
        print_return_call("brigntess", value)

    @property
    def contrast(self):
        """Get / set contrast of camera.

        :return: Contrast setting
        :rtype: float
        """
        print_return_call("contrast")
        return None

    @contrast.setter
    def contrast(self, value):
        print_return_call("contrast", value)

    # METHODS #

    def auto_exposure(self, value):
        """Turn auto exposure on or off.

        :param value: True for on, False for off.
        :type value: bool
        """
        print_return_call("auto_exposure", value)

    def capture(self, fname, format):
        """Capture an image.

        :param fname: Filename
        :type fname: str
        :param format: Format
        :type format: str
        """
        print_return_call("capture", fname, format)

    def close(self):
        """Close the camera connection."""
        print_return_call("close")

    def start_preview(self):
        """Start camera preview."""
        print_return_call("start_preview")

    def start_recording(self, fname, format):
        """Record a video.

        :param fname: Filename
        :type fname: str
        :param format: Format
        :type format: str
        """
        print_return_call("start_recording", fname, format)

    def stop_preview(self):
        """Stop camera preview."""
        print_return_call("stop_preview")

    def stop_recording(self):
        """Stop video recording."""
        print_return_call("stop_recording")


def print_return_call(fnc_name, *args, **kwargs):
    """Print and return the name and arguments.

    :param fnc_name: Function name.
    :type fnc_name: str

    :return: Name and arguments
    :rtype: Tuple(str, *args, **kwargs)
    """
    print(f"Fnc: {fnc_name}\nargs: {args}\nkwargs: {kwargs}")
    return fnc_name, args, kwargs
