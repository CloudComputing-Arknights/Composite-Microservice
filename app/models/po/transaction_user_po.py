from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    INITIATOR = "initiator"
    RECEIVER = "receiver"


class TransactionUser(SQLModel, table=True):
    __tablename__ = "transaction_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: str = Field(index=True)
    user_id: str = Field(index=True)
    user_role: UserRole = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
