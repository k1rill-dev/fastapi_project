from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.crud.token_crud import CrudToken
from db.models import User, Token
from schemas.token import ShowTokenAfterInsert


class TokenService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._crud_token = CrudToken(session=self._session)

    async def insert_refresh_token_into_db(self, token: str, user: User) -> ShowTokenAfterInsert:
        async with self._session.begin():
            token = await self._crud_token.create(token=token, user_id=user.user_id)
            return ShowTokenAfterInsert(
                token_id=token.token_id,
                user_id=token.user_id,
                token=token.token,
                date_created=token.date_created
            )

    async def get_token_from_db_with_user(self, user: User) -> Token:
        async with self._session.begin():
            token = await self._crud_token.get_token_by_user(user)
            return token

    async def get_token_from_db_with_id(self, token_id: UUID) -> Token:
        async with self._session.begin():
            token = await self._crud_token.get_token_by_id(token_id)
            return token

    async def delete_token(self, user: User = None, token_id: UUID = None):
        async with self._session.begin():
            await self._crud_token.delete(user, token_id)
            return "Token successful delete"
