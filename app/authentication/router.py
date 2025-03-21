import uuid
from hashlib import sha256
from fastapi import APIRouter, Body, HTTPException, Header
from pydantic import BaseModel

router = APIRouter()

users = {}
tokens = {}


class User(BaseModel):
    username: str
    password: bytes
    mail: str
    age_of_birth: int


class RegisterInput(BaseModel):
    username: str
    password: str
    mail: str
    age_of_birth: int


class RegisterOutput(BaseModel):
    username: str
    mail: str
    age_of_birth: int


@router.post("/register")
async def auth_register(input: RegisterInput = Body()) -> dict[str, RegisterOutput]:
    if input.username in users:
        raise HTTPException(status_code=409, detail="This username is already taken")

    to_hash = input.username + input.password
    hashed_password = sha256(to_hash.encode()).digest()

    new_user = User(
        username=input.username,
        password=hashed_password,
        mail=input.mail,
        age_of_birth=input.age_of_birth,
    )

    users[input.username] = new_user

    output = RegisterOutput(
        username=input.username,
        mail=input.mail,
        age_of_birth=input.age_of_birth,
    )

    return {"new_user": output}


class LoginInput(BaseModel):
    username: str
    password: str


@router.post("/login")
async def auth_login(input: LoginInput = Body()) -> dict[str, str]:
    if input.username not in users:
        raise HTTPException(status_code=404, detail='Username not found')

    to_hash = input.username + input.password
    hashed_password = sha256(to_hash.encode()).digest()
    hashed_stored_password = users[input.username].password

    if hashed_password == hashed_stored_password:
        random_id = str(uuid.uuid4())
        while random_id in tokens:
            random_id = str(uuid.uuid4())

        tokens[random_id] = input.username

        return {"auth": random_id}

    else:
        raise HTTPException(status_code=403, detail='Password is not correct')


class IntrospectOutput(BaseModel):
    username: str
    mail: str
    age_of_birth: int


@router.get("/introspect")
async def auth_introspect(auth: str = Header()) -> IntrospectOutput:
    if auth not in tokens:
        raise HTTPException(status_code=403, detail='Forbidden')

    username = tokens[auth]
    user = users[username]

    return IntrospectOutput(
        username=user.username,
        mail=user.mail,
        age_of_birth=user.age_of_birth,
    )


@router.post("/logout")
async def auth_logout(auth: str = Header()) -> dict[str, str]:
    if auth not in tokens:
        raise HTTPException(status_code=403, detail='Forbidden')

    del tokens[auth]
    return {'status': 'ok'}
