from dependency_injector import containers, providers

from app.authentication.dependency_injection.persistences.user_bo_persistences import UserBOPersistences
from app.authentication.domain.controllers.introspect_controller import IntrospectController


class IntrospectControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        IntrospectController,
        user_persistence_service=UserBOPersistences.carlemany()
    )
