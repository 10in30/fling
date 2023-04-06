from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.add_data_fling_id_add_post_response_add_data_fling_id_add_post import (
    AddDataFlingIdAddPostResponseAddDataFlingIdAddPost,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    fling_id: str,
    *,
    client: Client,
    key: str,
    val: str,
) -> Dict[str, Any]:
    url = "{}/{fling_id}/add".format(client.base_url, fling_id=fling_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["key"] = key

    params["val"] = val

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AddDataFlingIdAddPostResponseAddDataFlingIdAddPost.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    fling_id: str,
    *,
    client: Client,
    key: str,
    val: str,
) -> Response[Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]]:
    """Add Data

    Args:
        fling_id (str):
        key (str):
        val (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        fling_id=fling_id,
        client=client,
        key=key,
        val=val,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    fling_id: str,
    *,
    client: Client,
    key: str,
    val: str,
) -> Optional[Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]]:
    """Add Data

    Args:
        fling_id (str):
        key (str):
        val (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]
    """

    return sync_detailed(
        fling_id=fling_id,
        client=client,
        key=key,
        val=val,
    ).parsed


async def asyncio_detailed(
    fling_id: str,
    *,
    client: Client,
    key: str,
    val: str,
) -> Response[Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]]:
    """Add Data

    Args:
        fling_id (str):
        key (str):
        val (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        fling_id=fling_id,
        client=client,
        key=key,
        val=val,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    fling_id: str,
    *,
    client: Client,
    key: str,
    val: str,
) -> Optional[Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]]:
    """Add Data

    Args:
        fling_id (str):
        key (str):
        val (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddDataFlingIdAddPostResponseAddDataFlingIdAddPost, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            fling_id=fling_id,
            client=client,
            key=key,
            val=val,
        )
    ).parsed
