from fastapi import APIRouter, Body, HTTPException, Header
from pydantic import BaseModel

from app.authentication.dependency_injection.domain.introspect_controllers import IntrospectControllers
from app.authentication.dependency_injection.domain.login_controllers import LoginControllers
from app.authentication.dependency_injection.domain.logout_controllers import LogoutControllers
from app.authentication.dependency_injection.domain.register_controllers import RegisterControllers
from app.authentication.domain.persistences.exceptions import UsernameAlreadyTakenException, WrongPasswordException, \
    UsernameNotFoundException, BadTokenException

router = APIRouter()


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
    if register_input.username == '' or register_input.password == '':
        raise HTTPException(status_code=400, detail='Username and password can not be empty')

    register_controller = RegisterControllers.carlemany()

    try:
        user = register_controller(
            username=register_input.username,
            password=register_input.password,
            mail=register_input.mail,
            year_of_birth=register_input.year_of_birth
        )

    except UsernameAlreadyTakenException:
        raise HTTPException(status_code=409, detail="This username is already taken")

    output = RegisterOutput(
        id=user.id,
        username=user.username,
        mail=user.mail,
        year_of_birth=user.year_of_birth
    )

    return {"new_user": output}


class LoginInput(BaseModel):
    username: str
    password: str


@router.post("/login")
async def auth_login(login_input: LoginInput = Body()) -> dict[str, str]:
    if login_input.username == '' or login_input.password == '':
        raise HTTPException(status_code=400, detail='Username and password can not be empty')

    login_controller = LoginControllers.carlemany()

    try:
        token = login_controller(username=login_input.username, password=login_input.password)

    except UsernameNotFoundException:
        raise HTTPException(status_code=404, detail='Username not found')

    except WrongPasswordException:
        raise HTTPException(status_code=403, detail='Password is not correct')

    return {'auth': token}


class IntrospectOutput(BaseModel):
    id: int
    username: str
    mail: str
    year_of_birth: int


@router.get("/introspect")
async def auth_introspect(auth: str = Header()) -> IntrospectOutput:
    introspect_controller = IntrospectControllers.carlemany()

    user = introspect_controller(token=auth)
    if user is None:
        raise HTTPException(status_code=403, detail='Forbidden')

    return IntrospectOutput(
        id=user.id,
        username=user.username,
        mail=user.mail,
        year_of_birth=user.year_of_birth,
    )


@router.post("/logout")
async def auth_logout(auth: str = Header()) -> dict[str, str]:
    logout_controller = LogoutControllers.carlemany()

    try:
        logout_controller(token=auth)

    except BadTokenException:
        raise HTTPException(status_code=403, detail='Forbidden')

    return {'status': 'ok'}
