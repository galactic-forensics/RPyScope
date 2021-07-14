"""Test the microscope class."""

from pathlib import Path

from rpyscope.microscope import Cam, Microscope


def test_microscope_default_camera():
    """Ensure that the default camera is set to RPi."""
    mic = Microscope()
    assert mic.select_camera == Cam.RPi_HQ


def test_microscope_home_folder():
    """Make sure that the home folder is set to '/home/pi'."""
    mic = Microscope()
    assert mic.microscope_settings["home_folder"] == Path.home()
