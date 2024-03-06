from fastapi import HTTPException, status


class CustomException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(CustomException):
    status_code = status.HTTP_409_CONFLICT
    detail = ("User already exists",)


class IncorrectEmailOrPasswordException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ("Incorrect email or password",)


class TokenExpiredException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ("Expired token",)


class TokenAbsentException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ("Unknown token",)


class IncorrectTokenException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ("Incorrect token format",)


class UserIsNotPresentException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
