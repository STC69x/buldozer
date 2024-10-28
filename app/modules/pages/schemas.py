from pydantic import BaseModel
from typing import Optional

class PageSettingsBase(BaseModel):
    title: Optional[str] = None
    keywords: Optional[str] = None
    is_homepage: bool = False

class PageSettings(PageSettingsBase):
    page_id: int

class PageBase(BaseModel):
    name: str
    content: str
    category_id: int 
    slug: str

class PageCreate(PageBase):
    template: Optional[str]

class PageEdit(PageCreate):
    pass

class Page(PageBase):
    id: int

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    slug: str
    template: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributs = True

