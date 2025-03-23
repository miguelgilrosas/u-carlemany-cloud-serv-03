from hashlib import sha256

from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistences.exceptions import UsernameAlreadyTakenException
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface


class RegisterController:
    def __init__(self, user_persistence_service: UserBOInterface):
        self.user_persistence_service = user_persistence_service

    def __call__(self, username: str, password: str, mail: str, year_of_birth: int) -> UserBO:
        to_hash = username + password
        hashed_password = sha256(to_hash.encode()).digest()

        new_user = UserBO(
            username=username,
            password=hashed_password,
            mail=mail,
            year_of_birth=year_of_birth
        )

        try:
            self.user_persistence_service.create_user(user=new_user)
        except UsernameAlreadyTakenException:
            raise UsernameAlreadyTakenException

        return new_user
