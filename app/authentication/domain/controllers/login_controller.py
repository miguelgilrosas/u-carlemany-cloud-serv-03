from hashlib import sha256

from app.authentication.domain.persistences.exceptions import WrongPasswordException, UsernameNotFoundException
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface


class LoginController:
    def __init__(self, user_persistence_service: UserBOInterface):
        self.user_persistence_service = user_persistence_service

    def __call__(self, username: str, password: str) -> str:
        user = self.user_persistence_service.get_user_by_username(username=username)
        if not user:
            raise UsernameNotFoundException

        to_hash = username + password
        hashed_password = sha256(to_hash.encode()).digest()
        hashed_stored_password = user.password

        if hashed_password == hashed_stored_password:
            token = self.user_persistence_service.create_token(user_id=user.id)

            return token

        else:
            raise WrongPasswordException()
