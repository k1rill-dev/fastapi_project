from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.utils import get_current_user_from_token
from core import Hasher
from db.crud.user_crud import CrudUser
from db.connect_db import get_db
from db.models import User
from schemas.user import UserCreate, UserRead

router = APIRouter()


async def _create_new_user(body: UserCreate, session: AsyncSession) -> UserRead:
    async with session.begin():
        user_crud = CrudUser(User, session)
        user = await user_crud.create(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password)
        )
        return UserRead(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


@router.post("/create", response_model=UserRead)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> UserRead:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.get('/')
def index(current_user: User = Depends(get_current_user_from_token)):
    return {"login": True, "email": current_user.email}
