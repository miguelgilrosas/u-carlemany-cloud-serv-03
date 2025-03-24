from app.files.domain.persistences.exceptions import NotFoundException, BadTokenException
from app.files.domain.persistences.file_bo_interface import FileBOInterface
from app.files.domain.bo.file_bo import FileBO
from app.files.models import FileDB


class FileBOPostgresPersistenceService(FileBOInterface):
    async def get_files_by_owner_id(self, owner_id: int) -> list[FileBO]:
        files = await FileDB.filter(**{'owner': owner_id})

        result = []
        for file in files:
            result.append(
                FileBO(
                    id=file.id,
                    filename=file.filename,
                    path=file.path,
                    owner=file.owner,
                    desc=file.desc,
                    number_of_pages=file.number_of_pages
                )
            )

        return result

    async def post_file(self, file: FileBO) -> FileBO:
        new_file = await FileDB.create(
            filename=file.filename,
            path=file.path,
            owner=file.owner,
            desc=file.desc,
            number_of_pages=file.number_of_pages
        )
        file.id = new_file.id
        return file

    async def get_file_by_id(self, file_id: int) -> FileBO:
        files = await FileDB.filter(**{'id': file_id})
        if len(files) == 0:
            raise NotFoundException

        file = files[0]
        return FileBO(
            id=file.id,
            filename=file.filename,
            path=file.path,
            owner=file.owner,
            desc=file.desc,
            number_of_pages=file.number_of_pages
        )

    async def update_file(self, file_id: int, data: FileBO):
        files = await FileDB.filter(**{'id': file_id})
        if len(files) == 0:
            raise NotFoundException

        file = files[0]
        file.filename = data.filename
        file.path = data.path
        file.owner = data.owner
        file.desc = data.desc
        file.number_of_pages = data.number_of_pages

        await file.save()

    async def delete_file(self, file_id: int, owner: int) -> str:
        files = await FileDB.filter(**{"id": file_id, "owner": owner})
        if len(files) == 0:
            raise NotFoundException

        file = files[0]

        if file.owner != owner:
            raise BadTokenException

        path = file.path
        await file.delete()

        return path
