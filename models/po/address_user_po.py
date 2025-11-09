from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class AddressUser(SQLModel, table=True):
    __tablename__ = "address_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    address_id: str = Field(index=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)