class CollectorError(Exception):
    """Common base class for all exceptions raised by the library functions. All
    custom exceptions are derived from this type.
    """

    def __init__(self, message: str = None, cause: Exception = None) -> None:
        msg = message if message else ""
        if cause:
            self.cause = cause
            msg += " Caused by %r" % cause

        super().__init__(msg)
