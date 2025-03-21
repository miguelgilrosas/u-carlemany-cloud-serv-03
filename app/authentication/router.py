import uuid
from hashlib import sha256
from fastapi import APIRouter, Body, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

users = {}
new_user_id = 0
tokens = {}


class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: bytes
    mail: str
    year_of_birth: int


class RegisterInput(BaseModel):
    username: str
    password: str
    mail: str
    year_of_birth: int


class RegisterOutput(BaseModel):
    id: int
    username: str
    mail: str
    year_of_birth: int


@router.post("/register")
async def auth_register(register_input: RegisterInput = Body()) -> dict[str, RegisterOutput]:
    global new_user_id

    if is_username_taken(register_input.username):
        raise HTTPException(status_code=409, detail="This username is already taken")

    to_hash = register_input.username + register_input.password
    hashed_password = sha256(to_hash.encode()).digest()

    users[new_user_id] = User(
        id=new_user_id,
        username=register_input.username,
        password=hashed_password,
        mail=register_input.mail,
        year_of_birth=register_input.year_of_birth,
    )

    output = RegisterOutput(
        id=new_user_id,
        username=register_input.username,
        mail=register_input.mail,
        year_of_birth=register_input.year_of_birth,
    )

    new_user_id += 1

    return {"new_user": output}


def is_username_taken(username: str) -> bool:
    for user_id, user in users.items():
        if user.username == username:
            return True
    return False


class LoginInput(BaseModel):
    username: str
    password: str


@router.post("/login")
async def auth_login(login_input: LoginInput = Body()) -> dict[str, str]:
    user = get_user_by_username(login_input.username)
    if not user:
        raise HTTPException(status_code=404, detail='Username not found')

    to_hash = login_input.username + login_input.password
    hashed_password = sha256(to_hash.encode()).digest()
    hashed_stored_password = user.password

    if hashed_password == hashed_stored_password:
        token = str(uuid.uuid4())
        while token in tokens:
            token = str(uuid.uuid4())

        tokens[token] = user.id

        return {"auth": token}

    else:
        raise HTTPException(status_code=403, detail='Password is not correct')


def get_user_by_username(username: str) -> Optional[User]:
    for user_id, user in users.items():
        if user.username == username:
            return user
    return None


class IntrospectOutput(BaseModel):
    id: int
    username: str
    mail: str
    year_of_birth: int


@router.get("/introspect")
async def auth_introspect(auth: str = Header()) -> IntrospectOutput:
    if auth not in tokens:
        raise HTTPException(status_code=403, detail='Forbidden')

    user = users[tokens[auth]]

    return IntrospectOutput(
        id=user.id,
        username=user.username,
        mail=user.mail,
        year_of_birth=user.year_of_birth,
    )


@router.post("/logout")
async def auth_logout(auth: str = Header()) -> dict[str, str]:
    if auth not in tokens:
        raise HTTPException(status_code=403, detail='Forbidden')

    del tokens[auth]
    return {'status': 'ok'}
