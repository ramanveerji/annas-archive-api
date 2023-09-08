import os
from json import loads as json_load

from .. import FRONT_PAGE
from ..models.response import RecentDownload
from ..utils import http_get


async def get_recent_downloads() -> list[RecentDownload]:
    response = await http_get(os.path.join(FRONT_PAGE, "dyn/recent_downloads/"))
    data = json_load(response.text)
    return [
        RecentDownload(title=i["title"], url=os.path.join(FRONT_PAGE, i["path"]))
        for i in data
    ]
