#
#   Custom exceptions on transactions.
#
# =================================================================

from rest_framework import status
from rest_framework.exceptions import APIException


'''   Raised when a user attempts to modify a field that they don't have
      permission to.
'''
class FieldPermissionError(Exception):
    pass


'''   Raised when a user performs a bad request on a Transaction. '''
class BadTransactionRequest(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'bad transaction request.'

    def __init__(self, detail=None):

        if detail: self.detail = detail

