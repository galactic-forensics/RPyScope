# Run the App
import sys

from qtpy import QtWidgets

from rpyscope.controls import MicroscopeControls


def run():
    """Run the rpyscope app."""
    app = QtWidgets.QApplication(sys.argv)
    _ = MicroscopeControls()
    sys.exit(app.exec_())
