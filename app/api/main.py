from fastapi import APIRouter
from .routes import users
# from .routes.personal import income_personal


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(income_personal.router, prefix="/income/personal", tags=["income_personal"])
