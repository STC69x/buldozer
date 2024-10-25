from fastapi import Cookie, Depends, status, Request, HTTPException
from jwt.exceptions import InvalidTokenError

from fastapi.responses import RedirectResponse
from .config.database import AsyncSession, async_session
from .config.config import Config
from typing import Optional, List, Annotated
from app.modules.user.auth import get_user
from app.modules.user.models import User
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

cfg = Config()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login?api=true", auto_error=False)

    
async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


def get_token_from_cookie(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        return None
        #return RedirectResponse("user/login",  status_code=status.HTTP_303_SEE_OTHER)
    return token


async def get_current_user(token: str = Depends(oauth2_scheme),
                          db: AsyncSession = Depends(get_db),
                          token_cookie: str = Depends(get_token_from_cookie)):
                     
    token = token if token is not None and len(token) > 10  else token_cookie
    if token is None:
        return None
    try:
        payload = jwt.decode(token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except InvalidTokenError:
            return None
    return await get_user(username, db)


