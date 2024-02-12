# Development tools


class SimCamera:
    """Simulation camera to use when picamera2 is not installed."""

    def __init__(self):
        pass

    def configure(self, *args, **kwargs):
        print("Configure called.")

    def create_preview_configuration(self):
        print("Create preview configuration called.")
        return {}

    def create_still_configuration(self):
        print("Create still configuration called.")
        return {}

    def start(self):
        print("camera start called.")


class Transform:
    """Transformation class to use when picamera2 is not installed."""

    def __init__(self, *args, **kwargs):
        pass
