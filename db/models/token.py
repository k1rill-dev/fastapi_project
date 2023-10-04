import uuid
from sqlalchemy import Integer, ForeignKey, text
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship
from db.models import User
from .base import Base


class Token(Base):
    __tablename__ = "token"

    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.user_id), nullable=False, unique=True)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user = relationship("User", back_populates="token")
