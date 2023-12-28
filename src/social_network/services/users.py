from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from src.social_network.db import tables
from src.social_network.db.session import Session, get_session


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

    def get(self, user_id: int) -> tables.User:
        return self._get(user_id)
