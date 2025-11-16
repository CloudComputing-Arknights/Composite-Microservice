from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.transaction_status import TransactionStatus
from ..models.transaction_type import TransactionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Transaction")


@_attrs_define
class Transaction:
    """
    Attributes:
        transaction_id (str): The unique identifier for the transaction (UUID). Example:
            550e8400-e29b-41d4-a716-446655440000.
        type_ (TransactionType): The transaction type. Example: trade.
        status (TransactionStatus): The current status of the transaction. Example: pending.
        created_at (datetime.datetime): The timestamp when the transaction was created. Example: 2023-01-01T00:00:00.
        updated_at (datetime.datetime): The timestamp when the transaction was last updated. Example:
            2023-01-01T00:00:00.
        offered_price (float | None | Unset): Optional offered price when type is purchase. Example: 25.5.
        message (None | str | Unset): Optional message attached to the transaction. Example: Can we meet this weekend?.
    """

    transaction_id: str
    type_: TransactionType
    status: TransactionStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    offered_price: float | None | Unset = UNSET
    message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        transaction_id = self.transaction_id

        type_ = self.type_.value

        status = self.status.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        offered_price: float | None | Unset
        if isinstance(self.offered_price, Unset):
            offered_price = UNSET
        else:
            offered_price = self.offered_price

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transaction_id": transaction_id,
                "type": type_,
                "status": status,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if offered_price is not UNSET:
            field_dict["offered_price"] = offered_price
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        transaction_id = d.pop("transaction_id")

        type_ = TransactionType(d.pop("type"))

        status = TransactionStatus(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_offered_price(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        offered_price = _parse_offered_price(d.pop("offered_price", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        transaction = cls(
            transaction_id=transaction_id,
            type_=type_,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            offered_price=offered_price,
            message=message,
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
