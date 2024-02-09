# My own subclass for PiCam2

try:
    from picamera2 import Picamera2
except ImportError:  # local dev, not on RPi
    from rpyscope.dev import SimCamera as Picamera2

class Camera(Picamera2):
    """PiCam2 class for camera interaction.
    
    This is the class that actually interacts with the picamera2 library and runs
    the preview, etc.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the camera."""
        super().__init__(*args, **kwargs)
        
        # configure standard preview configuration
        _preview_configuration = self.create_preview_configuration()
        self.configure(_preview_configuration)
        

    
class PiCamHQ:
    """This is a property class to give us the available settings for a PiCamHQ."""
    
    def __init__(self):
        """Initialize the property class."""
        # these tuples are the configurations. They must have equal length
        self._mode = (1, 2, 3, 4)  # integers
        self._resolution = (
            (2028, 1080), (2028, 1520), (4056, 3040), (1012, 760)
        )  # resolution: width, height
        self._aspect_ratio = ("169:90", "4:3", "4:3", "4:3")  # info only
        self._video_mode = (True, True, True, True)  # available in video
        self._image_mode = (False, False, True, True)  # available in image mode
        self._fov = ("partial", "full", "full", "full")  # info only
        self._binning_scaling = (
            "2 x 2 binned", "2 x 2 binned", "None", "4 x 4 scaled"
        )  # info only
    
        
    @property
    def info(self):
        """Get an information table with the given settings."""
        # info_str = """Mode\tResolution\tAspect Ratio\tVideo\tImage\t"""
        return None
        
