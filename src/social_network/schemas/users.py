from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from src.social_network.schemas.countries import CountrySchema
from src.social_network.schemas.organizations import OrganizationBaseResponseSchema


class UserBaseSchema(BaseModel):
    email: str
    username: str
    name: str
    surname: str


class UpdateUserSchema(BaseModel):
    name: str
    surname: str
    about: str | None
    birthday: date | None
    avatar_path: str | None

    model_config = ConfigDict(from_attributes=True)


class UserDetailsSchema(BaseModel):
    count_posts: int | None
    count_followers: int | None
    count_following_users: int | None
    count_following_organizations: int | None

    model_config = ConfigDict(from_attributes=True)


class UserShortResponseSchema(UserBaseSchema):
    id: int
    avatar_path: str | None

    model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(UserBaseSchema):
    id: int

    about: str | None
    birthday: date | None
    avatar_path: str | None
    country: CountrySchema | None = None
    created_at: datetime
    owned_organizations: list[OrganizationBaseResponseSchema] | None

    details: UserDetailsSchema | None = None

    model_config = ConfigDict(from_attributes=True)


class UserAvatarResponse(BaseModel):
    avatar_path: str

    model_config = ConfigDict(from_attributes=True)


class UserPostSchema(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    avatar_path: str | None

    model_config = ConfigDict(from_attributes=True)


class UserOwnerSchema(UserPostSchema):
    pass
