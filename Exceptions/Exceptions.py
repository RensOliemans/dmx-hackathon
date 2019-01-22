class InvalidRequestException(Exception):
    """Exception thrown when an invalid request is done. Usually when 'ease' is invalid, or the color isn't good"""
    status_code = 400

    def __init__(self, message, inner_exception=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.inner_exception = inner_exception
        if status_code is not None:
            self.status_code = status_code


class ControllerSetLEDException(Exception):
    """Exception thrown when SetLED goes wrong. Often when there is no DMX controller plugged to the Pi"""
    status_code = 500

    def __init__(self, message, inner_exception=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.inner_exception = inner_exception
        if status_code is not None:
            self.status_code = status_code
