import uuid
from typing import Optional
from tortoise.exceptions import DoesNotExist

from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistences.exceptions import UsernameAlreadyTakenException, BadTokenException
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface
from app.authentication.models import UserDB, TokenDB


class UserBOPostgresPersistenceService(UserBOInterface):
    async def create_user(self, user: UserBO):
        users = await UserDB.filter(**{"username": user.username})
        if len(users) > 0:
            raise UsernameAlreadyTakenException

        new_user = await UserDB.create(
            username=user.username,
            password=user.password,
            mail=user.mail,
            year_of_birth=user.year_of_birth
        )

        user.id = new_user.id

    async def get_user_by_username(self, username: str) -> Optional[UserBO]:
        try:
            user = await UserDB.get(username=username)

        except DoesNotExist:
            return None

        return UserBO(
            id=user.id,
            username=user.username,
            password=user.password,
            mail=user.mail,
            year_of_birth=user.year_of_birth
        )

    async def get_user_by_id(self, user_id: int) -> Optional[UserBO]:
        try:
            user = await UserDB.get(id=int(user_id))

        except DoesNotExist:
            return None

        return UserBO(
            id=user.id,
            username=user.username,
            password=user.password,
            mail=user.mail,
            year_of_birth=user.year_of_birth
        )

    async def create_token(self, user_id: int) -> str:
        token = str(uuid.uuid4())
        token_db = await TokenDB.filter(**{'token': token})
        while len(token_db) > 0:
            token = str(uuid.uuid4())
            token_db = await TokenDB.filter(**{'token': token})

        await TokenDB.create(token=token, user_id=user_id)

        return token

    async def get_user_id_by_token(self, token: str) -> Optional[int]:
        db_result = await TokenDB.filter(**{"token": token})
        if len(db_result) == 0:
            return None

        return db_result[0].user_id

    async def delete_token(self, token: str):
        db_result = await TokenDB.filter(**{"token": token})
        if len(db_result) == 0:
            raise BadTokenException

        await db_result[0].delete()
