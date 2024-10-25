from fastapi import (FastAPI, 
                     Request, 
                     Form, 
                     status, 
                     HTTPException, 
                     APIRouter,
                     Depends)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated, Optional
from datetime import datetime, timedelta

from app.config.config import Config
from app.config.database import AsyncSession
from app.dependencies import get_db
from app.handlers.create_jwt import create_access_token
from .schemas import UserLogin 
from .auth import get_user, verify_password

router = APIRouter()
cfg = Config()
templates = Jinja2Templates(directory=cfg.TEMPLATE_PATH)
router = APIRouter(tags=["user"], prefix="/user")


#####################
#Авторизация
####################
@router.get("/login")
async def login_form(request: Request,
                     message: Optional[str] = None):
    return templates.TemplateResponse("login_form.html", 
                                      {
                                          "request": request,
                                          "message": message
                                      }
                                  )

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                api: bool = False,
                db: AsyncSession = Depends(get_db)):
    user = await get_user(form_data.username, db)

    if not user:
        if api:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Incorrect username")
        return RedirectResponse("/user/login?message=nok_user", 
                                status_code=status.HTTP_303_SEE_OTHER)

    if not verify_password(form_data.password, user.hashed_password):
        if api:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Incorrect password")
        
        return RedirectResponse("/user/login?message=nok_pswd", 
                                status_code=status.HTTP_303_SEE_OTHER)

    if not user.is_active or not user.is_validate:
        if api:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Username Deactivated or not Activated")
        return RedirectResponse("/user/login?message=nok_active", 
                                status_code=status.HTTP_303_SEE_OTHER)
    # Create JWT
    access_token_expires = timedelta(minutes=cfg.TOKEN_LIFE)
    access_token = create_access_token(data={"sub": user.username}, 
                                       expires_delta=access_token_expires)
    if api:
        return access_token
    # Set cookie (optional: could also be sent in the response header)

    response = RedirectResponse("/", 
                                status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response
