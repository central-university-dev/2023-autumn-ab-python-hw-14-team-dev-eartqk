from fastapi import APIRouter, Depends, File, UploadFile

from src.social_network.schemas.auth import UserAuthSchema
from src.social_network.schemas.organizations import (
    CreateOrganizationSchema,
    OrganizationAvatarResponse,
    OrganizationResponseSchema,
    UpdateOrganizationSchema,
)
from src.social_network.schemas.posts import PostResponseSchema
from src.social_network.schemas.users import UserShortResponseSchema
from src.social_network.services.auth import get_current_user_from_cookies
from src.social_network.services.organizations import OrganizationsService

router = APIRouter(
    prefix='/organizations',
    tags=['organizations'],
)


@router.get('', response_model=list[OrganizationResponseSchema])
def get_organizations(skip: int = 0, limit: int = 30, service: OrganizationsService = Depends()):
    return service.get_organizations(skip, limit)


@router.get('/{org_id}', response_model=OrganizationResponseSchema)
def get_organization(org_id: int, service: OrganizationsService = Depends()):
    return service.get_with_details(org_id)


@router.get('/{org_id}/posts', response_model=list[PostResponseSchema])
def get_organization_posts(org_id: int, skip: int = 0, limit: int = 30, service: OrganizationsService = Depends()):
    return service.get_org_posts(org_id, skip, limit)


@router.get('/{org_id}/followers', response_model=list[UserShortResponseSchema])
def get_organization_followers(org_id: int, service: OrganizationsService = Depends()):
    return service.get_org_followers(org_id)


@router.post('', response_model=OrganizationResponseSchema)
def create_organization(
    org_data: CreateOrganizationSchema,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: OrganizationsService = Depends(),
):
    return service.create_organization(user.id, org_data)


@router.put('/{org_id}', response_model=OrganizationResponseSchema)
def update_organization(
    org_id: int,
    org_data: UpdateOrganizationSchema,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: OrganizationsService = Depends(),
):
    return service.update_organization(user.id, org_id, org_data)


@router.put('/{org_id}/avatar', response_model=OrganizationAvatarResponse)
def upload_avatar(
    org_id: int,
    avatar_file: UploadFile = File(...),
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: OrganizationsService = Depends(),
):
    return service.upload_avatar(user.id, org_id, avatar_file)
