from app.files.domain.persistences.file_bo_interface import FileBOInterface
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistences.exceptions import BadTokenException
from app.files.external.authentication.authentication_api import AuthenticationApi


class GetFilesByTokenController:
    def __init__(self, file_persistence_service: FileBOInterface):
        self.file_persistence_service = file_persistence_service

    async def __call__(self, token: str) -> list[FileBO]:
        auth_api = AuthenticationApi()
        try:
            user = await auth_api.auth_check(auth=token)

        except BadTokenException:
            raise BadTokenException

        return await self.file_persistence_service.get_files_by_owner_id(owner_id=user['id'])
