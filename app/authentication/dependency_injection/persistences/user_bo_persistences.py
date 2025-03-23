from dependency_injector import containers, providers

from app.authentication.persistence.memory.user_bo import UserBOMemoryPersistenceService


class UserBOPersistences(containers.DeclarativeContainer):
    memory = providers.Singleton(UserBOMemoryPersistenceService)
    carlemany = memory
