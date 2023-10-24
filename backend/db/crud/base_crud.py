from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.users import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self._model = model
        self._session = db

    def create(
            self,
            **kwargs) -> Type[ModelType]:
        raise NotImplementedError('Interface not implemented')

    def get(self, **kwargs) -> Type[ModelType]:
        ...

    def update(self, **kwargs) -> Type[ModelType]:
        ...

    def delete(self, **kwargs) -> bool:
        ...
