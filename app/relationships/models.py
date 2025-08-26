from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import validates

from  app.database import Base
from enum import Enum as PyEnum


class RelationType(PyEnum):
    MOTHER = "Мать"
    FATHER = "Отец"
    DAUGHTER = "Дочь"
    SON = "Сын"
    BROTHER = "Брат"
    SISTER = "Сестра"
    HUSBAND = "Муж"
    WIFE = "Жена"
    GRANDMOTHER = "Бабушка"
    GRANDFATHER = "Дедушка"
    RELATIVE = "Родственник"
    STEPFATHER = "Отчим"
    STEPMOTHER = "Мачеха"
    UNCLE = "Дядя"
    AUNT = "Тётя"
    MOTHER_IN_LAW = "Свекровь"
    FATHER_IN_LAW = "Свёкр"
    MOTHER_IN_LAW_W = "Тёщя"
    FATHER_IN_LAW_W = "Тесть"
    GRANDSON = "Внук"
    GRANDDAUGHTER = "Внучка"
    STEPSON = "Пасынок"
    STEPDAUGHTER = "Падчерица"
    NEPHEW = "Племянник"
    NIECE = "Племянница"
    HALF_BROTHER = "Сводный брат"
    HALF_SISTER = "Сводная сестра"
    COUSIN_BROTHER = "Двоюродный брат"
    COUSIN_SISTER = "Двоюродная сестра"
    BROTHER_IN_LAW= "Деверь"
    SISTER_IN_LAW = "Золовка"
    BROTHER_IN_LAW_W = "Шурин"
    SISTER_IN_LAW_W = "Свояченица"
    DAUGHTER_IN_LAW = "Невестка (жена сына)"
    SON_IN_LAW = "Зять (муж дочери)"
    SISTER_IN_LAW_H = "Невестка (жена брата)"
    BROTHER_IN_LAW_H = "Зять (муж сестры)"
    FORMER_WIFE = "Бывшая жена"
    FORMER_HUSBAND = "Бывший муж"
    GREAT_GRANDFATHER = "Прадедушка"
    GREAT_GRANDMOTHER = "Прабабушка"
    GREAT_GRANDSON = "Правнук"
    GREAT_GRANDDAUGHTER = "Правнучка"




class Relationships(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)
    tree_id = Column(ForeignKey("trees.id"))
    person_id_1 = Column(ForeignKey("persons.id"))
    person_id_2 = Column(ForeignKey("persons.id"))
    relation_type = Column(Enum(RelationType), nullable=False)

    @validates('person_id_1', 'person_id_2')
    def validate_person_ids(self, key, value):
        """Проверяет, чтобы person_id_1 и person_id_2 не совпадали"""
        if key == 'person_id_2' and value == self.person_id_1:
            raise ValueError("person_id_1 и person_id_2 не могут быть одинаковыми.")
        return value