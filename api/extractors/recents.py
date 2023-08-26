from dataclasses import dataclass
from json import loads as json_load

from bs4 import BeautifulSoup, Tag

from .. import FRONT_PAGE
from ..utils import http_get


@dataclass(slots=True)
class RecentDownload:
    title: str
    url: str


async def get_recommendations() -> list[RecentDownload]:
    response = await http_get(FRONT_PAGE + '/dyn/recent_downloads/')
    data = json_load(response.text)
    return [RecentDownload(i['title'], FRONT_PAGE + i['path']) for i in data]
