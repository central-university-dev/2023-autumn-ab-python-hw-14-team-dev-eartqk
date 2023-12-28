from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator

from src.social_network.schemas.countries import CountrySchema


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

    details: UserDetailsSchema | None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('birthday')
    def validate_birthday(cls, v):
        if v and not date(year=1900, month=1, day=1) <= v <= date.today():
            raise ValueError('Birthday must be correct')
        return v
