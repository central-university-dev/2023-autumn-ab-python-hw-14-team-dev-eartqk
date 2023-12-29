from fastapi import APIRouter, Depends, status

from src.social_network.schemas.auth import UserAuthSchema
from src.social_network.schemas.subscriptions import FollowOrganizationSchema, FollowUserResponseSchema
from src.social_network.services.auth import get_current_user_from_cookies
from src.social_network.services.subscriptions import SubscriptionsService

router = APIRouter(
    prefix='/follow',
    tags=['subscriptions'],
)


@router.get('/user/{user_id}', response_model=FollowUserResponseSchema)
def check_follow_user(
    user_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: SubscriptionsService = Depends(),
):
    is_follow = service.is_user_followed_user(follower_id=user.id, followed_id=user_id)
    return FollowUserResponseSchema(
        follower_user_id=user.id,
        followed_user_id=user_id,
        is_follow=is_follow,
    )


@router.post('/user/{user_id}', status_code=status.HTTP_200_OK)
def follow_user(
    user_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: SubscriptionsService = Depends(),
):
    service.follow_user(follower_id=user.id, followed_id=user_id)
    return FollowUserResponseSchema(
        follower_user_id=user.id,
        followed_user_id=user_id,
        is_follow=True,
    )


@router.delete('/user/{user_id}', status_code=status.HTTP_200_OK)
def unfollow_user(
    user_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: SubscriptionsService = Depends(),
):
    service.unfollow_user(follower_id=user.id, followed_id=user_id)
    return FollowUserResponseSchema(
        follower_user_id=user.id,
        followed_user_id=user_id,
        is_follow=False,
    )


@router.get('/organization/{org_id}', response_model=FollowOrganizationSchema)
def check_follow_organization(
    org_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: SubscriptionsService = Depends(),
):
    is_follow = service.is_user_followed_org(follower_id=user.id, followed_org_id=org_id)
    return FollowOrganizationSchema(
        follower_user_id=user.id,
        followed_org_id=org_id,
        is_follow=is_follow,
    )


@router.post('/organization/{org_id}', status_code=status.HTTP_200_OK)
def follow_organization(
    org_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: SubscriptionsService = Depends(),
):
    service.follow_org(follower_id=user.id, followed_org_id=org_id)
    return FollowOrganizationSchema(
        follower_user_id=user.id,
        followed_org_id=org_id,
        is_follow=True,
    )


@router.delete('/organization/{org_id}', status_code=status.HTTP_200_OK)
def unfollow_organization(
    org_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: SubscriptionsService = Depends(),
):
    service.unfollow_org(follower_id=user.id, followed_org_id=org_id)
    return FollowOrganizationSchema(
        follower_user_id=user.id,
        followed_org_id=org_id,
        is_follow=False,
    )
