from datetime import timedelta
from uuid import UUID

import sqlalchemy
from asyncpg import UniqueViolationError
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from core import settings
from db.crud.token_crud import CrudToken
from db.models import User, Token
from schemas.token import ShowTokenAfterInsert, TokenAfterLogin
from .utils import authenticate_user, _get_user_by_email_for_auth, get_current_user_from_token
from db.connect_db import get_db
from core.security import create_access_token, create_refresh_token, verify_refresh_token

login_router = APIRouter(prefix='/login')


async def _insert_refresh_token_into_db(token: str, user: User, session: AsyncSession) -> ShowTokenAfterInsert:
    async with session.begin():
        c = CrudToken(session=session)
        token = await c.create(token=token, user_id=user.user_id)
        return ShowTokenAfterInsert(
            token_id=token.token_id,
            user_id=token.user_id,
            token=token.token,
            date_created=token.date_created
        )


async def _get_token_from_db_with_user(user: User, session: AsyncSession) -> Token:
    async with session.begin():
        c = CrudToken(session=session)
        token = await c.get_token_by_user(user)
        return token


async def _get_token_from_db_with_id(token_id: UUID, session: AsyncSession) -> Token:
    async with session.begin():
        c = CrudToken(session=session)
        token = await c.get_token_by_id(token_id)
        return token


async def _delete_token(user: User = None, token_id: UUID = None, session: AsyncSession = None):
    async with session.begin():
        c = CrudToken(session=session)
        await c.delete(user, token_id)
        return "Token successful delete"


@login_router.post("/token", response_model=TokenAfterLogin)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    refresh_token = await create_refresh_token(
        data={"sub": user.email}
    )
    token_in_db = await _get_token_from_db_with_user(user=user, session=db)
    if token_in_db is None:
        token_in_db = await _insert_refresh_token_into_db(refresh_token, user, db)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "refresh_token_uuid": token_in_db.token_id,
        "message": "User Logged in Successfully."
    }


@login_router.get("/refresh")
async def get_new_access_token(token_uuid: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    token = await _get_token_from_db_with_id(token_uuid, db)
    refresh_data = await verify_refresh_token(token.token)
    user_email = refresh_data.get("sub")

    user = await _get_user_by_email_for_auth(email=user_email, session=db)

    new_access_token = await create_access_token(refresh_data)
    new_refresh_token = await create_refresh_token(data={"sub": user_email})

    await _delete_token(token_id=token.token_id, session=db)

    token_in_db = await _insert_refresh_token_into_db(token=new_refresh_token, user=user, session=db)

    return {
        "access_token": new_access_token,
        "refresh_token_uuid": token_in_db.token_id,
        "token_type": "Bearer"
    }
