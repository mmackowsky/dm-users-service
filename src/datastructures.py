from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text

from database import Base


class UsernamePasswordForm(BaseModel):
    username: str
    password: str


class UserForm(UsernamePasswordForm):
    email: str = None
    full_name: str = None
    user_type: str


class UserUpdateForm(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    user_type: str = None


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    full_name = Column(String(150), unique=False, nullable=True)
    user_type = Column(String(50), unique=False, nullable=False)
    hashed_password = Column(String(200), unique=True, nullable=False)
    created_by = Column(ForeignKey(id), nullable=False)
