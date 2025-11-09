from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="JobRead")


@_attrs_define
class JobRead:
    """
    Attributes:
        job_uuid (UUID):
        status (JobStatus):
        item_uuid (None | Unset | UUID):
        error_message (None | str | Unset):
    """

    job_uuid: UUID
    status: JobStatus
    item_uuid: None | Unset | UUID = UNSET
    error_message: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_uuid = str(self.job_uuid)

        status = self.status.value

        item_uuid: None | str | Unset
        if isinstance(self.item_uuid, Unset):
            item_uuid = UNSET
        elif isinstance(self.item_uuid, UUID):
            item_uuid = str(self.item_uuid)
        else:
            item_uuid = self.item_uuid

        error_message: None | str | Unset
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_UUID": job_uuid,
                "status": status,
            }
        )
        if item_uuid is not UNSET:
            field_dict["item_UUID"] = item_uuid
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_uuid = UUID(d.pop("job_UUID"))

        status = JobStatus(d.pop("status"))

        def _parse_item_uuid(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                item_uuid_type_0 = UUID(data)

                return item_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        item_uuid = _parse_item_uuid(d.pop("item_UUID", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        job_read = cls(
            job_uuid=job_uuid,
            status=status,
            item_uuid=item_uuid,
            error_message=error_message,
        )

        job_read.additional_properties = d
        return job_read

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
