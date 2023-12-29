from fastapi import APIRouter, Depends, status

from src.social_network.schemas.auth import UserAuthSchema
from src.social_network.schemas.comments import CommentResponseSchema, CreateCommentSchema, UpdateCommentSchema
from src.social_network.services.auth import get_current_user_from_cookies
from src.social_network.services.comments import CommentsService

router = APIRouter(
    prefix='/comments',
    tags=['comments'],
)


@router.get('/{comment_id}')
def get_comment(comment_id: int, service: CommentsService = Depends()) -> CommentResponseSchema:
    comment = service.get(comment_id)
    return CommentResponseSchema.model_validate(comment)


@router.post('/post/{post_id}')
def create_comment_on_post(
    post_id: int,
    comment_data: CreateCommentSchema,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: CommentsService = Depends(),
) -> CommentResponseSchema:
    comment = service.create_comment(user.id, post_id, comment_data)
    return CommentResponseSchema.model_validate(comment)


@router.put('/{comment_id}')
def update_comment(
    comment_id: int,
    comment_data: UpdateCommentSchema,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: CommentsService = Depends(),
) -> CommentResponseSchema:
    comment = service.update_comment(user.id, comment_id, comment_data)
    return CommentResponseSchema.model_validate(comment)


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    user: UserAuthSchema = Depends(get_current_user_from_cookies),
    service: CommentsService = Depends(),
):
    return service.delete_comment(user.id, comment_id)
