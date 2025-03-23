from typing import Optional

from app.authentication.domain.persistences.user_bo_interface import UserBOInterface


class IntrospectController:
    def __init__(self, user_persistence_service: UserBOInterface):
        self.user_persistence_service = user_persistence_service

    async def __call__(self, token: str) -> Optional[dict[str, str]]:
        print(token)
        user_id = await self.user_persistence_service.get_user_id_by_token(token)
        print('user_id: '+str(user_id))
        if user_id is None:
            return None

        return await self.user_persistence_service.get_user_by_id(user_id=user_id)
