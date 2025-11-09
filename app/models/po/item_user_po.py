from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class ItemUser(SQLModel, table=True):
    __tablename__ = "item_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: str = Field(index=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
