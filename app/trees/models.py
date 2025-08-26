from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base

class Trees(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True)
    users_tree_id = Column(ForeignKey("users.id"))
    name = Column(String, nullable=False)