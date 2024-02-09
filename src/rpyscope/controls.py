# Main Control GUI

from qtpy import QtCore, QtGui, QtWidgets

from rpyscope.camera import Camera
from rpyscope.preview import PreviewWindow

class MicroscopeControls(QtWidgets.QMainWindow):
    """Main window for controls of the microscope."""

    def __init__(self) -> None:
        """Initialize the control GUI."""
        super().__init__(parent=None)

        left = 0
        top = 0
        width = 300
        height = 700
        self.setWindowTitle("Control")

        # setup camera and start preview
        self.cam = Camera()
        
        self.preview = PreviewWindow(self.cam, parent=self)
        self.cam.start()
        
        self.init_ui()
        
        self.show()
        self.setGeometry(QtCore.QRect(left, top, width, height))

    def init_ui(self):
        """Initialize the user interface."""
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(layout)
        
        # set quit shortcut to Ctrl+Q
        quit_sc = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
        quit_sc.activated.connect(self.close)
        
        # Settings
        settings_button = QtWidgets.QPushButton("Settings [S]")
        settings_button.clicked.connect(self.open_settings)
        settings_button.setToolTip("Change program settings")
        settings_button.setShortcut("S")
        layout.addWidget(settings_button)
        
        # Brightness
        layout.addWidget(QtWidgets.QLabel("Brightness [B]"))
        bright_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        bright_slider.setMinimum(0)
        bright_slider.setMaximum(100)
        # bright_slider.valueChanged.connect(self.brightness_changed)  # fixme
        bright_sc = QtWidgets.QShortcut(QtGui.QKeySequence("B"), self)
        bright_sc.activated.connect(bright_slider.setFocus)
        bright_reset_button = QtWidgets.QPushButton("default")
        # bright_reset_button.clicked.connect(self.reset_bright)  # fixme
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(bright_slider)
        h_layout.addWidget(bright_reset_button)
        layout.addLayout(h_layout)
        # self.config.add_handler("brightness", self.bright_slider)  # fixme
        
        # Contrast
        layout.addWidget(QtWidgets.QLabel("Contrast [C]"))
        contr_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        contr_slider.setMinimum(-100)
        contr_slider.setMaximum(100)
        # contr_slider.valueChanged.connect(self.contrast_changed)  # fixme
        contr_reset_button = QtWidgets.QPushButton("default")
        # contr_reset_button.clicked.connect(self.reset_contr)  # fixme
        contr_sc = QtWidgets.QShortcut(QtGui.QKeySequence("C"), self)
        contr_sc.activated.connect(contr_slider.setFocus)
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(contr_slider)
        h_layout.addWidget(contr_reset_button)
        layout.addLayout(h_layout)
        # config.add_handler("contrast", self.contr_slider)  # fixme
    
    def open_settings(self):
        """Open the settings dialog."""
        pass
