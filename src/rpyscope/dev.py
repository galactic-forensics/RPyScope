# Development tools

import copy
from enum import Enum

from qtpy import QtCore, QtWidgets


class SimCamera:
    """Simulation camera to use when picamera2 is not installed."""

    def __init__(self):
        self._config = {"main": {}, "controls": {}}

    def configure(self, *args, **kwargs):
        print(f"camera configured with {args=} and {kwargs=}")
        pass

    def create_preview_configuration(self):
        return copy.deepcopy(self._config)

    def create_still_configuration(self):
        return copy.deepcopy(self._config.copy())

    def create_video_configuration(self):
        return copy.deepcopy(self._config.copy())

    def start(self):
        print("camera start called.")

    def start_recording(self, *args, **kwargs):
        print(f"start_recrding called with {args=} and {kwargs=}")

    def stop(self):
        print("camera stop called.")

    def stop_recording(self):
        print("stop_recording called")

    def switch_mode_and_capture_image(self, *args, **kwargs):
        print(f"switch mode and capture image called with {args=} and {kwargs=}")

    def wait(self, *args, **kwargs):
        print("cam.wait called")


class Transform:
    """Transformation class to use when picamera2 is not installed."""

    def __init__(self, *args, **kwargs):
        print(f"Transform called with {args=} and {kwargs=}")
        pass


class Quality(Enum):
    """Fake quality class."""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


class H264Encoder:
    """Fake H264Encoder"""

    def __init__(self):
        pass
    
class QGlPicamera2(QtWidgets.QWidget):
    """Fake QGLPicamera2 class."""
    
    done_signal = QtCore.Signal()
    signal_done = QtCore.Signal()
    def __init__(self, *args, **kwargs):
        super().__init__()
