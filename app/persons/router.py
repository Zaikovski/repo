from fastapi import APIRouter, Depends

from app.exceptions import IncorrectTreeIDException, IncorrectPersonIDException
from app.persons.repository import PersonsRepo
from app.persons.schemas import SPersons, SPersonsUpdate, SPersonsCreate
from app.trees.repository import TreesRepo
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/trees/families",
    tags=["Моя семья"]
)

@router.get("/{tree_id}", response_model=list[SPersons])
async def get_persons(tree_id:int, user: Users = Depends(get_current_user)):
    tree =await TreesRepo.find_one_or_none(id=tree_id, users_tree_id=user.id)
    if not tree:
        raise IncorrectTreeIDException()
    result = await PersonsRepo.find_all(tree_id=tree.id)
    return result

@router.put("/{tree_id}/person/{person_id}", response_model=SPersons)
async def update_person(
    tree_id: int,
    person_id: int,
    person_data: SPersonsUpdate,
    user: Users = Depends(get_current_user)
):
    tree = await TreesRepo.find_one_or_none(id=tree_id, users_tree_id=user.id)
    if not tree:
        raise IncorrectTreeIDException()

    updated_person = await PersonsRepo.update(
        object_id=person_id,
        data=person_data.dict(exclude_unset=True),
        tree_id=tree.id  # ограничение: обновляем только в рамках своей семьи
    )
    if not updated_person:
        raise IncorrectPersonIDException

    return updated_person

@router.post("/{tree_id}/person", response_model=SPersons)
async def add_person(
    tree_id: int,
    person_data: SPersonsCreate,
    user: Users = Depends(get_current_user)
):
    tree = await TreesRepo.find_one_or_none(id=tree_id, users_tree_id=user.id)
    if not tree:
        raise IncorrectTreeIDException()

    # Добавляем нового человека без создания связей
    new_person = await PersonsRepo.add_and_return(tree_id=tree.id, **person_data.dict())
    return new_person
