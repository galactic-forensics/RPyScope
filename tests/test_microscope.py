"""Test the microscope class."""

from src import Microscope


def test_home_folder():
    mic = Microscope()
    assert mic.microscope_settings["home_folder"] == "/home/pi"
