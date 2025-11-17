from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.message_read import MessageRead
from ...types import Response


def _get_kwargs(
    thread_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/threads/{thread_id}/messages",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[MessageRead] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = MessageRead.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[MessageRead]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    thread_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[MessageRead]]:
    """Get Messages

    Args:
        thread_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[MessageRead]]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    thread_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[MessageRead] | None:
    """Get Messages

    Args:
        thread_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[MessageRead]
    """

    return sync_detailed(
        thread_id=thread_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    thread_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[MessageRead]]:
    """Get Messages

    Args:
        thread_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[MessageRead]]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thread_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[MessageRead] | None:
    """Get Messages

    Args:
        thread_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[MessageRead]
    """

    return (
        await asyncio_detailed(
            thread_id=thread_id,
            client=client,
        )
    ).parsed
