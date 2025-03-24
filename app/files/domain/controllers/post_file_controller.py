from app.files.domain.persistences.file_bo_interface import FileBOInterface
from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistences.exceptions import BadTokenException
from app.files.external.authentication.authentication_api import AuthenticationApi


class PostFileController:
    def __init__(self, file_persistence_service: FileBOInterface):
        self.file_persistence_service = file_persistence_service

    async def __call__(self, file: FileBO, token: str) -> FileBO:
        auth_api = AuthenticationApi()
        try:
            user = await auth_api.auth_check(auth=token)

        except BadTokenException:
            raise BadTokenException

        file.owner = user['id']
        return await self.file_persistence_service.post_file(file)
