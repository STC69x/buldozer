from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.config.database import AsyncSession
from .models import User
from .roles_enum import Role
from sqlalchemy.future import select


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_user(username: str, db: AsyncSession):
    return (await db.execute(select(User)\
                             .filter(User.username == username)))\
                             .scalar_one_or_none()

async def create_user(username: str, 
                      password: str):
    hashed_password = get_password_hash(password)
    user = User(username=username, 
                hashed_password=hashed_password, 
                role=Role.ANONYMOUSE)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
