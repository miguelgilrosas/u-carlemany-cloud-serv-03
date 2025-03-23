from app.authentication.domain.persistences.exceptions import BadTokenException
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface


class LogoutController:
    def __init__(self, user_persistence_service: UserBOInterface):
        self.user_persistence_service = user_persistence_service

    def __call__(self, token: str):
        try:
            self.user_persistence_service.delete_token(token=token)

        except BadTokenException:
            raise BadTokenException
