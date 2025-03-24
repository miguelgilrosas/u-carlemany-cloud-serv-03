from abc import ABC, abstractmethod

from app.files.domain.bo.file_bo import FileBO


class FileBOInterface(ABC):
    @abstractmethod
    def get_files_by_owner_id(self, owner_id) -> list[FileBO]:
        pass

    def post_file(self, data: FileBO) -> FileBO:
        pass

    def get_file_by_id(self, file_id: int) -> FileBO:
        pass

    def update_file(self, file_id: int, data: FileBO):
        pass

    def delete_file(self, file_id: int, owner: int) -> str:
        pass
