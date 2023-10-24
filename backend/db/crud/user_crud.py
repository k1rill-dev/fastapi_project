from typing import Type, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.crud.base_crud import BaseCRUD, ModelType
from backend.db.models import User


class CrudUser(BaseCRUD):
    def __init__(self, model: Type[ModelType] = User, session: AsyncSession = None):
        super().__init__(model, session)
        self._session = session

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(self._model).where(self._model.email == email)
        res = await self._session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def create(
            self,
            name: str,
            surname: str,
            email: str,
            hashed_password: str) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password
        )
        self._session.add(new_user)
        await self._session.flush()
        return new_user
