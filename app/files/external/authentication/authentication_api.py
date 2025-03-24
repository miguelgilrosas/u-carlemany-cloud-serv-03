import aiohttp
import json

from app.files.domain.persistences.exceptions import BadTokenException

authentication_url = '0.0.0.0'


class AuthenticationApi:
    async def introspect(self, auth: str):
        headers = {
            "accept": "application/json",
            "auth": auth
        }
        url = "http://" + authentication_url + ":80/auth/introspect"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=False) as response:
                status_code = response.status
                if status_code != 200:
                    return None

                body = await response.text()
                return body

    async def auth_check(self, auth: str):
        auth_response = await self.introspect(auth=auth)
        if auth_response is None:
            raise BadTokenException

        return json.loads(auth_response)
