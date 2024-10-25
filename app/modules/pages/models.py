from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    slug = Column(String, unique=True, index=True)
    template = Column(String, nullable=True, default=None)
        
    pages = relationship("Page", back_populates="category")

class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    page_name = Column(String, index=True)
    content = Column(String, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    slug = Column(String, unique=True, index=True)
    
    page_settings = relationship("PageSettings", 
                                 back_populates="page", 
                                 uselist=False,
                                 lazy="joined")

    category = relationship("Category", back_populates="pages")

class PageSettings(Base):
    __tablename__ = "pages_settings"
    
    page_id = Column(Integer, ForeignKey("pages.id"), primary_key=True, index=True)
    title = Column(String)
    keywords = Column(String, nullable=True)
    is_homepage = Column(Boolean, default=False, index=True)
    template = Column(String, default="page_base.html")
    
    page = relationship("Page", back_populates="page_settings")
