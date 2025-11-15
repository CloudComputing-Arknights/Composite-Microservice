from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import (
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    update_transaction,
    delete_transaction
)

# Create APIRouter for global transaction endpoints
transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])

# ---------------------------------------------------------------------------
# Public/Admin endpoint: Get all transactions in the system
# ---------------------------------------------------------------------------
@transaction_router.get("/", response_model=List[TransactionResponse])
async def list_transactions(skip: int = 0, limit: int = 20):
    transactions = await get_all_transactions(skip=skip, limit=limit)
    return transactions

# ---------------------------------------------------------------------------
# Public/Admin endpoint: Get transaction by ID
# ---------------------------------------------------------------------------
@transaction_router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str):
    transaction = await get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# ---------------------------------------------------------------------------
# Admin endpoint: Create a new transaction
# ---------------------------------------------------------------------------
@transaction_router.post("/", response_model=TransactionResponse)
async def create_new_transaction(payload: TransactionCreate):
    return await create_transaction(payload)

# ---------------------------------------------------------------------------
# Admin endpoint: Update a transaction
# ---------------------------------------------------------------------------
@transaction_router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_existing_transaction(transaction_id: str, payload: TransactionUpdate):
    updated = await update_transaction(transaction_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated

# ---------------------------------------------------------------------------
# Admin endpoint: Delete a transaction
# ---------------------------------------------------------------------------
@transaction_router.delete("/{transaction_id}")
async def delete_existing_transaction(transaction_id: str):
    success = await delete_transaction(transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted successfully"}