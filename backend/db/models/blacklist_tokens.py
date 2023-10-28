import uuid
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Base


class TokenBlacklist(Base):
    __tablename__ = "blacklist"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    token = relationship("Token", back_populates="blacklist")
