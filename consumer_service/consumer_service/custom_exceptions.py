from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException


class Not_Found(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    error = True

    def __init__(self, msg):
        detail = {"msg": msg}
        super().__init__(detail=detail, code=self.status_code)


class Validation_Error(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, msg):
        detail = {"msg": msg}
        super().__init__(detail=detail, code=self.status_code)


class Custom_Error(APIException):

    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        self.detail = {"msg": message}
        super().__init__(detail=self.detail, code=status_code)


class Invalid_credentials(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    error = True

    def __init__(self, msg):
        detail = {"msg": msg}
        super().__init__(detail, code=self.status_code)
