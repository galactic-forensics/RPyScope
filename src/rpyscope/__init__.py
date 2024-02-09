# Initialize the RPyScope

import sys

from qtpy import QtWidgets

from rpyscope.microscope import Cam
from rpyscope.gui import MainWindowControls


def demo():
    """Run the app with the demo camera."""
    app = QtWidgets.QApplication(sys.argv)
    rpyscope_app = MainWindowControls(Cam.Demo)
    rpyscope_app.show()

    sys.exit(app.exec_())


def rpihq():
    """Run the app with support for the RPi HQ camera."""
    app = QtWidgets.QApplication(sys.argv)
    rpyscope_app = MainWindowControls(Cam.RPiCam)
    rpyscope_app.show()

    sys.exit(app.exec_())
