from app.repository.base import BaseRepo
from app.users.models import Users


class UsersRepo(BaseRepo):
    model = Users