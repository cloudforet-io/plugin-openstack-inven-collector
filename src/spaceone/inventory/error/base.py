from spaceone.inventory.model.common.response import BaseResponse

from typing import Optional  # pylint: disable=unused-import

# Error message that is called when a user hits either a MemoryError or OverflowError
# when trying to send large files via a multipart/form-data post/patch through
# the requests library.
FILE_SIZE_WARNING = (
    "One of the file(s) you are trying to upload may be too large. Install these"
    " additional dependencies to handle the large file upload and try again."
    "\npip install requests[security]"
)


class CollectorError(Exception):
    """Common base class for all exceptions raised by the library functions. All
    custom exceptions are derived from this type.
    """

    def __init__(self, message: str = None, cause: Exception = None) -> None:
        """Initalize the error object.

        Optionally accepts a custom message and cause. If provided, the cause is
        the exception object that was handled when this exception is created.

        Args:
            message: A human readable message that explains the error.
            cause: An exception object that caused this exception to be raised.
        """

        msg = message if message else ""
        if cause:
            self.cause = cause
            msg += " Caused by %r" % cause
            if getattr(cause, "response", None) is not None:
                try:
                    self._response = BaseResponse(cause.response)  # type: ignore
                    err_msg = cause.response.json().get("error", {}).get("message")  # type: ignore
                    if err_msg:
                        msg += ": %s" % err_msg
                except Exception:  # pylint: disable=broad-except
                    # the error response wasn't json so there's nothing additional
                    # we will add
                    pass

        super().__init__(msg)

    @property
    def http_err_response(self) -> Optional[BaseResponse]:
        """Describes a response to an API request that contains an error.

        Returns:
            Response object if the exception was raised because of an API failure (HTTP status code of 400 or higher). None if the exception was not related to an API error.
        """

        return getattr(self, "_response", None)
