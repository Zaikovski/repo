
from pydantic import BaseModel


class STrees(BaseModel):
    id: int
    users_tree_id: int
    name: str

    class Config:
        orm_mode = True