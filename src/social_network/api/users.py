from fastapi import APIRouter, Depends, status
from fastapi.openapi.models import Response

from src.social_network.schemas.auth import UserAuthSchema
from src.social_network.schemas.users import UpdateUserSchema, UserResponseSchema, UserShortResponseSchema
from src.social_network.services.auth import get_current_user_from_cookies
from src.social_network.services.users import UsersService

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/', response_model=list[UserShortResponseSchema])
def get_users(
    skip: int = 0,
    limit: int = 30,
    service: UsersService = Depends(),
):
    return service.get_users(skip, limit)


@router.get('/{user_id}', response_model=UserResponseSchema)
def get_user(
    user_id: int,
    service: UsersService = Depends(),
):
    return service.get_user_with_details(user_id)


@router.put('/', response_model=UserResponseSchema)
def update_user(
    user_data: UpdateUserSchema,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: UsersService = Depends(),
):
    return service.update_user(user.id, user_data)


@router.delete('/', response_model=Response)
def delete_user(
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: UsersService = Depends(),
):
    service.make_inactive(user.id)
    return Response(status=status.HTTP_204_NO_CONTENT, description='The user inactive')
