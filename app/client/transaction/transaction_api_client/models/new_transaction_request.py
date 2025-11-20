from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_transaction_request_status import NewTransactionRequestStatus
from ..models.new_transaction_request_type import NewTransactionRequestType
from ..types import UNSET, Unset

T = TypeVar("T", bound="NewTransactionRequest")


@_attrs_define
class NewTransactionRequest:
    """
    Attributes:
        type_ (NewTransactionRequestType): Transaction type. Example: trade.
        offered_price (float | None | Unset): Optional offered price when type is purchase. Example: 25.5.
        message (None | str | Unset): Optional initial message. Example: Can we meet this weekend?.
        status (NewTransactionRequestStatus | Unset): Initial status for the transaction. Default:
            NewTransactionRequestStatus.PENDING. Example: pending.
    """

    type_: NewTransactionRequestType
    offered_price: float | None | Unset = UNSET
    message: None | str | Unset = UNSET
    status: NewTransactionRequestStatus | Unset = NewTransactionRequestStatus.PENDING
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

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

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if offered_price is not UNSET:
            field_dict["offered_price"] = offered_price
        if message is not UNSET:
            field_dict["message"] = message
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = NewTransactionRequestType(d.pop("type"))

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

        _status = d.pop("status", UNSET)
        status: NewTransactionRequestStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = NewTransactionRequestStatus(_status)

        new_transaction_request = cls(
            type_=type_,
            offered_price=offered_price,
            message=message,
            status=status,
        )

        new_transaction_request.additional_properties = d
        return new_transaction_request

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
