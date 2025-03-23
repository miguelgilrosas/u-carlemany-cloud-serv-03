from typing import Optional

from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistences.exceptions import UsernameAlreadyTakenException
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface


class UserBOMemoryPersistenceService(UserBOInterface):
    def __init__(self):
        self.users = {}
        self.new_user_id = 0

    def is_username_taken(self, username: str) -> bool:
        for user_id, user in self.users.items():
            if user.username == username:
                return True
        return False

    def create_user(self, user: UserBO):
        if self.is_username_taken(user.username):
            raise UsernameAlreadyTakenException

        user.id = self.new_user_id
        self.users[self.new_user_id] = user
        self.new_user_id += 1
        print(self.users)

    def get_user_by_username(self, username: str) -> Optional[UserBO]:
        for _, user in self.users.items():
            if user.username == username:
                return user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[UserBO]:
        if user_id not in self.users:
            return None

        return self.users[user_id]
