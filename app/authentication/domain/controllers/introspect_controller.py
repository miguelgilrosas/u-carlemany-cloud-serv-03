from typing import Optional

from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface


class IntrospectController:
    def __init__(self, user_persistence_service: UserBOInterface):
        self.user_persistence_service = user_persistence_service

    def __call__(self, token: str) -> Optional[UserBO]:
        user_id = self.user_persistence_service.get_user_id_by_token(token=token)
        if user_id is None:
            return None

        return self.user_persistence_service.get_user_by_id(user_id=user_id)
