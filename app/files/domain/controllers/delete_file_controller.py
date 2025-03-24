import os

from app.files.domain.persistences.exceptions import BadTokenException, NotFoundException
from app.files.domain.persistences.file_bo_interface import FileBOInterface
from app.files.external.authentication.authentication_api import AuthenticationApi


class DeleteFileController:
    def __init__(self, file_persistence_service: FileBOInterface):
        self.file_persistence_service = file_persistence_service

    async def __call__(self, file_id: int, token: str):
        auth_api = AuthenticationApi()
        try:
            user = await auth_api.auth_check(auth=token)

        except BadTokenException:
            raise BadTokenException

        try:
            path = await self.file_persistence_service.delete_file(file_id=file_id, owner=user['id'])

        except NotFoundException:
            raise NotFoundException

        except BadTokenException:
            raise BadTokenException

        if path != '':
            os.remove(path)
