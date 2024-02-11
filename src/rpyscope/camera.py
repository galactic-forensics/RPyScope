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
        self._name = "Raspberry Pi High Quality Camera"
        # these tuples are the configurations. They must have equal length
        self._modes = (1, 2, 3, 4)  # integers
        self._resolutions = (
            (2028, 1080),
            (2028, 1520),
            (4056, 3040),
            (1012, 760),
        )  # resolution: width, height
        self._aspect_ratios = ("169:90", "4:3", "4:3", "4:3")  # info only
        self._video_modes = (True, True, True, True)  # available in video
        self._limits_frame_rates = (
            (0.1, 50),
            (0.1, 50),
            (0.005, 10),
            (50.1, 120),
        )  # min, max
        self._image_modes = (False, False, True, True)  # available in image mode
        self._fovs = ("partial", "full", "full", "full")  # info only
        self._binning_scalings = (
            "2 x 2 binned",
            "2 x 2 binned",
            "None",
            "4 x 4 scaled",
        )  # info only

        # set parameters
        self._mode = None
        self._resolution_video_mode = None
        self._limits_frame_rate = None

        # set default resolution
        self.resolution_video_mode = self._resolutions[2]
        self.resolution_image_mode = self._resolutions[2]

        self._video_format = "h264"

    @property
    def info(self) -> tuple[tuple, tuple]:
        """Get information about the camera.
        
        This information can be displayed as a table. The first tuple returned 
        should be the header(s) of the table. The second returned tuples should be 
        the data per column.
        
        :return: Two tuples:
            - First tuple: Headers
            - Second tuple: Tuple of tuples... data
        """
        hdr = (
            "Mode", "Resolution (px)", "Aspect Ratio",
            "Video", "Frame rate (fps)", "Image", "Field of View", "Binning & Scaling"
        )

        table = (
            [str(it) for it in self._modes],
            [f"{w}x{h}" for w, h in self._resolutions],
            self._aspect_ratios,
            ["x" if it else "" for it in self._video_modes],
            [f"{it} - {jt}" for it, jt in self._limits_frame_rates],
            ["x" if it else "" for it in self._image_modes],
            self._fovs,
            self._binning_scalings
        )

        return hdr, table

    @property
    def limits_frame_rate(self) -> tuple:
        """Get the limits of the frame rate.

        :return: min, max at given setting.
        """
        return self._limits_frame_rate

    @property
    def mode(self) -> int:
        """Get/set the mode the camera is in - sets video mode!"""
        return self._mode

    @mode.setter
    def mode(self, value: int):
        idx = self._modes.index(value)
        self._mode = value
        self._resolution_video_mode = self._resolutions[idx]
        self._limits_frame_rate = self._limits_frame_rates[idx]
        
    @property
    def name(self):
        """Get the name of the camera."""
        return self._name

    @property
    def resolution_image_mode(self) -> tuple:
        """Set / get one of the resolutions for image mode.

        This is the standard setter, using a tuple.

        :return: Width, height in pixels
        """
        return self._resolution_image_mode

    @resolution_image_mode.setter
    def resolution_image_mode(self, value: tuple):
        idx = self._resolutions.index(value)
        self._resolution_image_mode = value
        self._mode = self._modes[idx]

    @property
    def resolution_str_image_mode(self) -> str:
        """Set / get one of the resolutions as a string for image mode.

        Uses the resolution property, but works with strings: "{width}x{height}".

        :return: String of resolution: "{width}x{height}"
        """
        w, h = self.resolution_image_mode
        return f"{w}x{h}"

    @resolution_str_image_mode.setter
    def resolution_str_image_mode(self, value):
        w, h = value.split("x")
        self.resolution_image_mode = int(w), int(h)

    @property
    def resolution_video_mode(self) -> tuple:
        """Set / get one of the resolutions for video mode.

        This is the standard setter, using a tuple.

        :return: Width, height in pixels
        """
        return self._resolution_video_mode

    @resolution_video_mode.setter
    def resolution_video_mode(self, value: tuple):
        idx = self._resolutions.index(value)
        self._resolution_video_mode = value
        self._mode = self._modes[idx]
        self._limits_frame_rate = self._limits_frame_rates[idx]

    @property
    def resolution_str_video_mode(self) -> str:
        """Set / get one of the resolutions as a string for video mode.

        Uses the resolution property, but works with strings: "{width}x{height}".

        :return: String of resolution: "{width}x{height}"
        """
        w, h = self.resolution_video_mode
        return f"{w}x{h}"

    @resolution_str_video_mode.setter
    def resolution_str_video_mode(self, value):
        w, h = value.split("x")
        self.resolution_video_mode = int(w), int(h)

    @property
    def resolutions_video_mode(self) -> tuple:
        """Get all resolutions as tuples."""
        return self._resolutions

    @property
    def resolutions_image_mode(self):
        """Get all resolutions that are possible in image mode."""
        return [k for it, k in enumerate(self._resolutions) if self._image_modes[it]]

    @property
    def video_format(self) -> str:
        """Get the video format qualifier as a string."""
        return self._video_format
