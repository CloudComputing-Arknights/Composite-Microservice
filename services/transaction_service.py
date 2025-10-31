import httpx
from fastapi import HTTPException
from pydantic import BaseModel

TRANSACTION_SERVICE_URL = "http://34.172.7.104:8000"


class NewTrade(BaseModel):
    itemId: int
    initiatorUserId: str
    receiverUserId: str


async def create_transaction(trade_data: NewTrade) -> dict:
    """
    Creates a new transaction in the Transaction service.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{TRANSACTION_SERVICE_URL}/transactions/transaction",
                json=trade_data.dict(),
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Transaction Service: {e.response.text}",
            )


async def list_transactions_for_user(user_id: str) -> list[dict]:
    """
    Fetches all transactions for a given user (both as initiator and receiver).
    """
    async with httpx.AsyncClient() as client:
        try:
            # Fetch transactions where the user is the initiator
            initiator_params = {"initiatorUserId": user_id, "limit": 100}
            initiator_resp = await client.get(f"{TRANSACTION_SERVICE_URL}/transactions", params=initiator_params)
            initiator_resp.raise_for_status()

            # Fetch transactions where the user is the receiver
            receiver_params = {"receiverUserId": user_id, "limit": 100}
            receiver_resp = await client.get(f"{TRANSACTION_SERVICE_URL}/transactions", params=receiver_params)
            receiver_resp.raise_for_status()

            # Combine and remove duplicates
            transactions = {t['transactionId']: t for t in initiator_resp.json()}
            for t in receiver_resp.json():
                transactions[t['transactionId']] = t

            return list(transactions.values())

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Transaction Service: {e.response.text}",
            )