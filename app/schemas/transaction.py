from pydantic import BaseModel
from typing import Optional

class TransactionCreate(BaseModel):
    item_id: str
    buyer_id: str
    seller_id: str
    price: float

class TransactionUpdate(BaseModel):
    price: Optional[float] = None

class TransactionResponse(BaseModel):
    id: str
    item_id: str
    buyer_id: str
    seller_id: str
    price: float