import logging
from dataclasses import asdict
from http import HTTPStatus

from sanic.request import Request
from sanic.response import json

from . import extractors
from .middlewares.caching import cache
from .middlewares.querycheck import query_checker


@cache
async def recents(_):
    try:
        recent_downloads = await extractors.recents.get_recent_downloads()
    except Exception as err:
        logging.error("loading recents", err)
        return json(
            body={"error": "failed to load recent downloads"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    response = json([asdict(r) for r in recent_downloads])
    return response


@query_checker(["q"])
@cache
async def search(request: Request, q: str):
    language = request.args.get("lang", "")
    extension = request.args.get("ext", "")
    order_by = request.args.get("sort", "")
    try:
        result = await extractors.search.get_search_results(
            query=q,
            language=language,
            file_type=extractors.search.FileType(extension),
            order_by=extractors.search.OrderBy(order_by),
        )
    except Exception as err:
        logging.error("searching", err)
        return json(
            body={"error": "failed to load search results"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    response = json([asdict(r) for r in result])
    return response


@query_checker(["path"])
@cache
async def download(_, path: str):
    try:
        download_data = await extractors.download.get_download(path)
    except Exception as err:
        logging.error("loading download information", err)
        return json(
            body={"error": "failed to load download data"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    return json(asdict(download_data))
