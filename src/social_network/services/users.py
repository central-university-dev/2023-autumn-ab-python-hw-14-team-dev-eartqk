from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from src.social_network.db import tables
from src.social_network.db.session import Session, get_session
from src.social_network.schemas.users import UpdateUserSchema, UserDetailsSchema, UserResponseSchema


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
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

    def update_user(self, user_id: int, user_data: UpdateUserSchema) -> tables.User:
        user = self._get(user_id)
        for field, value in user_data:
            setattr(user, field, value)
        self.session.commit()
        return user

    def make_inactive(self, user_id: int):
        user = self._get(user_id)
        user.is_active = False
        self.session.commit()

    def make_active(self, user_id: int):
        user = self._get(user_id, is_active=False)
        user.is_active = True
        self.session.commit()
