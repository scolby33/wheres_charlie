class WheresCharlieError(Exception):
    def __init__(self, message):
        super(WheresCharlieError, self).__init__(message)


class ClientError(WheresCharlieError):
    def __init__(self, message, status_code=404, payload=None):
        super(ClientError, self).__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class ServerError(WheresCharlieError):
    def __init__(self, message, status_code=500, payload=None):
        super(ServerError, self).__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
