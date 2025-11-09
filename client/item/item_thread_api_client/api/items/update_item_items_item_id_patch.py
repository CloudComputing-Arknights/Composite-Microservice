from http import HTTPStatus
from typing import Any
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.item_read import ItemRead
from ...models.item_update import ItemUpdate
from ...types import Response


def _get_kwargs(
    item_id: UUID,
    *,
    body: ItemUpdate,
    if_match: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["if-match"] = if_match

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/items/{item_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ItemRead | None:
    if response.status_code == 200:
        response_200 = ItemRead.from_dict(response.json())

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
) -> Response[HTTPValidationError | ItemRead]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    item_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ItemUpdate,
    if_match: str,
) -> Response[HTTPValidationError | ItemRead]:
    """Update Item

     Partially update an item's information.

    Args:
        item_id (UUID):
        if_match (str):
        body (ItemUpdate): Partial update for an item and its post.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ItemRead]
    """

    kwargs = _get_kwargs(
        item_id=item_id,
        body=body,
        if_match=if_match,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    item_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ItemUpdate,
    if_match: str,
) -> HTTPValidationError | ItemRead | None:
    """Update Item

     Partially update an item's information.

    Args:
        item_id (UUID):
        if_match (str):
        body (ItemUpdate): Partial update for an item and its post.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ItemRead
    """

    return sync_detailed(
        item_id=item_id,
        client=client,
        body=body,
        if_match=if_match,
    ).parsed


async def asyncio_detailed(
    item_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ItemUpdate,
    if_match: str,
) -> Response[HTTPValidationError | ItemRead]:
    """Update Item

     Partially update an item's information.

    Args:
        item_id (UUID):
        if_match (str):
        body (ItemUpdate): Partial update for an item and its post.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ItemRead]
    """

    kwargs = _get_kwargs(
        item_id=item_id,
        body=body,
        if_match=if_match,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    item_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: ItemUpdate,
    if_match: str,
) -> HTTPValidationError | ItemRead | None:
    """Update Item

     Partially update an item's information.

    Args:
        item_id (UUID):
        if_match (str):
        body (ItemUpdate): Partial update for an item and its post.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ItemRead
    """

    return (
        await asyncio_detailed(
            item_id=item_id,
            client=client,
            body=body,
            if_match=if_match,
        )
    ).parsed
