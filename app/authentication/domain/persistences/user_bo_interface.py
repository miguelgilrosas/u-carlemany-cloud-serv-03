from abc import ABC, abstractmethod
from typing import Optional

from app.authentication.domain.bo.user_bo import UserBO


class UserBOInterface(ABC):
    @abstractmethod
    def create_user(self, user: UserBO):
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[UserBO]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserBO]:
        pass

    @abstractmethod
    def create_token(self, user_id: int) -> str:
        pass

    @abstractmethod
    def get_user_id_by_token(self, token: str) -> Optional[int]:
        pass

    @abstractmethod
    def delete_token(self, token: str):
        pass
