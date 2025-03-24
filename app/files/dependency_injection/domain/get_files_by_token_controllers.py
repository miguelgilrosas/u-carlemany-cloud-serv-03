from dependency_injector import containers, providers

from app.files.domain.controllers.get_files_by_token_controller import GetFilesByTokenController
from app.files.dependency_injection.persistences.file_bo_persistences import FileBOPersistences


class GetFilesByTokenControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        GetFilesByTokenController,
        file_persistence_service=FileBOPersistences.carlemany()
    )
