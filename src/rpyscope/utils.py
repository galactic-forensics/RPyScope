# Utility functions and enums

from enum import IntEnum

from qtpy import QtGui, QtWidgets

from rpyscope.camera import PiCamHQ


class TimeUnits(IntEnum):
    """Time units enum, values are seconds in unit."""

    sec = 1
    min = 60


class CameraInfo(QtWidgets.QDialog):
    """Simple QDialog that displays the camera info in a digestable manner."""

    def __init__(self, camera: PiCamHQ, parent=None):
        """Initialize the dialog."""
        super().__init__(parent=parent)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        font_bold = QtGui.QFont()
        font_bold.setBold(True)

        # title
        tit_lbl = QtWidgets.QLabel(f"Camera: {camera.name}")
        tit_lbl.setFont(font_bold)
        layout.addWidget(tit_lbl)

        # now make the table
        tbl_layout = QtWidgets.QGridLayout()

        hdrs, table_content = camera.info

        for col, hdr in enumerate(hdrs):
            tbl_layout.addWidget(QtWidgets.QLabel(hdr), 0, col)
            for row, content in enumerate(table_content[col]):
                tbl_layout.addWidget(QtWidgets.QLabel(content), row + 1, col)

        layout.addLayout(tbl_layout)

        ok_button = QtWidgets.QDialogButtonBox.StandardButton.Ok
        button_box = QtWidgets.QDialogButtonBox(ok_button)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.show()
