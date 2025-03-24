from dependency_injector import containers, providers
from app.files.persistence.postgres.file_bo import FileBOPostgresPersistenceService


class FileBOPersistences(containers.DeclarativeContainer):
    postgres = providers.Singleton(FileBOPostgresPersistenceService)
    carlemany = postgres
