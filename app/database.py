from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings



engine = create_async_engine(settings.DATABASE_URL) #движок чтобы создать сессию

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) #генератор сессий чтобы передавать транзакции

class Base(DeclarativeBase): #этот класс используется для миграций, чтобы сравнить состояние в коде и в базе данных, если в базе данных нет то он меняет таблицу. Все классы будут наследоваться отсюда
    pass