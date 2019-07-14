class MoxtraException(Exception):
    pass


class TransportError(MoxtraException):
    pass


class NotFoundError(TransportError):
    ' 404 '


HTTP_EXCEPTIONS = {
    404: NotFoundError,
}
