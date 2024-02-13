# My own subclass for PiCam2

from pathlib import Path

try:
    from picamera2 import Picamera2
    from picamera2.encoders import H264Encoder, Quality
    from libcamera import Transform
except ImportError:  # local dev, not on RPi
    from rpyscope.dev import SimCamera as Picamera2
    from rpyscope.dev import H264Encoder, Quality, Transform


class PiCamHQ:
    """This is a property class to give us the available settings for a PiCamHQ."""

    def __init__(self, control, **kwargs):
        """Pi Camera HQ class to run the camera and do all the neat things necessary.

        `self.cam` contains the actual `picamera2` camera object.

        :param control: The microscope control object.
        :param kwargs: Keyword arguments:
            - hflip: Horizontal flip, default False
            - vflip: Vertical flip, default False
        """
        # Camera setup
        self.cam = Picamera2()
        self.control = control

        self._video_encoder = H264Encoder()
        self._video_quality = Quality.VERY_HIGH
        self._video_format = "h264"

        # temporary variables:
        self._filename = None
        self._is_recording = False

        # define transformation
        self._hflip = kwargs.get("hflip", False)
        self._vflip = kwargs.get("vflip", False)

        # configure standard preview configuration
        self._preview_configuration = self.cam.create_preview_configuration()
        self._preview_configuration["transform"] = self.transform
        self.cam.configure(self._preview_configuration)

        self._capture_configuration = self.cam.create_still_configuration()
        self._capture_configuration["transform"] = self.transform

        self._video_configuration = self.cam.create_video_configuration()
        self._video_configuration["transform"] = self.transform

        # Camera information
        self._name = "Raspberry Pi High Quality Camera"
        # these tuples are the configurations. They must have equal length
        self._resolutions = (
            (2028, 1080),
            (1332, 990),
            (4056, 3040),
            (2028, 1520),
            (1014, 760),
        )  # resolution: width, height
        self._aspect_ratios = ("169:90", "4:3", "4:3", "4:3", "4:3")  # info only
        self._video_modes = (True, True, False, False, False)  # available in video
        self._limits_frame_rates = (
            (0.1, 50),
            (0.1, 120),
            ("N/A", "N/A"),
            ("N/A", "N/A"),
            ("N/A", "N/A"),
        )  # min, max
        self._image_modes = (False, False, True, True, True)  # available in image mode
        self._fovs = ("partial", "zoomed", "full", "full", "full")  # info only

        # set parameters
        self._resolution_video_mode = None
        self._limits_frame_rate = None
        self._frame_rate = None

        # set default resolution
        self.resolution_video_mode = self._resolutions[0]
        self.resolution_image_mode = self._resolutions[2]

        # set default frame rate
        self.frame_rate = 30

    @property
    def frame_rate(self) -> float:
        """Get the current frame rate."""
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, value):
        self._frame_rate = value
        self.update_video_configuration(framerate=value)

    @property
    def hflip(self) -> bool:
        """Get horizontal flip mode.

        :return: True if horizontal flip is enabled.
        """
        return self._hflip

    @hflip.setter
    def hflip(self, value):
        self._hflip = value

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
            "Resolution (px)",
            "Aspect Ratio",
            "Video",
            "Frame rate (fps)",
            "Image",
            "Field of View",
        )

        table = (
            [f"{w}x{h}" for w, h in self._resolutions],
            self._aspect_ratios,
            ["x" if it else "" for it in self._video_modes],
            [f"{it} - {jt}" for it, jt in self._limits_frame_rates],
            ["x" if it else "" for it in self._image_modes],
            self._fovs,
        )

        return hdr, table

    @property
    def limits_frame_rate(self) -> tuple:
        """Get the limits of the frame rate.

        :return: min, max at given setting.
        """
        return self._limits_frame_rate

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
        self._resolution_image_mode = value
        self.update_capture_configuration(resolution=value)

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
        self._limits_frame_rate = self._limits_frame_rates[idx]
        self.update_video_configuration(resolution=value)

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
        return [k for it, k in enumerate(self._resolutions) if self._video_modes[it]]

    @property
    def resolutions_image_mode(self):
        """Get all resolutions that are possible in image mode."""
        return [k for it, k in enumerate(self._resolutions) if self._image_modes[it]]

    @property
    def transform(self) -> Transform:
        """Get the transformation settings object."""
        return Transform(hflip=self._hflip, vflip=self._vflip)

    @property
    def vflip(self) -> bool:
        """Get vertical flip mode.

        :return: True if vertical flip is enabled.
        """
        return self._vflip

    @vflip.setter
    def vflip(self, value):
        self._vflip = value

    @property
    def video_format(self) -> str:
        """Get the video format qualifier as a string."""
        return self._video_format

    def capture_done(self, job):
        """"""
        result = self.cam.wait(job)

        if self._filename is not None:
            result.save(self._filename)
            self._filename = None

    def capture_image(self, filename: Path):
        """Capture an image and save it to a file.

        The capture configuration that is set up will be used. Saves an image to a
        PIL array and then saves it as a tiff file.

        :param filename: Filename to save the image to.
        """
        self._filename = filename

        self.cam.switch_mode_and_capture_image(
            self._capture_configuration,
            "main",
            signal_function=self.control.preview.qpicamera2.signal_done,
        )

    def capture_video_start(self, filename: Path):
        """Capture a video and save it to a file.

        The capture configuration that is set up will be used.

        :param filename: Filename to save the video to.
        """
        self.cam.stop()
        self.cam.configure(self._video_configuration)
        self.cam.start_recording(
            self._video_encoder, str(filename.absolute()), quality=self._video_quality
        )

    def capture_video_stop(self):
        """Stop the video recording."""
        self.cam.stop_recording()
        self.restart_preview()

    def restart_preview(self):
        """Load configuration for preview, then start the preview."""
        self.cam.stop()
        self.cam.configure(self._preview_configuration)
        self.cam.start()

    def update_capture_configuration(self, **kwargs):
        """Update the capture configuration.

        :param kwargs: Keyword arguments to update the configuration.
            - hflip: Horizontal flip.
            - vflip: Vertical flip.
            - resolution: (width, height) tuple.
        """
        self._hflip = kwargs.get("hflip", self._hflip)
        self._vflip = kwargs.get("vflip", self._vflip)
        self._capture_configuration["transform"] = self.transform

        resolution = kwargs.get("resolution", None)

        if resolution is not None:
            self._capture_configuration["main"]["size"] = resolution

    def update_preview_configuration(self, **kwargs):
        """Update the preview configuration.

        :param kwargs: Keyword arguments to update the configuration.
            - hflip: Horizontal flip.
            - vflip: Vertical flip.
        """
        self._hflip = kwargs.get("hflip", self._hflip)
        self._vflip = kwargs.get("vflip", self._vflip)
        self._preview_configuration["transform"] = self.transform

    def update_video_configuration(self, **kwargs):
        """Update the video configuration.

        :param kwargs: Keyword arguments to update the configuration.
            - hflip: Horizontal flip.
            - vflip: Vertical flip.
            - resolution: (width, height) tuple.
            - framerate: Frame rate in fps.
        """
        self._hflip = kwargs.get("hflip", self._hflip)
        self._vflip = kwargs.get("vflip", self._vflip)
        self._video_configuration["transform"] = self.transform

        resolution = kwargs.get("resolution", None)
        if resolution is not None:
            self._video_configuration["main"]["size"] = resolution

        framerate = kwargs.get("framerate", None)
        if framerate is not None:
            frame_rate_limit = 1.0e6 / framerate  # in microseconds
            self._video_configuration["controls"]["FrameDurationLimits"] = (
                int(frame_rate_limit),
                int(frame_rate_limit),
            )
