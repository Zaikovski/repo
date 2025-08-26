from app.database import async_session_maker
from sqlalchemy import select, insert
from sqlalchemy import update as sqlalchemy_update

class BaseRepo:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    @classmethod
    async def find_one_or_none(cls, **filter):
        async with async_session_maker() as session:
            filters = [getattr(cls.model, key) == value for key, value in filter.items()]
            query = select(cls.model).filter(*filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter):
        async with async_session_maker() as session:
            filters = [getattr(cls.model, key) == value for key, value in filter.items()]
            query = select(cls.model).filter(*filters)
            result = await session.execute(query)
            return result.scalars().all()  #  возвращаются ORM-объекты

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, object_id: int, data: dict, **filter):
        async with async_session_maker() as session:
            filters = [getattr(cls.model, key) == value for key, value in filter.items()]
            filters.append(cls.model.id == object_id)
            stmt = (
                sqlalchemy_update(cls.model)
                .where(*filters)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(stmt)
            await session.commit()

            # Возвращаем обновлённый объект
            query = select(cls.model).filter(cls.model.id == object_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_and_return(cls, **data):
        async with async_session_maker() as session:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
