from fastapi import (APIRouter, 
                     Depends, 
                     HTTPException, 
                     Request,
                     status)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dependencies import get_db
from app.config.config import Config, ConfigSite
from app.dependencies import get_current_user
from app.modules.user.models import User
from app.handlers.http_errors import notfound
from .models import Category, Page, PageSettings
from .schemas import PageBase

router = APIRouter()
cfg = Config()
cfg_site = ConfigSite()
templates = Jinja2Templates(directory = cfg.TEMPLATE_PATH)
router = APIRouter(tags=["pages"])


######################################
#Cтрацица в категории/Page in Category
#####################################
@router.get("/{category_slug}/{page_slug}")
async def get_page_by_category(request: Request,
                               category_slug: str, 
                               page_slug: str, 
                               db: AsyncSession = Depends(get_db), 
                               current_user: User = Depends(get_current_user),
                               api: bool = False):
    category = (await db.execute(select(Category)\
                                .filter(Category.slug == category_slug)))\
                                .scalar_one_or_none()
    if not category:
        if api:
            raise notfound
        return templates.TemplateResponse(cfg.ERROR_404_TEMPLATE, 
                                          {
                                           "request": request,
                                           "cfg": cfg_site
                                          }
                                      )
    page = (await db.execute(select(Page)\
                            .filter(Page.category_id == category.id,
                                    Page.slug == page_slug)))\
                            .scalar_one_or_none()
    if not page:
        if api:
            raise notfound
        return templates.TemplateResponse(cfg.ERROR_404_TEMPLATE, 
                                          {
                                           "request": request,
                                           "cfg": cfg_site
                                          }
                                      )
    if api:
        return page
    template_is_set = page.page_settings.template\
                      if page.page_settings is not None else None  
    template = template_is_set if template_is_set is not None\
                               else cfg.DEFAULT_TEMPLATE
    return templates.TemplateResponse(template, 
                                              {
                                               "request": request,
                                               "page": page,
                                               "user": current_user
                                              }
                                          )

####################################################
#Вывод страцицы или категории/View Page Or Category  
####################################################
@router.get("/{slug}")
async def get_page(request: Request, slug: str, 
                   db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user),
                   api: bool = False):
    category = (await db.execute(select(Category)\
                                 .filter(Category.slug == slug)))\
                                 .scalar_one_or_none()
    page = (await db.execute(select(Page)\
                             .filter(Page.slug == slug)))\
                             .scalar_one_or_none()
    if category:
        if api:
            return category
        template = category.template if category.template is not None\
                                      else cfg.DEFAULT_CATEGORY_TEMPLATE
        return templates.TemplateResponse(template, 
                                              {
                                               "request": request,
                                               "category": category,
                                               "user": current_user
                                              }
                                         )
    if page:
        if page.category_id:
            category = (await db.execute(select(Category)\
                                         .filter(Category.id == page.category_id)))\
            .scalar_one_or_none()
            if api:
                return RedirectResponse("{0}/{1}?api=True"\
                                        .format(category.slug, page.slug), 
                                        status_code = status.HTTP_302_FOUND)
            return RedirectResponse("{0}/{1}".format(category.slug, page.slug), 
                                    status_code = status.HTTP_302_FOUND)
    if api:
        raise notfound
    return templates.TemplateResponse(cfg.ERROR_404_TEMPLATE, 
                                      {
                                       "request": request,
                                       "cfg": cfg_site
                                      }
                                   )
###########################
#Главная страница/Home Page
###########################
@router.get("/")
async def get_homepage(request: Request,
                       db: AsyncSession = Depends(get_db),
                       api: bool = False, 
                       current_user: User = Depends(get_current_user)):
    
    homepage = (await db.execute(select(Page)\
                                 .join(PageSettings, Page.page_settings)\
                                 .filter(PageSettings.is_homepage == True)
    )).scalar_one_or_none()
    if homepage:
        #Устанавливаем шаблона
        template_is_set = homepage.page_settings.template    
        template = template_is_set + ".html"\
                   if str(template_is_set) else cfg.DEFAULT_TEMPLATE
        return templates.TemplateResponse(template, 
                                              {
                                               "request": request,
                                               "page": homepage,
                                               "user": current_user
                                              }
                                          )
    if api:
          raise notfound
    return templates.TemplateResponse(cfg.ERROR_404_TEMPLATE, 
                                              {
                                               "request": request,
                                               "cfg": cfg_site
                                              }
                                          )
