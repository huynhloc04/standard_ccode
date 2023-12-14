from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel
from datetime import datetime


class TimeMixin(BaseModel):
    """Mixin class for datetime value of when the entity was created and when it was last modified. """

    created_at: datetime = Field(default_factory=datetime.now)
    verified_at: datetime = Field(default_factory=datetime.now)
    registered_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)


class UserModel(SQLModel, TimeMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool
    is_verified: bool