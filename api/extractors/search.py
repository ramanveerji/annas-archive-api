from html import unescape as html_unescape
from urllib.parse import urljoin

from bs4 import Tag

from .. import FRONT_PAGE
from ..models.args import FileType, Language, OrderBy
from ..models.response import SearchResult
from ..utils import html_parser
from .generic import extract_file_info, extract_publish_info


async def get_search_results(
    query: str,
    language: Language = Language.ANY,
    file_type: FileType = FileType.ANY,
    order_by: OrderBy = OrderBy.MOST_RELEVANT,
) -> list[SearchResult]:
    soup = await html_parser(
        url=urljoin(FRONT_PAGE, "search"),
        params={
            "q": query,
            "lang": language.value,
            "ext": file_type.value,
            "sort": order_by.value,
        },
    )
    raw_results = soup.find_all("a", class_="js-vim-focus")
    return list(filter(lambda i: i is not None, map(parse_result, raw_results)))


def parse_result(raw_content: Tag) -> SearchResult | None:
    try:
        title = raw_content.find("h3").text.strip()
    except:
        return None
    authors = raw_content.find("div", class_="truncate italic").text

    publish_info = raw_content.find("div", class_="truncate text-sm").text
    publisher, publish_date = extract_publish_info(publish_info)

    thumbnail = raw_content.find("img").get("src") or None
    id = raw_content.get("href").split("/md5/")[-1]

    raw_file_info = raw_content.find(
        "div", class_="truncate text-xs text-gray-500"
    ).text
    file_info = extract_file_info(raw_file_info)

    return SearchResult(
        id=id,
        title=html_unescape(title),
        authors=html_unescape(authors),
        file_info=file_info,
        thumbnail=thumbnail,
        publisher=html_unescape(publisher) if publisher else None,
        publish_date=publish_date,
    )
