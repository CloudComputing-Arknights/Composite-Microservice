from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.message_create import MessageCreate
from ...models.message_read import MessageRead
from typing import cast
from uuid import UUID



def _get_kwargs(
    thread_id: UUID,
    *,
    body: MessageCreate,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/threads/{thread_id}/messages".format(thread_id=thread_id,),
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> HTTPValidationError | MessageRead | None:
    if response.status_code == 201:
        response_201 = MessageRead.from_dict(response.json())



        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[HTTPValidationError | MessageRead]:
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
    body: MessageCreate,

) -> Response[HTTPValidationError | MessageRead]:
    """ Send Message

    Args:
        thread_id (UUID):
        body (MessageCreate):  Example: {'content': 'Hey! Are you still selling the mirror?',
            'sender_id': '123e4567-e89b-12d3-a456-426614174000'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MessageRead]
     """


    kwargs = _get_kwargs(
        thread_id=thread_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    thread_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: MessageCreate,

) -> HTTPValidationError | MessageRead | None:
    """ Send Message

    Args:
        thread_id (UUID):
        body (MessageCreate):  Example: {'content': 'Hey! Are you still selling the mirror?',
            'sender_id': '123e4567-e89b-12d3-a456-426614174000'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MessageRead
     """


    return sync_detailed(
        thread_id=thread_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    thread_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: MessageCreate,

) -> Response[HTTPValidationError | MessageRead]:
    """ Send Message

    Args:
        thread_id (UUID):
        body (MessageCreate):  Example: {'content': 'Hey! Are you still selling the mirror?',
            'sender_id': '123e4567-e89b-12d3-a456-426614174000'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MessageRead]
     """


    kwargs = _get_kwargs(
        thread_id=thread_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    thread_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: MessageCreate,

) -> HTTPValidationError | MessageRead | None:
    """ Send Message

    Args:
        thread_id (UUID):
        body (MessageCreate):  Example: {'content': 'Hey! Are you still selling the mirror?',
            'sender_id': '123e4567-e89b-12d3-a456-426614174000'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MessageRead
     """


    return (await asyncio_detailed(
        thread_id=thread_id,
client=client,
body=body,

    )).parsed
