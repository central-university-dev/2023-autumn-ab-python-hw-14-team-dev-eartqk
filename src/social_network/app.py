from fastapi import APIRouter, FastAPI

from src.social_network.api.auth import router as auth_router
from src.social_network.api.countries import router as countries_router
from src.social_network.api.organizations import router as organizations_router
from src.social_network.api.users import router as users_router

app = FastAPI(
    title='HW14 Social Network',
    description='Backend-API for homework 14 AB',
    version='1.0.0',
)

api_router = APIRouter(prefix='')

api_router.include_router(auth_router)
api_router.include_router(countries_router)
api_router.include_router(users_router)
api_router.include_router(organizations_router)

app.include_router(api_router)
