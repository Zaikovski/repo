from fastapi import FastAPI, Depends
from datetime import date
from typing import Optional
from pydantic import BaseModel

from app.persons.router import router as router_persons
from app.trees.router import router as router_trees
from app.users.router import router as router_users
from app.relationships import router as relationships_router

app = FastAPI()

app.include_router(router_users)
app.include_router(router_persons)
app.include_router(router_trees)
app.include_router(relationships_router.router)

class PersonSearchArgs:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        fathers_name: str,
        birth_date: date,
        death_date: Optional[date] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.fathers_name = fathers_name
        self.birth_date = birth_date
        self.death_date = death_date

class SPerson(BaseModel):
    first_name: str
    last_name: str
    fathers_name: str
    birth_date: date
    death_date: Optional[date] = None
