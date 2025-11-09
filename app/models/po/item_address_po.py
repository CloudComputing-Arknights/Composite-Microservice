from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class ItemAddress(SQLModel, table=True):
    __tablename__ = "item_address"

    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: str = Field(index=True)
    address_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
