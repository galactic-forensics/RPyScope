# Utility functions and enums

from datetime import datetime
from enum import IntEnum
from pathlib import Path
from typing import Union

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


class SettingsQComboBox(QtWidgets.QComboBox):
    """Create a narrow QComboBox for image rotation settings in Settings."""

    def __init__(self, *args, **kwargs):
        """Initialize and set maximum width."""
        super().__init__(*args, **kwargs)
        self.setMaximumWidth(100)


def filename_increment(
    pth: Union[Path, str], fname: str, ext: str, date_prefix=True
) -> Path:
    """Create a filename, increment it with three digits, and return the full path.

    The returned filename will be a complete path, where the filename is going to be
    "fname-XXX.ext". Here, XXX is a three-digit, auto-incrementing number.

    :param pth: Path where file should live.
    :param fname: File name, as a string.
    :param ext: File extension.
    :param date_prefix: If True, add a date prefix to the filename.
    """
    if isinstance(pth, str):
        pth = Path(pth)

    if date_prefix:
        fname = f"{datetime.now().strftime('%Y-%m-%d')}-{fname}"
    it = 0
    while True:
        new_fname = pth.joinpath(f"{fname}-{it:03d}.{ext}")
        if not new_fname.exists():
            return new_fname
        it += 1
