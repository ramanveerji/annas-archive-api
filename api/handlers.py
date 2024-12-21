import logging
from dataclasses import asdict
from http import HTTPStatus

from sanic.request import Request
from sanic.response import json

from . import extractors
from .middlewares.caching import cache
from .middlewares.querycheck import query_checker
from .models import args


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
    return json([asdict(r) for r in recent_downloads])


@query_checker(["q"])
@cache
async def search(request: Request, q: str):
    try:
        language = args.Language(request.args.get("lang", ""))
    except ValueError:
        return json({"error": "invalid language code"}, HTTPStatus.BAD_REQUEST)
    try:
        extension = args.FileType(request.args.get("ext", ""))
    except ValueError:
        return json({"error": "invalid file extension"}, HTTPStatus.BAD_REQUEST)
    try:
        order_by = args.OrderBy(request.args.get("sort", ""))
    except ValueError:
        return json({"error": "invalid sort mode"}, HTTPStatus.BAD_REQUEST)
    try:
        result = await extractors.search.get_search_results(
            query=q,
            language=language,
            file_type=extension,
            order_by=order_by,
        )
    except Exception as err:
        logging.error("searching", err)
        return json(
            body={"error": "failed to load search results"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    return json([asdict(r) for r in result])


@query_checker(["id"])
@cache
async def download(_, id: str):
    try:
        download_data = await extractors.download.get_download(id)
    except Exception as err:
        logging.error("loading download information", err)
        return json(
            body={"error": "failed to load download data"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    return json(asdict(download_data))
