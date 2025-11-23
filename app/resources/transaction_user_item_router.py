from fastapi import APIRouter, HTTPException, Header, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Literal
import asyncio

from app.models.dto.transaction_user_item_dto import (
    CreateTransactionReq,
    TransactionRes,
    UpdateTransactionStatusReq
)
from app.services.transaction_user_item_repository import (
    create_transaction_user_item_relation,
    get_transaction_relation,
    get_user_transactions,
    verify_transaction_initiator,
    verify_transaction_receiver,
    delete_transaction_relation
)
from app.utils.db_connection import SessionDep
from app.utils.config import get_transaction_client
from app.utils.auth import get_user_id_from_token

from app.client.transaction.transaction_api_client.api.default import (
    create_transaction_transactions_transaction_post,
    get_transaction_transactions_transaction_id_get,
    list_transactions_transactions_get,
    update_transaction_transactions_transaction_id_put,
    delete_transaction_transactions_transaction_id_delete
)
from app.client.transaction.transaction_api_client.models.new_transaction_request import NewTransactionRequest
from app.client.transaction.transaction_api_client.models.new_transaction_request_type import NewTransactionRequestType
from app.client.transaction.transaction_api_client.models.new_transaction_request_status import NewTransactionRequestStatus
from app.client.transaction.transaction_api_client.models.update_status_request import UpdateStatusRequest
from app.client.transaction.transaction_api_client.models.update_status_request_status import UpdateStatusRequestStatus
from app.client.transaction.transaction_api_client.models.list_transactions_transactions_get_status_param_type_0 import (
    ListTransactionsTransactionsGetStatusParamType0
)
from app.client.transaction.transaction_api_client.models.list_transactions_transactions_get_type_type_0 import (
    ListTransactionsTransactionsGetTypeType0
)

transaction_user_item_router = APIRouter(
    tags=["Transaction User Item"]
)

security = HTTPBearer()


@transaction_user_item_router.post("/transactions/transaction", response_model=TransactionRes, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: CreateTransactionReq,
    session: SessionDep,
    token: HTTPAuthorizationCredentials = Depends(security),
    x_idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key")
):
    """Create a new transaction."""
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        transaction_req = NewTransactionRequest(
            type_=NewTransactionRequestType(payload.type),
            offered_price=payload.offered_price,
            status=NewTransactionRequestStatus(payload.status),
            message=payload.message,
        )

        request_kwargs = {
            "client": get_transaction_client(),
            "body": transaction_req,
        }

        if x_idempotency_key:
            request_kwargs["x_idempotency_key"] = x_idempotency_key

        transaction_result = await create_transaction_transactions_transaction_post.asyncio(
            **request_kwargs
        )

        if not transaction_result:
            raise HTTPException(status_code=500, detail="Failed to create transaction in microservice")
        
        # Create local relation: current user is the initiator
        relation = await create_transaction_user_item_relation(
            session=session,
            transaction_id=transaction_result.transaction_id,
            initiator_user_id=str(user_uuid),
            receiver_user_id=payload.receiver_user_id,
            requested_item_id=payload.requested_item_id,
            offered_item_id=payload.offered_item_id,
        )
        
        return TransactionRes(
            transaction_id=transaction_result.transaction_id,
            requested_item_id=relation.requested_item_id,
            initiator_user_id=relation.initiator_user_id,
            receiver_user_id=relation.receiver_user_id,
            type=transaction_result.type_.value,
            offered_item_id=relation.offered_item_id,
            offered_price=transaction_result.offered_price if transaction_result.offered_price else None,
            status=transaction_result.status.value,
            message=transaction_result.message if transaction_result.message else None,
            created_at=transaction_result.created_at,
            updated_at=transaction_result.updated_at,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")


@transaction_user_item_router.get("/transactions/{transaction_id}", response_model=TransactionRes)
async def get_transaction(
    transaction_id: str,
    session: SessionDep,
    token: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a transaction by ID."""
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        # Parallel execution: fetch from microservice and local DB simultaneously
        transaction_result, relation = await asyncio.gather(
            get_transaction_transactions_transaction_id_get.asyncio(
                client=get_transaction_client(),
                transaction_id=transaction_id
            ),
            get_transaction_relation(session, transaction_id)
        )
        
        if not transaction_result:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Verify user is a participant (initiator or receiver)
        user_id_str = str(user_uuid)
        if user_id_str not in [relation.initiator_user_id, relation.receiver_user_id]:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return TransactionRes(
            transaction_id=transaction_result.transaction_id,
            requested_item_id=relation.requested_item_id,
            initiator_user_id=relation.initiator_user_id,
            receiver_user_id=relation.receiver_user_id,
            type=transaction_result.type_.value,
            offered_item_id=relation.offered_item_id,
            offered_price=transaction_result.offered_price if transaction_result.offered_price else None,
            status=transaction_result.status.value,
            message=transaction_result.message if transaction_result.message else None,
            created_at=transaction_result.created_at,
            updated_at=transaction_result.updated_at,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@transaction_user_item_router.get("/transactions", response_model=list[TransactionRes])
async def list_transactions(
    session: SessionDep,
    token: HTTPAuthorizationCredentials = Depends(security),
    status_param: Optional[Literal["pending", "accepted", "rejected", "canceled", "completed"]] = None,
    requested_item_id: Optional[str] = None,
    type: Optional[Literal["trade", "purchase"]] = None,
    limit: int = 50,
    offset: int = 0,
):
    """List all transactions for the current user."""
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        user_id_str = str(user_uuid)
        
        # Prepare query parameters for downstream service
        status_param_client = None
        if status_param:
            status_param_client = ListTransactionsTransactionsGetStatusParamType0(status_param)
        
        type_client = None
        if type:
            type_client = ListTransactionsTransactionsGetTypeType0(type)
        
        # Parallel execution: fetch user relations and downstream transactions simultaneously
        relations, transactions_result = await asyncio.gather(
            get_user_transactions(session, user_id_str),
            list_transactions_transactions_get.asyncio(
                client=get_transaction_client(),
                status_param=status_param_client,
                type_=type_client,
                limit=limit,
                offset=offset
            )
        )
        
        if requested_item_id:
            relations = [r for r in relations if r.requested_item_id == requested_item_id]
        
        relation_map = {r.transaction_id: r for r in relations}
        
        if not transactions_result:
            return []
        
        # Combine results: only include transactions where user is a participant
        combined_results = []
        for trans in transactions_result:
            if trans.transaction_id not in relation_map:
                continue
            
            rel = relation_map[trans.transaction_id]
            combined_results.append(TransactionRes(
                transaction_id=trans.transaction_id,
                requested_item_id=rel.requested_item_id,
                initiator_user_id=rel.initiator_user_id,
                receiver_user_id=rel.receiver_user_id,
                type=trans.type_.value,
                offered_item_id=rel.offered_item_id,
                offered_price=trans.offered_price if trans.offered_price else None,
                status=trans.status.value,
                message=trans.message if trans.message else None,
                created_at=trans.created_at,
                updated_at=trans.updated_at,
            ))
        
        return combined_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@transaction_user_item_router.put("/transactions/{transaction_id}", response_model=TransactionRes)
async def update_transaction(
    transaction_id: str,
    payload: UpdateTransactionStatusReq,
    session: SessionDep,
    token: HTTPAuthorizationCredentials = Depends(security)
):
    """Update a transaction's status."""
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        user_id_str = str(user_uuid)
        
        relation = await get_transaction_relation(session, transaction_id)
        
        # Verify user is a participant (initiator or receiver)
        if user_id_str not in [relation.initiator_user_id, relation.receiver_user_id]:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Permission checks: only initiator can cancel
        if payload.status == "canceled":
            is_initiator = await verify_transaction_initiator(session, transaction_id, user_id_str)
            if not is_initiator:
                raise HTTPException(status_code=403, detail="Only initiator can cancel the transaction")
        
        # Permission checks: only receiver can accept or reject
        elif payload.status in ["accepted", "rejected"]:
            is_receiver = await verify_transaction_receiver(session, transaction_id, user_id_str)
            if not is_receiver:
                raise HTTPException(status_code=403, detail="Only receiver can accept or reject the transaction")
        
        update_req = UpdateStatusRequest(
            status=UpdateStatusRequestStatus(payload.status)
        )
        
        transaction_result = await update_transaction_transactions_transaction_id_put.asyncio(
            client=get_transaction_client(),
            transaction_id=transaction_id,
            body=update_req
        )
        
        if not transaction_result:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return TransactionRes(
            transaction_id=transaction_result.transaction_id,
            requested_item_id=relation.requested_item_id,
            initiator_user_id=relation.initiator_user_id,
            receiver_user_id=relation.receiver_user_id,
            type=transaction_result.type_.value,
            offered_item_id=relation.offered_item_id,
            offered_price=transaction_result.offered_price if transaction_result.offered_price else None,
            status=transaction_result.status.value,
            message=transaction_result.message if transaction_result.message else None,
            created_at=transaction_result.created_at,
            updated_at=transaction_result.updated_at,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@transaction_user_item_router.delete("/transactions/{transaction_id}", response_model=TransactionRes)
async def delete_transaction(
    transaction_id: str,
    session: SessionDep,
    token: HTTPAuthorizationCredentials = Depends(security)
):
    """Delete a transaction."""
    try:
        user_uuid = get_user_id_from_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        user_id_str = str(user_uuid)
        
        # Parallel execution: fetch transaction, relation, and verify permission simultaneously
        transaction_result, relation, is_initiator = await asyncio.gather(
            get_transaction_transactions_transaction_id_get.asyncio(
                client=get_transaction_client(),
                transaction_id=transaction_id
            ),
            get_transaction_relation(session, transaction_id),
            verify_transaction_initiator(session, transaction_id, user_id_str)
        )
        
        if not transaction_result:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Permission check: only initiator can delete
        if not is_initiator:
            raise HTTPException(status_code=403, detail="Only initiator can delete the transaction")
        
        return_data = TransactionRes(
            transaction_id=transaction_result.transaction_id,
            requested_item_id=relation.requested_item_id,
            initiator_user_id=relation.initiator_user_id,
            receiver_user_id=relation.receiver_user_id,
            type=transaction_result.type_.value,
            offered_item_id=relation.offered_item_id,
            offered_price=transaction_result.offered_price if transaction_result.offered_price else None,
            status=transaction_result.status.value,
            message=transaction_result.message if transaction_result.message else None,
            created_at=transaction_result.created_at,
            updated_at=transaction_result.updated_at,
        )
        
        await delete_transaction_relation(session, transaction_id)
        
        await delete_transaction_transactions_transaction_id_delete.asyncio(
            client=get_transaction_client(),
            transaction_id=transaction_id
        )
        
        return return_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
