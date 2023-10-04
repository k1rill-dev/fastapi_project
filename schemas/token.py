from datetime import datetime

from pydantic import UUID4, BaseModel


class TokenAfterLogin(BaseModel):
    access_token: str
    token_type: str
    refresh_token_uuid: UUID4
    message: str


class ShowTokenAfterInsert(BaseModel):
    token_id: UUID4
    user_id: UUID4
    token: str
    date_created: datetime


class TokenPayload(BaseModel):
    id: UUID4
