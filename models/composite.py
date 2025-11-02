from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

# Import enums from the generated Item client so our Pydantic models stay aligned
from client.item.item_thread_api_client.models.category_type import CategoryType
from client.item.item_thread_api_client.models.condition_type import ConditionType
from client.item.item_thread_api_client.models.transaction_type import TransactionType


# -----------------------------------------------------------------------------
# Pydantic Models for Composite Requests/Responses
# -----------------------------------------------------------------------------

class LoginRequest(BaseModel):
    """Placeholder login payload. Actual authentication is not implemented yet.

    This exists so the endpoint contract is in place.
    """

    username: str = Field(..., description="Username to log in as (placeholder)")
    password: str = Field(..., description="Password (ignored — auth not implemented)")


class LoginResponse(BaseModel):
    message: str


class CurrentUser(BaseModel):
    """Current logged-in user information (placeholder)."""

    username: str
    user_id: Optional[UUID] = Field(None, description="UUID from User service if resolved")


class CreateOwnItemRequest(BaseModel):
    """Create an item on behalf of the currently logged-in user.

    The server will enforce ownership and set the user UUID from the session (placeholder).
    """

    title: str
    condition: ConditionType
    transaction_type: TransactionType
    price: float
    description: Optional[str] = None
    category: Optional[List[CategoryType]] = None
    location: Optional[str] = None
    image_urls: Optional[List[str]] = None


class UpdateOwnItemRequest(BaseModel):
    """Partial update for an item owned by the current user."""

    title: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[ConditionType] = None
    category: Optional[List[CategoryType]] = None
    transaction_type: Optional[TransactionType] = None
    price: Optional[float] = None
    location: Optional[str] = None
    image_urls: Optional[List[str]] = None


class TransactionInitRequest(BaseModel):
    """Placeholder request to start a transaction as the current user.

    Note: The Transaction service uses integer item IDs and string user IDs, which may
    not directly match the Item/User services used here. This is a placeholder to
    establish the API contract in the composite layer.
    """

    item_id: int
    receiver_user_id: str


class TransactionInitResponse(BaseModel):
    message: str
