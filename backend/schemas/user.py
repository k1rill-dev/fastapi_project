from pydantic import EmailStr

from backend.schemas.base import Base


class UserRead(Base):
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(Base):
    name: str
    surname: str
    email: EmailStr
    password: str


class UserUpdate(Base):
    name: str
    surname: str
    email: EmailStr


class UserDeactivate(Base):
    email: EmailStr
    is_active: bool
