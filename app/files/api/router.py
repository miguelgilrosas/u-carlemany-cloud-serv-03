from fastapi import APIRouter, Body, UploadFile, File, Header, HTTPException
from fastapi.responses import FileResponse
import uuid
from pydantic import BaseModel

from app.files.dependency_injection.domain.delete_file_controllers import DeleteFileControllers
from app.files.dependency_injection.domain.get_file_controllers import GetFileControllers
from app.files.dependency_injection.domain.get_files_by_token_controllers import GetFilesByTokenControllers
from app.files.dependency_injection.domain.merge_files_controllers import MergeFilesControllers
from app.files.dependency_injection.domain.post_file_content_controllers import PostFileContentControllers
from app.files.dependency_injection.domain.post_file_controllers import PostFileControllers
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistences.exceptions import BadTokenException, NotFoundException

router = APIRouter()

files = {}


class FileInput(BaseModel):
    filename: str
    desc: str
    number_of_pages: int


@router.get("/")
async def get_files(auth: str = Header()) -> list[FileBO]:
    get_files_by_token_controller = GetFilesByTokenControllers.carlemany()

    try:
        result = await get_files_by_token_controller(token=auth)

    except BadTokenException:
        raise HTTPException(status_code=403, detail='Forbidden')

    return result


@router.post("/")
async def post_file(
    data_input: FileInput = Body(),
    auth: str = Header()
) -> FileBO:

    file = FileBO(
        filename=data_input.filename,
        path='',
        owner=-1,
        desc=data_input.desc,
        number_of_pages=data_input.number_of_pages
    )

    post_file_controller = PostFileControllers.carlemany()
    try:
        result = await post_file_controller(token=auth, file=file)

    except BadTokenException:
        raise HTTPException(status_code=403, detail='Forbidden')

    return result


class MergeInput(BaseModel):
    file_id1: int
    file_id2: int


@router.post("/merge")
async def merge_files(
    input_data: MergeInput = Body(),
    auth: str = Header()
) -> dict[str, int]:
    merge_files_controller = MergeFilesControllers.carlemany()

    try:
        new_file_id = await merge_files_controller(file_id1=input_data.file_id1, file_id2=input_data.file_id2, token=auth)

    except BadTokenException:
        raise HTTPException(status_code=403, detail='Forbidden')

    except NotFoundException:
        raise HTTPException(status_code=404, detail='Not found')

    return {"file_id": new_file_id}


@router.post("/{file_id}")
async def post_file_by_id(
    file_id: int,
    auth: str = Header(),
    input_file: UploadFile = File()
) -> dict[str, str]:
    post_file_content_controller = PostFileContentControllers.carlemany()

    try:
        return await post_file_content_controller(file_id=file_id, token=auth, input_file=input_file)

    except NotFoundException:
        raise HTTPException(status_code=404, detail='Not found')

    except BadTokenException:
        raise HTTPException(status_code=403, detail='Forbidden')


@router.get("/{file_id}")
async def get_file_by_id(
    file_id: str,
    auth: str = Header()
) -> FileResponse:
    get_file_controller = GetFileControllers.carlemany()

    try:
        file = await get_file_controller(file_id=file_id, token=auth)

    except NotFoundException:
        raise HTTPException(status_code=404, detail='Not found')

    except BadTokenException:
        raise HTTPException(status_code=403, detail='Forbidden')

    return FileResponse(
        path=file.path,
        filename=file.filename,
        media_type='application/pdf'
    )


@router.delete("/{file_id}")
async def delete_file_by_id(
    file_id: str,
    auth: str = Header()
) -> dict[str, str]:
    delete_file_controller = DeleteFileControllers.carlemany()

    try:
        await delete_file_controller(file_id=file_id, token=auth)

    except BadTokenException:
        raise HTTPException(status_code=403, detail='Forbidden')

    except NotFoundException:
        raise HTTPException(status_code=404, detail='Not found')

    return {"status": "ok"}
