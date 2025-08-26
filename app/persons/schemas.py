from datetime import date
from typing import Optional

from pydantic import BaseModel
from enum import Enum

class SexEnum(str, Enum):
    MALE = 'Мужчина'
    FEMALE = 'Женщина'


class SPersons(BaseModel):
    id: int
    tree_id: int
    first_name: str
    last_name: str
    fathers_name: Optional[str] = None
    sex: SexEnum
    date_birth: date
    date_death: Optional[date] = None  # Сделаем дату смерти необязательной
    description: Optional[str] = None
    image_id: Optional[int] = None

class SPersonsUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    fathers_name: Optional[str] = None
    sex: Optional[SexEnum] = None
    date_birth: Optional[date] = None
    date_death: Optional[date] = None
    description: Optional[str] = None
    image_id: Optional[int] = None

class SPersonsCreate(BaseModel):
    first_name: str
    last_name: str
    fathers_name: Optional[str] = None
    sex: SexEnum
    date_birth: date
    date_death: Optional[date] = None
    description: Optional[str] = None
    image_id: Optional[int] = None

    class Config:
        orm_mode = True
