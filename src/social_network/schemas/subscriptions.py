from pydantic import BaseModel


class FollowUserResponseSchema(BaseModel):
    follower_user_id: int
    followed_user_id: int
    is_follow: bool


class FollowOrganizationSchema(BaseModel):
    follower_user_id: int
    followed_org_id: int
    is_follow: bool
