from pydantic import BaseModel, ConfigDict


class UserAuthBaseSchema(BaseModel):
    email: str
    username: str
    name: str
    surname: str


class CreateUserAuthSchema(UserAuthBaseSchema):
    password: str


class UserAuthSchema(UserAuthBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
