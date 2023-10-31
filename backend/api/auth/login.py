from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from core import settings
from db.models import User
from api.services import TokenService
from .utils import authenticate_user, _get_user_by_email_for_auth, get_current_user_from_token
from db.connect_db import get_db
from core.security import create_access_token, create_refresh_token, verify_refresh_token

login_router = APIRouter(prefix='/login')


async def _unset_all_cookies(response: Response) -> str:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token_uuid")
    response.delete_cookie(key="login_status")
    return "successful unset"


@login_router.post("/token")
async def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    token_worker = TokenService(db)
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
    response.set_cookie(key="access_token", value=f"{access_token}", httponly=True)

    response.set_cookie(key="login_status", value="true")

    refresh_token = await create_refresh_token(
        data={"sub": user.email}
    )
    token_in_db = await token_worker.get_token_from_db_with_user(user=user)
    if token_in_db is None:
        token_in_db = await token_worker.insert_refresh_token_into_db(refresh_token, user)

    response.set_cookie(key="refresh_token_uuid", value=f'{token_in_db.token_id}', httponly=True)

    return {
        "refresh_token_uuid": token_in_db.token_id,
        "message": "User Logged in Successfully."
    }


@login_router.post("/refresh")
async def get_new_access_token(response: Response,
                               token_uuid: UUID, db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(get_current_user_from_token)):
    token_worker = TokenService(db)
    token = await token_worker.get_token_from_db_with_id(token_uuid)
    refresh_data = await verify_refresh_token(token.token)
    user_email = refresh_data.get("sub")

    user = await _get_user_by_email_for_auth(email=user_email, session=db)

    new_access_token = await create_access_token(refresh_data)
    new_refresh_token = await create_refresh_token(data={"sub": user_email})

    await token_worker.delete_token(token_id=token.token_id)

    token_in_db = await token_worker.insert_refresh_token_into_db(token=new_refresh_token, user=user)

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token_uuid")

    response.set_cookie(key="access_token", value=f"{new_access_token}", httponly=True)
    response.set_cookie(key="refresh_token_uuid", value=f"{token_in_db.token_id}", httponly=True)

    return {
        "success": True,
        "refresh_token_uuid": token_in_db.token_id
    }


@login_router.post('/logout')
async def logout(response: Response,
                 current_user: User = Depends(get_current_user_from_token)):
    status_unset = await _unset_all_cookies(response)
    user_id = current_user.user_id

    return {
        "status": status_unset,
        "user_id": user_id
    }
