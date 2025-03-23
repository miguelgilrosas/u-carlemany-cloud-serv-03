from dependency_injector import containers, providers

from app.authentication.dependency_injection.persistences.user_bo_persistences import UserBOPersistences
from app.authentication.domain.controllers.login_controller import LoginController


class LoginControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        LoginController,
        user_persistence_service=UserBOPersistences.carlemany()
    )
