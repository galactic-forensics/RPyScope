"""Class for the RPi camera."""

from rpyscope.cameras.abstract_camera import AbsCamera

try:
    from picamera import PiCamera
except ModuleNotFoundError:
    print("No picamera Module. Please choose Demo camera.")

    class PiCamera:
        """Dummy class so we can init the RPiCam."""

        pass


class RPiCam(PiCamera):
    __metaclass__ = AbsCamera
    """Re-implementation of the PiCamera instance of picamera.

    This is done such that we are easily capable of implementing the same routines
    for various cameras. Most of the software will be built on PiCamera commands,
    so here we really only add where absolutely necessary.
    """

    def __init__(self):
        """Initialize RPiCam."""
        super().__init__()

    def auto_exposure(self, value):
        """Turn auto exposure on or off.

        :param value: True for on, False for off.
        :type value: bool
        """
        if value:
            self.exposure_mode = "auto"
            self.awb_mode = "auto"
        else:
            self.shutter_speed = self.exposure_speed
            self.exposure_mode = "off"
            g = self.awb_gains
            self.awb_mode = "off"
            self.awb_gains = g
