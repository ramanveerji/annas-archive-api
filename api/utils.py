from dataclasses import dataclass

from aiohttp import ClientSession


@dataclass(slots=True)
class Response:
    status_code: int
    text: str


async def http_get(url: str, params: dict = {}) -> Response:
    session = ClientSession()
    response = await session.get(url, params=params)
    text = await response.text()
    await session.close()
    return Response(response.status, text)
