class InvalidRequestException(Exception):
    status_code = 400

    def __init__(self, message, inner_exception=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.inner_exception = inner_exception
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['inner_exception'] = str(self.inner_exception)
        return rv


class ControllerSetLEDException(Exception):
    status_code = 500

    def __init__(self, message, inner_exception=None, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.inner_exception = inner_exception
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['inner_exception'] = str(self.inner_exception)
        return rv
