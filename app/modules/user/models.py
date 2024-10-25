from sqlalchemy import (Column, 
                        Integer, 
                        String, 
                        Boolean, 
                        ForeignKey,
                        DateTime)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base



class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_validate = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, 
                                  onupdate=datetime.now)                                                            

    role_id = Column(Integer, ForeignKey("roles.id"))    
    role = relationship("Role", back_populates="users",
                                uselist=False,
                                lazy="joined")

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    
    users = relationship("User", back_populates="role")
