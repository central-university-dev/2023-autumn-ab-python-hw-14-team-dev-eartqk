from fastapi import Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import joinedload

from src.social_network.db import tables
from src.social_network.db.session import Session, get_session
from src.social_network.schemas.organizations import (
    CreateOrganizationSchema,
    OrganizationAvatarResponse,
    OrganizationDetailsSchema,
    OrganizationResponseSchema,
    UpdateOrganizationSchema,
)
from src.social_network.services.minio.uploads import UploadsService
from src.social_network.services.users import UsersService


class OrganizationsService:
    def __init__(
        self,
        uploads_service: UploadsService = Depends(),
        users_service: UsersService = Depends(),
        session: Session = Depends(get_session),
    ):
        self.uploads_service = uploads_service
        self.users_service = users_service
        self.session = session

    def _get(self, org_id: int) -> tables.Organization:
        org = self.session.query(tables.Organization).filter_by(id=org_id).first()
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Organization not found.')
        return org

    def _get_org_details(self, org_id) -> OrganizationDetailsSchema:
        count_followers = self.session.query(tables.follower_organization).filter_by(followed_org_id=org_id).count()
        return OrganizationDetailsSchema(count_followers=count_followers)

    def get(self, org_id: int) -> tables.Organization:
        return self._get(org_id)

    def get_with_details(self, org_id: int) -> OrganizationResponseSchema:
        org = self._get(org_id)
        details = self._get_org_details(org_id)
        response = OrganizationResponseSchema.model_validate(org)
        response.details = details
        return response

    def get_organizations(self, skip: int = 0, limit: int = 30) -> list[tables.Organization]:
        orgs = self.session.query(tables.Organization).offset(skip).limit(limit).all()
        return orgs

    def get_org_posts(self, org_id: int, skip: int = 0, limit: int = 30) -> list[tables.Post]:
        posts = (
            self.session.query(tables.Post)
            .options(joinedload(tables.Post.organization))
            .options(joinedload(tables.Post.user))
            .options(joinedload(tables.Post.comments))
            .filter_by(organization_id=org_id)
            .order_by(tables.Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return posts

    def get_org_followers(self, org_id: int) -> list[tables.User] | None:
        org = (
            self.session.query(tables.Organization)
            .options(joinedload(tables.Organization.followers))
            .filter_by(id=org_id)
            .first()
        )
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Organization not found.')
        return org.followers

    def create_organization(self, user_id: int, org_data: CreateOrganizationSchema) -> tables.Organization:
        org = tables.Organization(
            owner_id=user_id,  # type: ignore
            **org_data.model_dump(),
        )
        self.session.add(org)
        self.session.commit()
        return org

    @staticmethod
    def _check_permission(user: tables.User, org: tables.Organization) -> None:
        if org.owner_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You don have permission')

    def update_organization(self, user_id: int, org_id: int, org_data: UpdateOrganizationSchema) -> tables.Organization:
        user = self.users_service.get(user_id)
        org = self._get(org_id)
        self._check_permission(user, org)
        for field, value in org_data:
            setattr(org, field, value)
        self.session.commit()
        return org

    def upload_avatar(
        self,
        user_id: int,
        org_id: int,
        file: UploadFile = File(...),
    ) -> OrganizationAvatarResponse:
        user = self.users_service.get(user_id)
        org = self._get(org_id)
        self._check_permission(user, org)
        file_path = self.uploads_service.upload_file(file, only_picture=True)
        org.avatar_path = file_path
        self.session.commit()
        return OrganizationAvatarResponse.model_validate(org)
