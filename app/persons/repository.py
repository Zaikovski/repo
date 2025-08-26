from app.persons.models import Persons
from app.repository.base import BaseRepo



class PersonsRepo(BaseRepo):
    model = Persons
