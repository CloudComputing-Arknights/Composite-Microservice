from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ThreadUser(SQLModel, table=True):
    __tablename__ = "thread_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: str = Field(index=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

