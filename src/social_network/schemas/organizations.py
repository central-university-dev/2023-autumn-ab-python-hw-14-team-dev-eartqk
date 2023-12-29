from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.social_network.schemas.countries import CountrySchema


class UserOwnerSchema(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    avatar_path: str | None

    model_config = ConfigDict(from_attributes=True)


class OrganizationBaseSchema(BaseModel):
    name: str
    about: str | None


class OrganizationBaseResponseSchema(OrganizationBaseSchema):
    id: int
    created_at: datetime
    avatar_path: str | None

    model_config = ConfigDict(from_attributes=True)


class OrganizationDetailsSchema(BaseModel):
    count_followers: int | None

    model_config = ConfigDict(from_attributes=True)


class OrganizationResponseSchema(OrganizationBaseResponseSchema):
    owner: UserOwnerSchema

    country: CountrySchema | None

    details: OrganizationDetailsSchema | None = None


class OrganizationPostSchema(BaseModel):
    id: int
    name: str
    avatar_path: str | None

    model_config = ConfigDict(from_attributes=True)


class CreateOrganizationSchema(OrganizationBaseSchema):
    pass


class UpdateOrganizationSchema(OrganizationBaseSchema):
    pass


class OrganizationAvatarResponse(BaseModel):
    avatar_path: str

    model_config = ConfigDict(from_attributes=True)
