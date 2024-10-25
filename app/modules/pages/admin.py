from fastapi import (APIRouter, 
                     Depends, 
                     HTTPException, 
                     Request, 
                     Form,
                     status)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from typing import Annotated, Optional

from app.dependencies import get_db, get_current_user
from app.config.database import AsyncSession
from app.config.config import Config, ConfigSite
from app.modules.pages.schemas import  CategoryCreate, PageCreate
from app.modules.pages.models import Category, Page, PageSettings
from app.handlers.auth_role_checker import auth_and_roles_required
from app.handlers.http_errors import noauth, noapi


router = APIRouter()
cfg = Config()
cfg_site = ConfigSite()
templates = Jinja2Templates(directory = cfg.TEMPLATE_ADMIN_PATH)
router = APIRouter(tags = ["adminpanel"], prefix = "/adminpanel")

###############################
#Категории
###############################
@router.get("/categories")
async def get_categories_list(request: Request,
                              db: AsyncSession = Depends(get_db),
                              current_user = Depends(get_current_user),
                              message = Optional[str],
                              api: bool = False): 
    if auth_and_roles_required(current_user, ["administrator"]):
        try:
            categories = (await db.execute(select(Category)))\
                                            .scalars()\
                                            .all()
        except Exception as e:
            return templates.TemplateResponse("error.html", 
                                              {
                                                "request": request,
                                                "error": e
                                              }
                                          )
        if api:
            return categories
        return templates.TemplateResponse("categories_list.html", 
                                         {
                                          "request": request,
                                          "cfg": cfg_site,
                                          "message": message,
                                          "categories": categories
                                         }
                                     )
    if api:
        raise noauth
    return RedirectResponse("/user/login", status_code = status.HTTP_303_SEE_OTHER)

###################################
#Создание категории\Category create
###################################
@router.get("/category/create")
def create_category_form(request: Request, 
                         current_user = Depends(get_current_user),
                         api: bool = False):
    if api:
        raise noapi
    if auth_and_roles_required(current_user, ["administrator"]):
        return templates.TemplateResponse("category_create_form.html",
                                          {
                                           "request": request,
                                           "cfg": cfg_site,
                                          }
                                      )
    return RedirectResponse("/user/login", status_code = status.HTTP_303_SEE_OTHER)

@router.post("/category/create")
async def create_category(request: Request,
                          category: Annotated[CategoryCreate, Form()],  
                          db: AsyncSession = Depends(get_db),
                          current_user = Depends(get_current_user),
                          api: bool = False):
    if auth_and_roles_required(current_user, ["administrator"]):
        try:
            if category.template:
                category.template = category.template + ".html" 

            category = Category(name=category.name,
                                slug=category.slug,
                                template=category.template )
            db.add(category)
            await db.commit()
            await db.refresh(category)        
        except Exception as e:
            return templates.TemplateResponse("error.html", 
                                                  { 
                                                    "request": request,
                                                    "error": e
                                                  }
                                          )
        if api:
            return category

        return RedirectResponse("/adminpanel/categories?message=created",
                                status_code = status.HTTP_303_SEE_OTHER)
    if api:
        raise noauth
    return RedirectResponse("/user/login", status_code = status.HTTP_303_SEE_OTHER)

############################
#Список страниц \Pages List   
###########################
@router.get("/pages")
async def get_pages_list(request: Request, 
                         message = Optional[str], 
                         db: AsyncSession = Depends(get_db),
                         current_user = Depends(get_current_user),
                         api: bool = False):
    if auth_and_roles_required(current_user, ["administrator"]):
        try:
            pages = (await db.execute(select(Page)))\
                                      .scalars()\
                                      .all()
        except Exception as e:
            return templates.TemplateResponse("error.html", 
                                                  {
                                                    "request": request,
                                                    "error": e
                                                  }
                                              )
        if api:
            return pages
        return templates.TemplateResponse("pages_list.html", 
                                             {
                                              "request": request,
                                              "cfg": cfg_site,
                                              "message": message,
                                              "pages": pages
                                             }
                                         )
    if api:
        raise noauth
    return RedirectResponse("/user/login", status_code = status.HTTP_303_SEE_OTHER)

###############################
#Создание страницы\Page Create
###############################
@router.get("/page/create")
async def create_page_form(request: Request,
                           current_user = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db),
                           api: bool = False):  
    if api:
        raise noapi
    if auth_and_roles_required(current_user, ["administrator"]):
        categories = (await db.execute(select(Category)))\
                                       .scalars()\
                                       .all()

        return templates.TemplateResponse("page_create_form.html",
                                              {
                                               "request": request,
                                               "cfg": cfg_site,
                                               "categories": categories,
                                              }
                                          )
    return RedirectResponse("/user/login", status_code = status.HTTP_303_SEE_OTHER)

@router.post("/page/create")
async def page_category(request: Request,
                        page: Annotated[PageCreate, Form()], 
                        current_user = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db),
                        api: bool = False):
    if auth_and_roles_required(current_user, ["administrator"]):
        try:
            template =\
            page.template + ".html" if str(page.template) else None  

            page = Page(page_title = page.title,
                        slug = page.slug,
                        category_id = page.category_id,
                        template = template)
            db.add(page)
            await db.commit()
            await db.refresh(page)
        except Exception as e:
            return templates.TemplateResponse("error.html", 
                                                  { 
                                                    "request": request,
                                                    "error": e
                                                  }
                                              )
        if api:
            return page
        return RedirectResponse("/adminpanel/pages?message=created",
                                status_code = status.HTTP_303_SEE_OTHER)
    if api:
        return noauth     
    return RedirectResponse("/user/login", status_code = status.HTTP_303_SEE_OTHER)
