from fastapi import APIRouter, HTTPException, Header, status
from typing import Optional, Literal
from sqlmodel import select

from app.models.dto.transaction_dto import (
    CreateTransactionReq,
    TransactionRes,
    UpdateTransactionStatusReq
)
from app.models.po.transaction_user_item_po import TransactionUserItem
from app.utils.db_connection import SessionDep
from app.utils.config import get_transaction_client

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

transaction_router = APIRouter()


@transaction_router.post("/transactions/transaction", response_model=TransactionRes, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: CreateTransactionReq,
    session: SessionDep,
    x_idempotency_key: Optional[str] = Header(None, alias="X-Idempotency-Key")
):
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
        
        relation = TransactionUserItem(
            transaction_id=transaction_result.transaction_id,
            initiator_user_id=payload.initiator_user_id,
            receiver_user_id=payload.receiver_user_id,
            requested_item_id=payload.requested_item_id,
            offered_item_id=payload.offered_item_id,
        )
        
        session.add(relation)
        await session.commit()
        await session.refresh(relation)
        
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
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")


@transaction_router.get("/transactions/{transaction_id}", response_model=TransactionRes)
async def get_transaction(transaction_id: str, session: SessionDep):
    try:
        transaction_result = await get_transaction_transactions_transaction_id_get.asyncio(
            client=get_transaction_client(),
            transaction_id=transaction_id
        )
        
        if not transaction_result:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        stmt = select(TransactionUserItem).where(
            TransactionUserItem.transaction_id == transaction_id
        )
        result = await session.exec(stmt)
        relation = result.first()
        
        if not relation:
            raise HTTPException(status_code=404, detail="Transaction relation not found")
        
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


@transaction_router.get("/transactions", response_model=list[TransactionRes])
async def list_transactions(
    session: SessionDep,
    status_param: Optional[Literal["pending", "accepted", "rejected", "canceled", "completed"]] = None,
    initiator_user_id: Optional[str] = None,
    receiver_user_id: Optional[str] = None,
    requested_item_id: Optional[str] = None,
    type: Optional[Literal["trade", "purchase"]] = None,
    limit: int = 50,
    offset: int = 0,
):
    try:
        stmt = select(TransactionUserItem)
        
        has_relation_filter = False
        if initiator_user_id:
            stmt = stmt.where(TransactionUserItem.initiator_user_id == initiator_user_id)
            has_relation_filter = True
        if receiver_user_id:
            stmt = stmt.where(TransactionUserItem.receiver_user_id == receiver_user_id)
            has_relation_filter = True
        if requested_item_id:
            stmt = stmt.where(TransactionUserItem.requested_item_id == requested_item_id)
            has_relation_filter = True
        
        result = await session.exec(stmt)
        relations = result.all()
        relation_map = {r.transaction_id: r for r in relations}
        
        status_param_client = None
        if status_param:
            status_param_client = ListTransactionsTransactionsGetStatusParamType0(status_param)
        
        type_client = None
        if type:
            type_client = ListTransactionsTransactionsGetTypeType0(type)
        
        transactions_result = await list_transactions_transactions_get.asyncio(
            client=get_transaction_client(),
            status_param=status_param_client,
            type_=type_client,
            limit=limit,
            offset=offset
        )
        
        if not transactions_result:
            return []
        
        combined_results = []
        for trans in transactions_result:
            if has_relation_filter and trans.transaction_id not in relation_map:
                continue
            
            if trans.transaction_id not in relation_map:
                stmt_single = select(TransactionUserItem).where(
                    TransactionUserItem.transaction_id == trans.transaction_id
                )
                result_single = await session.exec(stmt_single)
                rel = result_single.first()
                if not rel:
                    continue
                relation_map[trans.transaction_id] = rel
            
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


@transaction_router.put("/transactions/{transaction_id}", response_model=TransactionRes)
async def update_transaction(
    transaction_id: str,
    payload: UpdateTransactionStatusReq,
    session: SessionDep
):
    try:
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
        
        stmt = select(TransactionUserItem).where(
            TransactionUserItem.transaction_id == transaction_id
        )
        result = await session.exec(stmt)
        relation = result.first()
        
        if not relation:
            raise HTTPException(status_code=404, detail="Transaction relation not found")
        
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


@transaction_router.delete("/transactions/{transaction_id}", response_model=TransactionRes)
async def delete_transaction(transaction_id: str, session: SessionDep):
    try:
        transaction_result = await get_transaction_transactions_transaction_id_get.asyncio(
            client=get_transaction_client(),
            transaction_id=transaction_id
        )
        
        if not transaction_result:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        stmt = select(TransactionUserItem).where(
            TransactionUserItem.transaction_id == transaction_id
        )
        result = await session.exec(stmt)
        relation = result.first()
        
        if not relation:
            raise HTTPException(status_code=404, detail="Transaction relation not found")
        
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
        
        await session.delete(relation)
        await session.commit()
        
        await delete_transaction_transactions_transaction_id_delete.asyncio(
            client=get_transaction_client(),
            transaction_id=transaction_id
        )
        
        return return_data
        
    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
