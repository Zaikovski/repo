from datetime import datetime, timezone

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UserIsNotPresentException
from app.users.repository import UsersRepo


def get_token(request: Request):
    token = request.cookies.get("tree_access_token")
    if not token:
        raise TokenAbsentException()
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException()
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException()
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException()
    user = await UsersRepo.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException()

    return user