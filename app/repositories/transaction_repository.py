import httpx
from app.schemas.transaction import TransactionCreate, TransactionUpdate
TRANSACTION_SERVICE_URL = "http://34.172.7.104:8000"


async def get_all_transactions(skip: int = 0, limit: int = 20):
    async with httpx.AsyncClient(base_url=TRANSACTION_SERVICE_URL) as client:
        response = await client.get("/transactions", params={"skip": skip, "limit": limit})
        response.raise_for_status()
        return response.json()


async def get_transaction_by_id(transaction_id: str):
    async with httpx.AsyncClient(base_url=TRANSACTION_SERVICE_URL) as client:
        response = await client.get(f"/transactions/{transaction_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


async def get_transaction(transaction_data: TransactionCreate):
    async with httpx.AsyncClient(base_url=TRANSACTION_SERVICE_URL) as client:
        response = await client.post("/transactions", json=transaction_data.dict())
        response.raise_for_status()
        return response.json()


async def create_transaction(transaction_id: str, transaction_data: TransactionUpdate):
    async with httpx.AsyncClient(base_url=TRANSACTION_SERVICE_URL) as client:
        response = await client.patch(f"/transactions/{transaction_id}", json=transaction_data.dict())
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    
async def update_transaction(session: AsyncSession, transaction_id: str, updates: dict) -> Transaction:
    statement = select(Transaction).where(Transaction.id == transaction_id)
    result = await session.exec(statement)
    transaction = result.first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in updates.items():
        setattr(transaction, key, value)

    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction

async def delete_transaction(transaction_id: str):
    async with httpx.AsyncClient(base_url=TRANSACTION_SERVICE_URL) as client:
        response = await client.delete(f"/transactions/{transaction_id}")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True