from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.social_network.schemas.users import UserShortResponseSchema


class CommentBaseSchema(BaseModel):
    body: str


class CreateCommentSchema(CommentBaseSchema):
    pass


class UpdateCommentSchema(CommentBaseSchema):
    pass


class CommentResponseSchema(CommentBaseSchema):
    id: int
    user: UserShortResponseSchema
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
