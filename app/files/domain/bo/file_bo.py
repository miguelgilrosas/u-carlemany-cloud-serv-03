from typing import Optional
from pydantic import BaseModel


class FileBO(BaseModel):
    id: Optional[int] = None
    filename: str
    path: str
    owner: int
    desc: str
    number_of_pages: int
