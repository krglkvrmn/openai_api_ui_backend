import datetime
import uuid

from pydantic import BaseModel


class SessionToken(BaseModel):
    token: uuid.UUID
    expiry_date: datetime.datetime
