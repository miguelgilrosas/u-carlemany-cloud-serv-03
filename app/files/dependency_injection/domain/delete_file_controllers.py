from dependency_injector import containers, providers

from app.files.domain.controllers.delete_file_controller import DeleteFileController
from app.files.dependency_injection.persistences.file_bo_persistences import FileBOPersistences


class DeleteFileControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        DeleteFileController,
        file_persistence_service=FileBOPersistences.carlemany()
    )
