from fastapi import Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import joinedload

from src.social_network.db import tables
from src.social_network.db.session import Session, get_session
from src.social_network.schemas.users import UpdateUserSchema, UserAvatarResponse, UserDetailsSchema, UserResponseSchema
from src.social_network.services.minio.uploads import UploadsService


class UsersService:
    def __init__(self, uploads_service: UploadsService = Depends(), session: Session = Depends(get_session)):
        self.uploads_service = uploads_service
        self.session = session

    def _get(self, user_id: int, is_active: bool = True) -> tables.User:
        user = (
            self.session.query(tables.User)
            .options(joinedload(tables.User.owned_organizations))
            .filter_by(
                id=user_id,
                is_active=is_active,
            )
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exists')
        return user

    def _get_user_details(self, user_id: int) -> UserDetailsSchema:
        count_posts = self.session.query(tables.Post).filter_by(user_id=user_id).count()
        count_followers = self.session.query(tables.follower_user).filter_by(followed_user_id=user_id).count()
        count_following_users = self.session.query(tables.follower_user).filter_by(follower_user_id=user_id).count()
        count_following_organizations = self.session.query(tables.Organization).filter_by(owner_id=user_id).count()

        return UserDetailsSchema(
            count_posts=count_posts,
            count_followers=count_followers,
            count_following_users=count_following_users,
            count_following_organizations=count_following_organizations,
        )

    def get(self, user_id: int) -> tables.User:
        return self._get(user_id)

    def get_user_with_details(self, user_id: int) -> UserResponseSchema:
        user = self._get(user_id)
        details = UserDetailsSchema.model_validate(self._get_user_details(user.id))
        response = UserResponseSchema.model_validate(user)
        response.details = details
        return response

    def get_users(self, skip: int = 0, limit: int = 30) -> list[tables.User]:
        users = self.session.query(tables.User).filter_by(is_active=True).offset(skip).limit(limit).all()
        return users

    def get_posts(self, user_id: int, skip: int = 0, limit: int = 30) -> list[tables.Post]:
        user = self._get(user_id)
        posts = (
            self.session.query(tables.Post)
            .filter_by(
                user_id=user.id,
                organization_id=None,
            )
            .order_by(tables.Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return posts

    def update_user(self, user_id: int, user_data: UpdateUserSchema) -> tables.User:
        user = self._get(user_id)
        for field, value in user_data:
            setattr(user, field, value)
        self.session.commit()
        return user

    def make_inactive(self, user_id: int) -> None:
        user = self._get(user_id)
        user.is_active = False
        self.session.commit()

    def make_active(self, user_id: int) -> None:
        user = self._get(user_id, is_active=False)
        user.is_active = True
        self.session.commit()

    def upload_avatar(
        self,
        user_id: int,
        file: UploadFile = File(...),
    ) -> UserAvatarResponse:
        user = self._get(user_id)
        file_path = self.uploads_service.upload_file(file, only_picture=True)
        user.avatar_path = file_path
        self.session.commit()
        return UserAvatarResponse.model_validate(user)

    def get_user_followers(self, user_id: int) -> list[tables.User]:
        user = (
            self.session.query(tables.User)
            .filter_by(
                id=user_id,
                is_active=True,
            )
            .options(joinedload(tables.User.followers))  # type: ignore
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exists')
        return user.followers  # type: ignore

    def get_user_followed_users(self, user_id: int) -> list[tables.User]:
        user = (
            self.session.query(tables.User)
            .filter_by(
                id=user_id,
                is_active=True,
            )
            .options(joinedload(tables.User.followed_users))
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exists')
        return user.followed_users

    def get_user_followed_organizations(self, user_id: int) -> list[tables.User]:
        user = (
            self.session.query(tables.User)
            .filter_by(
                id=user_id,
                is_active=True,
            )
            .options(joinedload(tables.User.followed_orgs))
            .first()
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exists')
        return user.followed_orgs
