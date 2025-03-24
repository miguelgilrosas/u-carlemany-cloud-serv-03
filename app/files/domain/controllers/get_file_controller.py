from fastapi.responses import FileResponse

from app.files.domain.persistences.file_bo_interface import FileBOInterface
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistences.exceptions import BadTokenException, NotFoundException
from app.files.external.authentication.authentication_api import AuthenticationApi


class GetFileController:
    def __init__(self, file_persistence_service: FileBOInterface):
        self.file_persistence_service = file_persistence_service

    async def __call__(self, file_id: int, token: str) -> FileBO:
        auth_api = AuthenticationApi()
        try:
            user = await auth_api.auth_check(auth=token)

        except BadTokenException:
            raise BadTokenException

        try:
            file = await self.file_persistence_service.get_file_by_id(file_id=file_id)

        except NotFoundException:
            raise NotFoundException

        if user['id'] != file.id:
            raise BadTokenException

        return file
