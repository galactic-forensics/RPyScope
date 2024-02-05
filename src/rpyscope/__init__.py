# Initialize the RPyScope

import sys

from qtpy import QtWidgets

from rpyscope.microscope import Cam
from rpyscope.gui_qt import MainWindowControls


def demo():
    """Run the app with the demo camera."""
    app = QtWidgets.QApplication(sys.argv)
    rpyscope_app = MainWindowControls(Cam.Demo)
    rpyscope_app.show()

    sys.exit(app.exec_())


def rpihq_legacy():
    """Run the app with the legacy support for the RPi HQ."""
    app = QtWidgets.QApplication(sys.argv)
    rpyscope_app = MainWindowControls(Cam.RPi_HQ)
    rpyscope_app.show()

    sys.exit(app.exec_())
