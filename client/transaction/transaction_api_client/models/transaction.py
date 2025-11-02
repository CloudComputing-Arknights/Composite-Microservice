from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.transaction_status import TransactionStatus

T = TypeVar("T", bound="Transaction")


@_attrs_define
class Transaction:
    """
    Attributes:
        transaction_id (int): The unique identifier for the transaction. Example: 5.
        item_id (int): The ID of the item being requested by the initiator. Example: 8.
        initiator_user_id (str): The ID of the user who started the transaction. Example: 4.
        receiver_user_id (str): The ID of the user who owns the requested item. Example: 6.
        status (TransactionStatus): The current status of the transaction. Example: pending.
        created_at (datetime.datetime): The timestamp when the transaction was created. Example: 2023-01-01T00:00:00.
        updated_at (datetime.datetime): The timestamp when the transaction was last updated. Example:
            2023-01-01T00:00:00.
    """

    transaction_id: int
    item_id: int
    initiator_user_id: str
    receiver_user_id: str
    status: TransactionStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transaction_id = self.transaction_id

        item_id = self.item_id

        initiator_user_id = self.initiator_user_id

        receiver_user_id = self.receiver_user_id

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transactionId": transaction_id,
                "itemId": item_id,
                "initiatorUserId": initiator_user_id,
                "receiverUserId": receiver_user_id,
                "status": status,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transaction_id = d.pop("transactionId")

        item_id = d.pop("itemId")

        initiator_user_id = d.pop("initiatorUserId")

        receiver_user_id = d.pop("receiverUserId")

        status = TransactionStatus(d.pop("status"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        transaction = cls(
            transaction_id=transaction_id,
            item_id=item_id,
            initiator_user_id=initiator_user_id,
            receiver_user_id=receiver_user_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

        transaction.additional_properties = d
        return transaction

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
