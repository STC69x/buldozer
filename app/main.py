from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .config.config import Config
from .config.database import engine, Base
#from .src.dependencies import get_token_header
#from .src.internal import admin
from .routers import router


###
# Main application file
###

def get_application() -> FastAPI:
    ''' Configure, start and return the application '''

    ## Start FastApi App 
    application = FastAPI()
    
    ##Config Load
    cfg = Config()

    ##Load static
    application.mount("/static", StaticFiles(directory="static"), name="static")
    
    ## Mapping routes
    application.include_router(router)

    ## Add exception handlers
    #application.add_exception_handler(HTTPException, http_error_handler)

    ## Allow cors TO CFG
    application.add_middleware(
        CORSMiddleware,
        allow_origins = cfg.ALLOWED_HOSTS or ["*"],
        allow_credentials = True, 
        allow_methods = cfg.ALLOWED_METHODS or ["*"],
        allow_headers = cfg.ALLOWED_HEADERS or ["*"],
    )

 #   ## Example of admin route
 #   application.include_router(
 #       admin.router,
 #       prefix="/admin",
 #       tags=["admin"],
 #       dependencies=[Depends(get_token_header)],
 #       responses={418: {"description": "I'm a teapot"}},
 #   )

    return application

app = get_application()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()

#@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = AsyncSession(engine) 
        response = await call_next(request)
    except Exception as e:
        response = JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {e}"},
        )
        if hasattr(request.state, 'db'):
            await request.state.db.rollback()
    finally:
        if hasattr(request.state, 'db'):
            await request.state.db.close()
    return response
