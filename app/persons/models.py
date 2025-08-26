from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum

from app.database import Base
from enum import Enum as PyEnum


class sex_of_person(PyEnum):
    FEMALE = "Женщина"
    MALE = "Мужчина"

class Persons(Base):
    __tablename__="persons"

    id = Column(Integer, primary_key=True)
    tree_id = Column(ForeignKey("trees.id"))
    sex = Column(Enum(sex_of_person), nullable=False)
    first_name = Column(String, nullable=False) #nullable  говорит обязательное ли заполнение
    last_name = Column(String, nullable=False)
    fathers_name = Column(String)
    date_birth = Column(Date, nullable=False)
    date_death = Column(Date)
    description = Column(String)
    image_id =Column(Integer)
