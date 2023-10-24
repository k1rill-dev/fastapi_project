from typing import Type, Union
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.db.crud.base_crud import BaseCRUD
from backend.db.models import Token, User


class CrudToken(BaseCRUD):
    def __init__(self, model: Type[Token] = Token, session: AsyncSession = None):
        super().__init__(model, session)
        self._session = session

    async def get_token_by_user(self, user: User) -> Union[Token, None]:
        query = select(Token).join(User).where(Token.user_id == user.user_id)
        res = await self._session.execute(query)
        token = res.fetchone()
        if token is not None:
            return token[0]

    async def get_token_by_id(self, token_id: UUID) -> Union[Token, None]:
        query = select(Token).where(token_id == Token.token_id)
        res = await self._session.execute(query)
        token = res.fetchone()
        if token is not None:
            return token[0]

    async def create(
            self,
            token: str,
            user_id: str) -> Token:
        new_token = Token(
            token=token,
            user_id=user_id
        )
        self._session.add(new_token)
        await self._session.flush()
        return new_token

    async def delete(self, user: User = None, token_id: UUID = None) -> bool:
        if user is not None:
            query = delete(Token).where(user.user_id == Token.user_id)
            res = await self._session.execute(query)
            return True
        elif token_id is not None:
            query = delete(Token).where(token_id == Token.token_id)
            res = await self._session.execute(query)
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
