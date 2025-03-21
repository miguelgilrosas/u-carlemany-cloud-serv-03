from fastapi import APIRouter, Body, UploadFile, File, Header, HTTPException
from fastapi.responses import FileResponse
from pypdf import PdfMerger
import uuid
from pydantic import BaseModel
import aiohttp
import json
import os

router = APIRouter()

authentication_url = '0.0.0.0'
files = {}


class FileModel(BaseModel):
    filename: str
    path: str
    owner: int
    desc: str
    number_of_pages: int


class FileInput(BaseModel):
    filename: str
    desc: str
    number_of_pages: int


@router.get("/")
async def get_files(auth: str = Header()) -> list[dict[str, FileModel]]:
    user = await auth_check(auth)

    result = []
    user_id = user['id']

    for key, value in files.items():
        if value.owner == user_id:
            result.append({key: value})

    return result


@router.post("/")
async def post_file(
    data_input: FileInput = Body(),
    auth: str = Header()
) -> dict[str, str]:
    user = await auth_check(auth)

    file_id = str(uuid.uuid4())
    while file_id in files:
        file_id = str(uuid.uuid4())

    files[file_id] = FileModel(
        filename=data_input.filename,
        path='',
        owner=user['id'],
        desc=data_input.desc,
        number_of_pages=data_input.number_of_pages
    )

    return {'file_id': file_id}


class MergeInput(BaseModel):
    file_id1: str
    file_id2: str


@router.post("/merge")
async def merge_files(
    input_data: MergeInput = Body(),
    auth: str = Header()
) -> dict[str, str]:
    user = await auth_check(auth)

    if input_data.file_id1 not in files or input_data.file_id2 not in files:
        raise HTTPException(status_code=404, detail='Not found')

    file1 = files[input_data.file_id1]
    file2 = files[input_data.file_id2]
    if file1.owner != user['id'] or file2.owner != user['id']:
        raise HTTPException(status_code=403, detail='Forbidden')

    merged_id = str(uuid.uuid4())
    while merged_id in files:
        merged_id = str(uuid.uuid4())
    merged = "files/" + merged_id + ".pdf"
    pdfs = [file1.path, file2.path]
    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    name = merged
    merger.write(name)
    merger.close()

    files[merged_id] = FileModel(
        filename='Merged.pdf',
        path=merged,
        author=user['username'],
        desc='Merged file created from "' + file1.path + '" and "' + file2.path + '"',
        number_of_pages=file1.number_of_pages + file2.number_of_pages
    )

    return {"file_id": merged_id}


@router.post("/{file_id}")
async def post_file_by_id(
    file_id: str,
    auth: str = Header(),
    input_file: UploadFile = File()
) -> dict[str, str]:
    user = await auth_check(auth)

    if file_id not in files:
        raise HTTPException(status_code=404, detail='Not found')

    file = files[file_id]

    if user['id'] != file.owner:
        raise HTTPException(status_code=403, detail='Forbidden')

    prefix = 'files/'
    path = prefix + file_id + '.pdf'
    with open(path, "wb") as buffer:
        while chunk := await input_file.read(8192):
            buffer.write(chunk)
    file.path = path

    return {"status": "ok"}


@router.get("/{file_id}")
async def get_file_by_id(
    file_id: str,
    auth: str = Header()
) -> FileResponse:
    user = await auth_check(auth)

    if file_id not in files:
        raise HTTPException(status_code=404, detail='Not found')

    file = files[file_id]

    if user['id'] != file.owner:
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
    user = await auth_check(auth)

    if file_id not in files:
        raise HTTPException(status_code=404, detail='Not found')

    file = files[file_id]

    if user['id'] != file.owner:
        raise HTTPException(status_code=403, detail='Forbidden')

    if file.path != '':
        os.remove(file.path)
    del files[file_id]

    return {"status": "ok"}


async def introspect(auth: str):
    headers = {
        "accept": "application/json",
        "auth": auth
    }
    url = "http://" + authentication_url + ":80/auth/introspect"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as response:
            status_code = response.status
            if status_code != 200:
                return None
            body = await response.text()
            return body


async def auth_check(auth):
    auth_response = await introspect(auth=auth)
    if auth_response is None:
        raise HTTPException(status_code=403, detail='Forbidden')

    return json.loads(auth_response)
