import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from api.auth.setup import backend
from db.managers.user_manager import get_user_manager
from db.models import User
from api import router
import uvicorn

from schemas.user import UserRead, UserCreate


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_auth_router(backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app=app, host='localhost', port=8000)
