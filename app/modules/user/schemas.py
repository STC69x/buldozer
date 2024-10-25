from pydantic import BaseModel, validator
from datetime import datetime
from .roles_enum import Role

class UserBase(BaseModel):
    username: str
    password: str
    email: str
    is_active: bool = False
    is_validate: bool = False
    created_at: datetime
    update_at: datetime
    role: Role

class User(UserBase):
    id: int
    username: str
    email: str
    is_active: bool
    is_validate: bool
    created_at: datetime
    update_at: datetime
    role: str    

class UserCreate(UserBase):
    pass

    @validator('role')
    def role_must_be_valid(cls, value):
        if value not in [Role.USER, Role.ANONYMOUSE]:
            raise ValueError('Invalid role')
        return value

class UserLogin(BaseModel):
    username: str
    password: str
