from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, Response

from src.social_network.schemas.auth import (
    Token, UserAuthSchema,
    CreateUserAuthSchema,
)
from src.social_network.schemas.users import UserResponseSchema
from src.social_network.services.auth import AuthService, get_current_user_from_cookies
from src.social_network.services.users import UsersService

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/sign-up', response_model=Token)
def sign_up(
        user_data: CreateUserAuthSchema,
        service: AuthService = Depends(),
):
    token_data = service.register_new_user(user_data)
    response = JSONResponse(content=token_data.dict())
    response.set_cookie(
        key='access_token',
        value=token_data.access_token,
        secure=True,
        httponly=True,
        samesite='none',
    )
    return response


@router.post('/sign-in', response_model=Token)
def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    token_data = service.authenticate_user(
        form_data.username,
        form_data.password,
    )
    response = JSONResponse(content=token_data.dict())
    response.set_cookie(
        key='access_token',
        value=token_data.access_token,
        secure=True,
        httponly=True,
        samesite='none',
    )
    return response


@router.post('/logout')
def logout():
    response = Response()
    response.delete_cookie('access_token')
    return response


@router.get('/user', response_model=UserResponseSchema)
def get_user(
        user: UserAuthSchema = Depends(get_current_user_from_cookies),
        service: UsersService = Depends(),
):
    pass
