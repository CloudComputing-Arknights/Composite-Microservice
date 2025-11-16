from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TransactionUserItem(SQLModel, table=True):
    __tablename__ = "transaction_user_item"

    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: str = Field(index=True, unique=True)
    initiator_user_id: str = Field(index=True)
    receiver_user_id: str = Field(index=True)
    requested_item_id: str = Field(index=True)
    offered_item_id: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
