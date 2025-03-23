from dependency_injector import containers, providers

from app.authentication.dependency_injection.persistences.user_bo_persistences import UserBOPersistences
from app.authentication.domain.controllers.logout_controller import LogoutController


class LogoutControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        LogoutController,
        user_persistence_service=UserBOPersistences.carlemany()
    )
