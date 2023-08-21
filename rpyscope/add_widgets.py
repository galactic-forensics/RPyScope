"""Additional widgets for PyQt5 that we need."""

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt


class LineEditHistory(QLineEdit):
    """Create a line edit tool that contains a _history, like the terminal."""

    def __init__(self):
        QLineEdit.__init__(self)

        # History
        self._history = []
        self._history_counter = 0

    def add_to_history(self, val):
        """Add an entry to the _history."""
        self._history.append(val)

    def browse_history(self, up=True):
        """Browse the _history.

        Sets the text box of the CLI in order to browse the _history of the commands.

        :param up: Up direction or not? Up direction moves to older entries.
        :type up: bool
        """
        cnt = self._history_counter
        if up:
            cnt += 1
        else:
            cnt -= 1

        # check if outside of _history
        if cnt > len(self._history):
            return
        elif cnt <= 0:
            self.clear()
            self._history_counter = 0
            return
        else:
            self.setText(self._history[-cnt])
            self._history_counter = cnt

    def keyPressEvent(self, a0):
        """Handle key press events -> go to _history for arrow up and down."""
        super().keyPressEvent(a0)

        if a0.key() == Qt.Key_Return or a0.key() == Qt.Key_Enter:
            self._history_counter = 0
        elif a0.key() == Qt.Key_Up:
            self.browse_history(up=True)  # browse back in _history
        elif a0.key() == Qt.Key_Down:
            self.browse_history(up=False)  # browse forward in _history
        elif a0.key() == Qt.Key_Escape:  # reset the _history
            self.clear()
            self._history_counter = 0
