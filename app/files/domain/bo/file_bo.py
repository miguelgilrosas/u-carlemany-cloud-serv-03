from pydantic import BaseModel


class FileModel(BaseModel):
    filename: str
    path: str
    owner: int
    desc: str
    number_of_pages: int
