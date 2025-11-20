from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import enum

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class JobRead(BaseModel):
    job_UUID: UUID
    status: JobStatus
    item_UUID: Optional[UUID] = None
    error_message: Optional[str] = None
