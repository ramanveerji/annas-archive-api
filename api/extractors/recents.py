from html import unescape as html_unescape
from json import loads as json_load
from os import path

from .. import FRONT_PAGE
from ..models.response import RecentDownload
from ..utils import http_get


async def get_recent_downloads() -> list[RecentDownload]:
    response = await http_get(path.join(FRONT_PAGE, "dyn/recent_downloads/"))
    data = json_load(response.text)
    return [
        RecentDownload(
            title=html_unescape(item["title"]), id=item["path"].split("/md5/")[-1]
        )
        for item in data
    ]
