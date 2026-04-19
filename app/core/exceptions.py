"""
В этом файле вы описываете ваши HTTP-исключения в стиле CategoryNotFoundError(BaseHTTPException). То есть вы создаёте BaseHTTPException, который наследуется от HTTPException, а затем создаёте набор конкретных исключений для Auth Service. Здесь должны быть как минимум UserAlreadyExistsError (409), InvalidCredentialsError (401), InvalidTokenError (401), TokenExpiredError (401), UserNotFoundError (404), PermissionDeniedError (403). Эти исключения должны использоваться в usecase и dependencies вместо “ручных” raise HTTPException.
"""

from fastapi.exceptions import HTTPException
from fastapi import status


class BaseHTTPException (HTTPException):
    pass

class UserAlreadyExistsError(BaseHTTPException):
    def __init__(self, detail: str = "User already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidTokenError(BaseHTTPException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InvalidCredentialsError(BaseHTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class TokenExpiredError(BaseHTTPException):
    def __init__(self, detail: str = "Token expired"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UserNotFoundError(BaseHTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class PermissionDeniedError(BaseHTTPException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class InternalServerError(BaseHTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)