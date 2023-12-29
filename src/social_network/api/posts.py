from fastapi import APIRouter, Depends, File, UploadFile, status

from src.social_network.schemas.auth import UserAuthSchema
from src.social_network.schemas.posts import CreatePostSchema, PostResponseSchema, UpdatePostSchema
from src.social_network.services.auth import get_current_user_from_cookies
from src.social_network.services.posts import PostsService

router = APIRouter(
    prefix='/posts',
    tags=['posts'],
)


@router.get('/{post_id}')
def get_post(
    post_id: int,
    posts_service: PostsService = Depends(),
) -> PostResponseSchema:
    post = posts_service.get(post_id)
    return PostResponseSchema.model_validate(post)


@router.post('/')
def create_post(
    post_data: CreatePostSchema,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    posts_service: PostsService = Depends(),
) -> PostResponseSchema:
    post = posts_service.create_post(
        user_id=user.id,
        org_id=None,
        post_data=post_data,
    )
    return PostResponseSchema.model_validate(post)


@router.post('/organization/{org_id}')
def create_post_by_organization(
    post_data: CreatePostSchema,
    org_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    posts_service: PostsService = Depends(),
) -> PostResponseSchema:
    post = posts_service.create_post(
        user_id=user.id,
        org_id=org_id,
        post_data=post_data,
    )
    return PostResponseSchema.model_validate(post)


@router.put('/{post_id}')
def update_post(
    post_id: int,
    post_data: UpdatePostSchema,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    posts_service: PostsService = Depends(),
) -> PostResponseSchema:
    post = posts_service.update_post(user.id, post_id, post_data)
    return PostResponseSchema.model_validate(post)


@router.put('/{post_id}/attachments')
def upload_attachments(
    post_id: int,
    files: list[UploadFile] = File(...),
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    posts_service: PostsService = Depends(),
) -> PostResponseSchema:
    post = posts_service.upload_attachments(user.id, post_id, files)
    return PostResponseSchema.model_validate(post)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    posts_service: PostsService = Depends(),
):
    posts_service.delete_post(user.id, post_id)
