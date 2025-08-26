from app.relationships.models import Relationships
from app.repository.base import BaseRepo
from sqlalchemy import select, and_
from app.persons.models import Persons
from app.relationships.schemas import SCreateInitialRelation, RelationType
from fastapi import HTTPException, status

valid_relation_types_by_sex = {
    "Мужчина": {
        RelationType.FATHER,
        RelationType.SON,
        RelationType.BROTHER,
        RelationType.HUSBAND,
        RelationType.GRANDFATHER,
        RelationType.STEPFATHER,
        RelationType.UNCLE,
        RelationType.FATHER_IN_LAW,
        RelationType.FATHER_IN_LAW_W,
        RelationType.GRANDSON,
        RelationType.STEPSON,
        RelationType.NEPHEW,
        RelationType.HALF_BROTHER,
        RelationType.COUSIN_BROTHER,
        RelationType.BROTHER_IN_LAW,
        RelationType.BROTHER_IN_LAW_W,
        RelationType.SON_IN_LAW,
        RelationType.BROTHER_IN_LAW_H,
        RelationType.FORMER_HUSBAND,
        RelationType.GREAT_GRANDFATHER,
        RelationType.GREAT_GRANDSON,
        RelationType.RELATIVE,
    },
    "Женщина": {
        RelationType.MOTHER,
        RelationType.DAUGHTER,
        RelationType.SISTER,
        RelationType.WIFE,
        RelationType.GRANDMOTHER,
        RelationType.STEPMOTHER,
        RelationType.AUNT,
        RelationType.MOTHER_IN_LAW,
        RelationType.MOTHER_IN_LAW_W,
        RelationType.GRANDDAUGHTER,
        RelationType.STEPDAUGHTER,
        RelationType.NIECE,
        RelationType.HALF_SISTER,
        RelationType.COUSIN_SISTER,
        RelationType.SISTER_IN_LAW,
        RelationType.SISTER_IN_LAW_W,
        RelationType.DAUGHTER_IN_LAW,
        RelationType.SISTER_IN_LAW_H,
        RelationType.FORMER_WIFE,
        RelationType.GREAT_GRANDMOTHER,
        RelationType.GREAT_GRANDDAUGHTER,
        RelationType.RELATIVE,
    }
}


reverse_relations = {
    RelationType.FATHER: { "Мужчина": RelationType.SON, "Женщина": RelationType.DAUGHTER },
    RelationType.MOTHER: { "Мужчина": RelationType.SON, "Женщина": RelationType.DAUGHTER },
    RelationType.SON:    { "Мужчина": RelationType.FATHER, "Женщина": RelationType.MOTHER },
    RelationType.DAUGHTER: { "Мужчина": RelationType.FATHER, "Женщина": RelationType.MOTHER },
    RelationType.BROTHER: {"Мужчина": RelationType.BROTHER, "Женщина": RelationType.SISTER},
    RelationType.SISTER: {"Мужчина": RelationType.BROTHER, "Женщина": RelationType.SISTER},
    RelationType.HUSBAND: {"Мужчина": None, "Женщина": RelationType.WIFE},
    RelationType.WIFE: {"Мужчина": RelationType.HUSBAND, "Женщина": None},
    RelationType.GRANDMOTHER: {"Мужчина": RelationType.GRANDSON, "Женщина": RelationType.GRANDDAUGHTER},
    RelationType.GRANDFATHER: {"Мужчина": RelationType.GRANDSON, "Женщина": RelationType.GRANDDAUGHTER},
    RelationType.RELATIVE: {"Мужчина": RelationType.RELATIVE, "Женщина": RelationType.RELATIVE},
    RelationType.STEPFATHER: {"Мужчина": RelationType.STEPSON, "Женщина": RelationType.STEPDAUGHTER},
    RelationType.STEPMOTHER: {"Мужчина": RelationType.STEPSON, "Женщина": RelationType.STEPDAUGHTER},
    RelationType.UNCLE: {"Мужчина": RelationType.NEPHEW, "Женщина": RelationType.NIECE},
    RelationType.AUNT: {"Мужчина": RelationType.NEPHEW, "Женщина": RelationType.NIECE},
    RelationType.MOTHER_IN_LAW: {"Мужчина": None, "Женщина": RelationType.DAUGHTER_IN_LAW},
    RelationType.FATHER_IN_LAW: {"Мужчина": None, "Женщина": RelationType.DAUGHTER_IN_LAW},
    RelationType.MOTHER_IN_LAW_W: {"Мужчина": RelationType.SON_IN_LAW, "Женщина": None},
    RelationType.FATHER_IN_LAW_W: {"Мужчина": RelationType.SON_IN_LAW, "Женщина": None},
    RelationType.GRANDSON: {"Мужчина": RelationType.GRANDFATHER, "Женщина": RelationType.GRANDMOTHER},
    RelationType.GRANDDAUGHTER: {"Мужчина": RelationType.GRANDFATHER, "Женщина": RelationType.GRANDMOTHER},
    RelationType.STEPSON: {"Мужчина": RelationType.STEPFATHER, "Женщина": RelationType.STEPMOTHER},
    RelationType.STEPDAUGHTER: {"Мужчина": RelationType.STEPFATHER, "Женщина": RelationType.STEPMOTHER},
    RelationType.NEPHEW: {"Мужчина": RelationType.UNCLE, "Женщина": RelationType.AUNT},
    RelationType.NIECE: {"Мужчина": RelationType.UNCLE, "Женщина": RelationType.AUNT},
    RelationType.HALF_SISTER: {"Мужчина": RelationType.HALF_BROTHER, "Женщина": RelationType.HALF_SISTER},
    RelationType.HALF_BROTHER: {"Мужчина": RelationType.HALF_BROTHER, "Женщина": RelationType.HALF_SISTER},
    RelationType.COUSIN_BROTHER: {"Мужчина": RelationType.COUSIN_BROTHER, "Женщина": RelationType.COUSIN_SISTER},
    RelationType.COUSIN_SISTER: {"Мужчина": RelationType.COUSIN_BROTHER, "Женщина": RelationType.COUSIN_SISTER},
    RelationType.BROTHER_IN_LAW: {"Мужчина": None, "Женщина": RelationType.SISTER_IN_LAW_H},
    RelationType.SISTER_IN_LAW: {"Мужчина": None, "Женщина": RelationType.SISTER_IN_LAW_H},
    RelationType.BROTHER_IN_LAW_W: {"Мужчина": RelationType.BROTHER_IN_LAW_H, "Женщина": None},
    RelationType.SISTER_IN_LAW_W: {"Мужчина": RelationType.BROTHER_IN_LAW_H, "Женщина": None},
    RelationType.DAUGHTER_IN_LAW: {"Мужчина": RelationType.FATHER_IN_LAW, "Женщина": RelationType.MOTHER_IN_LAW},
    RelationType.SON_IN_LAW: {"Мужчина": RelationType.FATHER_IN_LAW_W, "Женщина": RelationType.MOTHER_IN_LAW_W},
    RelationType.SISTER_IN_LAW_H: {"Мужчина": RelationType.BROTHER_IN_LAW, "Женщина": RelationType.SISTER_IN_LAW},
    RelationType.BROTHER_IN_LAW_H: {"Мужчина": RelationType.BROTHER_IN_LAW_W, "Женщина": RelationType.SISTER_IN_LAW_W},
    RelationType.FORMER_WIFE: {"Мужчина": RelationType.FORMER_HUSBAND, "Женщина": None},
    RelationType.FORMER_HUSBAND: {"Мужчина": None, "Женщина": RelationType.FORMER_WIFE},
    RelationType.GREAT_GRANDFATHER: {"Мужчина": RelationType.GREAT_GRANDSON, "Женщина": RelationType.GREAT_GRANDDAUGHTER},
    RelationType.GREAT_GRANDMOTHER: {"Мужчина": RelationType.GREAT_GRANDSON, "Женщина": RelationType.GREAT_GRANDDAUGHTER},
    RelationType.GREAT_GRANDSON: {"Мужчина": RelationType.GREAT_GRANDFATHER, "Женщина": RelationType.GREAT_GRANDMOTHER},
    RelationType.GREAT_GRANDDAUGHTER: {"Мужчина": RelationType.GREAT_GRANDFATHER, "Женщина": RelationType.GREAT_GRANDMOTHER},
}


class RelationshipsRepo(BaseRepo):
    model = Relationships

    async def create_initial_relation(self, data: SCreateInitialRelation, db):

        def validate_sex(person: Persons, person_label: str) -> str:
            if not person:
                raise HTTPException(status_code=404, detail=f"{person_label} не найден.")
            if not person.sex:
                raise HTTPException(status_code=400, detail=f"У {person_label.lower()} не указан пол.")
            sex = person.sex
            if sex not in ("Мужчина", "Женщина"):
                raise HTTPException(status_code=400, detail=f"Пол {person_label.lower()} должен быть 'MAL' или 'FEMALE'.")
            return sex


        # Проверка на наличие связей у person_id_1
        result = await db.execute(
            select(Relationships).where(
                and_(
                    Relationships.tree_id == data.tree_id,
                    (Relationships.person_id_1 == data.person_id_1) |
                    (Relationships.person_id_2 == data.person_id_1)
                )
            )
        )

        if result.scalars().first():
            raise HTTPException(status_code=400, detail="У этого человека уже есть связи в дереве.")


        # Получение пола первого человека
        first_person = await db.get(Persons, data.person_id_1)
        first_sex = validate_sex(first_person, "Первый человек")

        if data.relation_type not in valid_relation_types_by_sex[first_sex]:
            raise HTTPException(
                status_code=400,
                detail=f"Тип связи '{data.relation_type.name}' не соответствует полу '{first_sex}' первого человека."
            )


        # Получение пола второго человека

        second_person = await db.get(Persons, data.person_id_2)
        second_sex = validate_sex(second_person, "Второй человек")

        # Проверка валидности связи
        if data.relation_type not in reverse_relations:
            raise HTTPException(status_code=400, detail="Невозможно построить обратную связь для данного типа.")

        reverse_type = reverse_relations[data.relation_type][second_sex]
        if reverse_type is None:
            raise HTTPException(status_code=400, detail="Обратная связь невозможна для данного пола.")

        existing = await db.execute(
            select(Relationships).where(
                and_(
                    Relationships.tree_id == data.tree_id,
                    (
                            (Relationships.person_id_1 == data.person_id_1) &
                            (Relationships.person_id_2 == data.person_id_2) &
                            (Relationships.relation_type == data.relation_type)
                    ) |
                    (
                            (Relationships.person_id_1 == data.person_id_2) &
                            (Relationships.person_id_2 == data.person_id_1) &
                            (Relationships.relation_type == reverse_type)
                    )
                )
            )
        )

        if existing.scalars().first():
            raise HTTPException(status_code=400, detail="Такая связь уже существует.")

        # Добавление обеих связей
        db.add_all([
            Relationships(
                tree_id=data.tree_id,
                person_id_1=data.person_id_1,
                person_id_2=data.person_id_2,
                relation_type=data.relation_type
            ),
            Relationships(
                tree_id=data.tree_id,
                person_id_1=data.person_id_2,
                person_id_2=data.person_id_1,
                relation_type=reverse_type
            )
        ])
        await db.commit()
