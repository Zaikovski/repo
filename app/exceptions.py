from fastapi import HTTPException, status

class TreesException(HTTPException):
    status_code = 500
    detail = ""
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException (TreesException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"

class IncorrectEmailOrPasswordException(TreesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный логин или пароль"


class TokenExpiredException(TreesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(TreesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(TreesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(TreesException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"


class IncorrectTreeIDException(TreesException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "У вас нет доступа к этому дереву"

class IncorrectPersonIDException(TreesException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Данный человек не найден"
