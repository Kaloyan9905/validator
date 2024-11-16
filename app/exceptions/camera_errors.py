class BaseCameraException(Exception):
    """
    Base class exception for camera related errors.
    """
    pass


class GrabFrameException(BaseCameraException):
    """
    Custom exception to indicate a failure to grab a frame.
    """
    pass
