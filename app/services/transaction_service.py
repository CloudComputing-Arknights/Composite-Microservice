from app.repositories.transaction_repository import (
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    update_transaction,
    delete_transaction
)

async def get_all_transactions(skip: int = 0, limit: int = 20):
    return await get_all_transactions(skip=skip, limit=limit)

async def get_transaction_by_id(transaction_id: str):
    return await get_transaction_by_id(transaction_id)

async def create_transaction(payload):
    return await create_transaction(payload)

async def update_transaction(transaction_id: str, payload):
    return await update_transaction(transaction_id, payload)

async def delete_transaction(transaction_id: str):
    return await delete_transaction(transaction_id)