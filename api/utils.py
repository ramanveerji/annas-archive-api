from dataclasses import dataclass

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag


@dataclass(slots=True)
class Response:
    status_code: int
    text: str


class HTTPFailed(Exception):
    pass


async def http_get(url: str, params: dict = {}) -> Response:
    async with ClientSession() as session:
        response = await session.get(
            url, params=dict(filter(lambda i: i[1] not in ("", None), params.items()))
        )
        return Response(response.status, await response.text())


async def html_parser(url: str, params: dict = {}) -> Tag:
    response = await http_get(url, params)
    if response.status_code >= 400:
        raise HTTPFailed(f"server returned http status {response.status_code}")
    text = response.text.replace("<!--", "").replace("-->", "")
    return BeautifulSoup(text, "lxml")
