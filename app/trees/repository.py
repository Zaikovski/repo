from app.repository.base import BaseRepo
from app.trees.models import Trees


class TreesRepo(BaseRepo):
    model = Trees
