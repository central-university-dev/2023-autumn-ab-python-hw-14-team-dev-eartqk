from datetime import datetime

from pydantic import BaseModel

from src.social_network.schemas.organizations import OrganizationPostSchema
from src.social_network.schemas.users import UserPostSchema


class PostBaseSchema(BaseModel):
    body: str


class CreatePostSchema(PostBaseSchema):
    pass


class UpdatePostSchema(PostBaseSchema):
    pass


class AttachmentResponseSchema(BaseModel):
    post_id: int
    path: str

    class Config:
        orm_mode = True


class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None

    user: UserPostSchema
    organization: OrganizationPostSchema | None
    attachments: list[AttachmentResponseSchema] | None

    class Config:
        orm_mode = True
