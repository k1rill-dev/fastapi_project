import uuid
from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str
    surname: str
    email: EmailStr


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    name: str
    surname: str
    email: EmailStr
    password: str
