from app.authentication.domain.persistences.exceptions import BadTokenException
from app.authentication.domain.persistences.token_interface import TokenInterface


class LogoutController:
    def __init__(self, token_persistence_service: TokenInterface):
        self.token_persistence_service = token_persistence_service

    def __call__(self, token: str):
        try:
            self.token_persistence_service.delete_token(token=token)

        except BadTokenException:
            raise BadTokenException
