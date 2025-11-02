from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.address_read import AddressRead
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    address_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/addresses/{address_id}",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AddressRead | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = AddressRead.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AddressRead | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    address_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AddressRead | HTTPValidationError]:
    """Get Address

    Args:
        address_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddressRead | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        address_id=address_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    address_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> AddressRead | HTTPValidationError | None:
    """Get Address

    Args:
        address_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddressRead | HTTPValidationError
    """

    return sync_detailed(
        address_id=address_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    address_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AddressRead | HTTPValidationError]:
    """Get Address

    Args:
        address_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AddressRead | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        address_id=address_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    address_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> AddressRead | HTTPValidationError | None:
    """Get Address

    Args:
        address_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AddressRead | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            address_id=address_id,
            client=client,
        )
    ).parsed
