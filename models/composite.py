from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


# -----------------------------------------------------------------------------
# Pydantic Models for Composite Responses
# -----------------------------------------------------------------------------
class PostAuthor(BaseModel):
    id: str
    username: str


class EnrichedPost(BaseModel):
    item_UUID: str
    title: str
    description: Optional[str] = None
    condition: str
    price: float
    transaction_type: str
    image_urls: List[str]
    author: PostAuthor


class TradeInitiationRequest(BaseModel):
    item_id: str
    initiator_user_id: str


class EnrichedTrade(BaseModel):
    transactionId: int
    item_title: str
    status: str
    initiator: PostAuthor
    receiver: PostAuthor
    createdAt: str
