from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class CreateTransactionReq(BaseModel):
    requested_item_id: str
    receiver_user_id: str
    type: Literal["trade", "purchase"]
    offered_item_id: Optional[str] = None
    offered_price: Optional[float] = None
    status: Literal["pending", "accepted", "rejected", "canceled", "completed"] = "pending"
    message: Optional[str] = None


class TransactionRes(BaseModel):
    transaction_id: str
    requested_item_id: str
    initiator_user_id: str
    receiver_user_id: str
    type: Literal["trade", "purchase"]
    offered_item_id: Optional[str] = None
    offered_price: Optional[float] = None
    status: Literal["pending", "accepted", "rejected", "canceled", "completed"]
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UpdateTransactionStatusReq(BaseModel):
    status: Literal["accepted", "rejected", "canceled", "completed"]


