from dependency_injector import containers, providers

from app.files.domain.controllers.get_file_controller import GetFileController
from app.files.dependency_injection.persistences.file_bo_persistences import FileBOPersistences


class GetFileControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        GetFileController,
        file_persistence_service=FileBOPersistences.carlemany()
    )