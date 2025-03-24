from pypdf import PdfMerger

from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistences.exceptions import BadTokenException, NotFoundException
from app.files.domain.persistences.file_bo_interface import FileBOInterface
from app.files.external.authentication.authentication_api import AuthenticationApi


class MergeFilesController:
    def __init__(self, file_persistence_service: FileBOInterface):
        self.file_persistence_service = file_persistence_service

    async def __call__(self, file_id1: int, file_id2: int, token: str) -> FileBO:
        auth_api = AuthenticationApi()
        try:
            user = await auth_api.auth_check(auth=token)

        except BadTokenException:
            raise BadTokenException

        try:
            file1 = await self.file_persistence_service.get_file_by_id(file_id=file_id1)
            file2 = await self.file_persistence_service.get_file_by_id(file_id=file_id2)

        except NotFoundException:
            raise NotFoundException

        user_id = user['id']
        if user_id != file1.owner or user_id != file2.owner:
            raise BadTokenException

        new_file = FileBO(
            filename='Merged.pdf',
            path='',
            owner=user_id,
            desc='Merged file created from "' + file1.path + '" and "' + file2.path + '"',
            number_of_pages=file1.number_of_pages + file2.number_of_pages
        )
        print('HOLA1')
        new_file = await self.file_persistence_service.post_file(new_file)
        print('HOLA2')
        new_file.path = "files/" + str(new_file.id) + ".pdf"
        await self.file_persistence_service.update_file(file_id=new_file.id, data=new_file)

        print('HOLA3')
        merged = new_file.path
        pdfs = [file1.path, file2.path]
        merger = PdfMerger()

        for pdf in pdfs:
            merger.append(pdf)

        name = merged
        merger.write(name)
        merger.close()

        return new_file.id
