import os

from bs4 import BeautifulSoup, Tag

from .. import FRONT_PAGE
from ..models.args import FileType, Language, OrderBy
from ..models.response import SearchResult
from ..utils import http_get
from .generic import extract_file_info, extract_publish_info


async def get_search_results(
    query: str,
    language: Language = Language.ANY,
    file_type: FileType = FileType.ANY,
    order_by: OrderBy = OrderBy.MOST_RELEVANT,
) -> list[SearchResult]:
    response = await http_get(
        url=os.path.join(FRONT_PAGE, "search"),
        params={
            "q": query,
            "lang": language,
            "ext": file_type.value,
            "sort": order_by.value,
        },
    )
    html = response.text.replace("<!--", "").replace("-->", "")
    soup = BeautifulSoup(html, "lxml")
    raw_results = soup.find_all("a", class_="js-vim-focus")
    results = list(map(parse_result, raw_results))
    return [i for i in results if i is not None]


def parse_result(raw_content: Tag) -> SearchResult | None:
    try:
        title = raw_content.find("h3").text.strip()
    except:
        return None
    authors = raw_content.find("div", class_="truncate italic").text

    publish_info = raw_content.find("div", class_="truncate text-sm").text
    publisher, publish_date = extract_publish_info(publish_info)

    thumbnail = raw_content.find("img").get("src") or None
    path = raw_content.get("href")

    raw_file_info = raw_content.find(
        "div", class_="truncate text-xs text-gray-500"
    ).text
    file_info = extract_file_info(raw_file_info)

    return SearchResult(
        title, authors, publisher, publish_date, thumbnail, path, file_info
    )
