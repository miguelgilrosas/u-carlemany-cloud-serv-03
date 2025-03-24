from dependency_injector import containers, providers

from app.files.domain.controllers.post_file_controller import PostFileController
from app.files.dependency_injection.persistences.file_bo_persistences import FileBOPersistences


class PostFileControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        PostFileController,
        file_persistence_service=FileBOPersistences.carlemany()
    )
