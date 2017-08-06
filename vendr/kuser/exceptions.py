#
# Custom exceptions on notifications.
#
# ===================================================================

from rest_framework import status
from rest_framework.exceptions import APIException


'''   Raised when a user sends a bad request on a Notification. '''
class InvalidFieldRequest(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail      = 'bad notification request.'

    def __init__(self, detail=None):

        if detail: self.detail = detail

'''   Raised when a user requests a non-existent notification. '''
class NotificationNotFound(APIException):

    status_code = status.HTTP_404_NOT_FOUND
    detail      = 'notification not found.'

    def __init__(self, detail=None):

        if detail: self.detail = detail


'''   Raised when a user queries a notification that they do not own. '''
class BadUserRequest(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail      = 'invalid user.'

    def __init__(self, detail=None):

        if detail: self.detail = detail

