from http import HTTPStatus
from typing import Any, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.thread_create import ThreadCreate
from ...models.thread_read import ThreadRead
from typing import cast



def _get_kwargs(
    *,
    body: ThreadCreate,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/threads/",
    }

    _kwargs["json"] = body.to_dict()


    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> HTTPValidationError | ThreadRead | None:
    if response.status_code == 201:
        response_201 = ThreadRead.from_dict(response.json())



        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())



        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[HTTPValidationError | ThreadRead]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ThreadCreate,

) -> Response[HTTPValidationError | ThreadRead]:
    """ Create Thread

    Args:
        body (ThreadCreate):  Example: {'author_id': 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
            'participant_id': 'bb12cc34-dd56-ee78-9900-aabbccddeeff'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ThreadRead]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ThreadCreate,

) -> HTTPValidationError | ThreadRead | None:
    """ Create Thread

    Args:
        body (ThreadCreate):  Example: {'author_id': 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
            'participant_id': 'bb12cc34-dd56-ee78-9900-aabbccddeeff'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ThreadRead
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ThreadCreate,

) -> Response[HTTPValidationError | ThreadRead]:
    """ Create Thread

    Args:
        body (ThreadCreate):  Example: {'author_id': 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
            'participant_id': 'bb12cc34-dd56-ee78-9900-aabbccddeeff'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ThreadRead]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ThreadCreate,

) -> HTTPValidationError | ThreadRead | None:
    """ Create Thread

    Args:
        body (ThreadCreate):  Example: {'author_id': 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
            'participant_id': 'bb12cc34-dd56-ee78-9900-aabbccddeeff'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ThreadRead
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
