from typing import Optional
import uuid

from app.authentication.domain.persistences.exceptions import BadTokenException
from app.authentication.domain.persistences.token_interface import TokenInterface


class TokenMemoryPersistenceService(TokenInterface):
    def __init__(self):
        self.tokens = {}

    def create_token(self, user_id: int) -> str:
        token = str(uuid.uuid4())
        while token in self.tokens:
            token = str(uuid.uuid4())

        self.tokens[token] = user_id

        print(self.tokens)
        return token

    def get_user_id_by_token(self, token: str) -> Optional[int]:
        if token not in self.tokens:
            return None

        return self.tokens[token]

    def delete_token(self, token: str):
        if token not in self.tokens:
            raise BadTokenException

        del self.tokens[token]
