from pydantic import BaseModel
from typing import Optional


class UserBO(BaseModel):
    id: Optional[int] = None
    username: str
    password: bytes
    mail: str
    year_of_birth: int
