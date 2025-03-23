from abc import ABC, abstractmethod
from typing import Optional


class TokenInterface(ABC):
    @abstractmethod
    def create_token(self, user_id: int) -> str:
        pass

    @abstractmethod
    def get_user_id_by_token(self, token: str) -> Optional[int]:
        pass

    @abstractmethod
    def delete_token(self, token: str):
        pass
