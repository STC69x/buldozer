from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.config.config import Config, ConfigSite
from app.modules.user.models import User
from app.dependencies import get_current_user
from app.handlers.auth_role_checker import auth_and_roles_required
from app.handlers.http_errors import noauth, noapi

router = APIRouter()
cfg = Config()
cfg_site = ConfigSite()
templates = Jinja2Templates(directory=cfg.TEMPLATE_PATH)
router = APIRouter(tags=["adminpanel"], prefix="/adminpanel")


##############################
#Панель управления/Admin Panel
##############################
@router.get("/")
def get_panel(request: Request, db: Session = Depends(get_db), 
              current_user: User = Depends(get_current_user),
              api: bool = False):
    if api:
        return noapi
    if auth_and_roles_required(current_user, ["administrator"]):
        return templates.TemplateResponse("adminpanel/main.html", 
                                          {
                                           "request": request,
                                           "user": current_user,
                                           "cfg": cfg_site
                                          }
                                         )
    if api:
        raise noauth
    return RedirectResponse("/user/login", status_code=status.HTTP_303_SEE_OTHER)
    
