# Initialize the RPyScope

import sys

from qtpy import QtWidgets

from rpyscope.microscope import Cam
from rpyscope.gui_qt import MainWindowControls


def demo():
    app = QtWidgets.QApplication(sys.argv)
    rpyscope_app = MainWindowControls(Cam.Demo)
    rpyscope_app.show()

    sys.exit(app.exec_())
