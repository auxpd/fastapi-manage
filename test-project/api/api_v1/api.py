from fastapi import APIRouter

from api.api_v1.endpoints import user

api_router = APIRouter()
# user
api_router.include_router(user.router, prefix='/user', tags=['user'])
