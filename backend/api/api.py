from fastapi import APIRouter

from api.endpoints import users, login, expenses, menus

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
api_router.include_router(menus.router, prefix="/menus", tags=["menus"])
