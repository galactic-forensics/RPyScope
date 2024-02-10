# Development tools


class SimCamera:
    """Simulation camera to use when picamera2 is not installed."""

    def __init__(self):
        pass

    def configure(self, *args, **kwargs):
        print("Configure called.")

    def create_preview_configuration(self):
        print("Create preview configuration called.")

    def start(self):
        print("camera start called.")
