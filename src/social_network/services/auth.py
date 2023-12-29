from datetime import datetime, timedelta

import bcrypt
from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from src.social_network.db import tables
from src.social_network.db.session import Session, get_session
from src.social_network.schemas.auth import CreateUserAuthSchema, Token, UserAuthSchema
from src.social_network.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserAuthSchema:
    return AuthService.validate_token(token)


def get_current_user_from_cookies(access_token: str | None = Cookie(None)) -> UserAuthSchema:
    return AuthService.validate_token(access_token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))  # type: ignore

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # type: ignore

    @classmethod
    def validate_token(cls, token: str | None) -> UserAuthSchema:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer',
            },
        )

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except (JWTError, AttributeError):
            raise exception from None

        user_data = payload.get('user')

        try:
            user = UserAuthSchema.model_validate(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = UserAuthSchema.model_validate(user)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.model_dump(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: CreateUserAuthSchema) -> Token:
        user = tables.User(  # type: ignore[call-arg]
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
            name=user_data.name,
            surname=user_data.surname,
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={
                'WWW-Authenticate': 'Bearer',
            },
        )

        user = self.session.query(tables.User).filter(tables.User.username == username).first()

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        user.is_active = True
        self.session.commit()

        return self.create_token(user)
