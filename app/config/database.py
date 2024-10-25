import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

###
# Database Configuration
###

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://cms_user:12344321@localhost:5432/cms"

engine = create_async_engine(os.getenv("DB_URL", SQLALCHEMY_DATABASE_URL))

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)

Base = declarative_base()
