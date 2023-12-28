from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator


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


class UserShortResponseSchema(UserBaseSchema):
    id: int
    avatar_path: str | None

    model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(UserBaseSchema):
    id: int

    about: str | None
    birthday: date | None
    avatar_path: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator('birthday')
    def validate_birthday(self, v):
        if v and not date(year=1900, month=1, day=1) <= v <= date.today():
            raise ValueError('Birthday must be correct')
        return v
