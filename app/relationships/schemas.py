from pydantic import BaseModel
from enum import Enum
from typing import Literal

class RelationType(str, Enum):
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

class SCreateInitialRelation(BaseModel):
    tree_id: int
    person_id_1: int  # Тот, кого пользователь добавил
    person_id_2: int  # Родственник
    relation_type: RelationType
