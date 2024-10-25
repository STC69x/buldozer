from fastapi import APIRouter, Depends

from app.modules.pages import pages, admin as admin_pages
from app.modules.adminpanel import adminpanel
from app.modules.user import login
router = APIRouter()


def include_routes():
    router.include_router(adminpanel.router)
    router.include_router(admin_pages.router)
    router.include_router(login.router)
    router.include_router(pages.router)

include_routes()
