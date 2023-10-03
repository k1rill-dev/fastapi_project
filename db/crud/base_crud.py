from typing import TypeVar, Generic, Type

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db.connect_db import get_db
from db.models.users import Base, User

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self._model = model
        self._session = db

    def create(
            self,
            name: str,
            surname: str,
            email: str,
            hashed_password: str) -> User:
        raise NotImplementedError('Interface not implemented')

    def get(self):
        raise NotImplementedError('Interface not implemented')

    def update(self):
        raise NotImplementedError('Interface not implemented')

    def delete(self):
        raise NotImplementedError('Interface not implemented')
