import uuid
from .connect_db import get_db
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Boolean, Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, Mapped

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    id: UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = Column(String, nullable=False)
    surname: Mapped[str] = Column(String, nullable=False)
    email: Mapped[str] = Column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = Column(String, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = Column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = Column(
        Boolean, default=False, nullable=False
    )


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)
