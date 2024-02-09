# Preview for picamera2

from qtpy import QtWidgets

try:
    from picamera2.previews.qt import QGlPicamera2
    from picamera2 import Picamera2
except ImportError:  # local development, not on RPi
    from rpyscope.dev import SimCamera as Picamera2


class PreviewWindow(QtWidgets.QMainWindow):
    """Preview window, subclassed from existing QGlPicamera2."""

    def __init__(self, picam2: Picamera2, parent=None, **kwargs):
        """Initialize the class.
        
        :param picam2: Camera instance to display.
        :param parent: Parent Widget.
        :param kwargs: Keyword arguments:
            top: Top position of window, default 0
            left: left position of window, default 350
            height: Height of window, default 600
            width: Width of window, default 800
            transform: Transfomration for preview, default None
        """
        super().__init__(parent=parent)
        
        self.setWindowTitle("Live preview")
        
        top = kwargs.get("top", 0)
        left = kwargs.get("left", 350)
        height = kwargs.get("height", 600)
        width = kwargs.get("width", 800)
        
        if Picamera2.__name__ != "SimCamera":
            preview_widget = QGlPicamera2(picam2, transform=kwargs.get("transform", None))
            self.setCentralWidget(preview_widget)
        
        self.show()
        self.setGeometry(left, top, width, height)
        