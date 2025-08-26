from fastapi import APIRouter, Depends

from app.trees.repository import TreesRepo
from app.trees.schemas import STrees
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/trees",
    tags=["Мои родословные деревья"]
)

@router.get("", response_model=list[STrees])
async def get_trees(user: Users = Depends(get_current_user)):
    result = await TreesRepo.find_all(users_tree_id=user.id)
    return result
