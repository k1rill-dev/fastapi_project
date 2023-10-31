from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Depends
from starlette import status

from api.auth.utils import oauth2_scheme
from core import settings
from jose import jwt, JWTError
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS) + datetime.utcnow()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY_REFRESH, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def verify_refresh_token(token: str = Depends(oauth2_scheme)) -> dict:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_REFRESH, algorithms=settings.ALGORITHM)

        email: str = payload.get("sub")
        if email is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return {"sub": email}


async def get_new_access_token(token: str) -> str:
    data = await verify_refresh_token(token)
    return await create_access_token(data)
