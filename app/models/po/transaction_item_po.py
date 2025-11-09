from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class ItemRole(str, Enum):
    REQUESTED = "requested"
    OFFERED = "offered"


class TransactionItem(SQLModel, table=True):
    __tablename__ = "transaction_item"

    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: str = Field(index=True)
    item_id: str = Field(index=True)
    item_role: ItemRole = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
