from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.relationships.repository import RelationshipsRepo
from app.relationships.schemas import SCreateInitialRelation
from app.database import async_session_maker

router = APIRouter()

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

@router.post("/initial")
async def create_initial_rel(
    data: SCreateInitialRelation,
    db: AsyncSession = Depends(get_db)
):
    repo = RelationshipsRepo()
    await repo.create_initial_relation(data, db)
    return {"detail": "Связь успешно создана"}
