from functools import wraps
from http import HTTPStatus
from typing import List

from sanic.request import Request
from sanic.response import HTTPResponse, json


def query_checker(queries: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs) -> HTTPResponse:
            for query in queries:
                kwargs[query] = request.args.get(query)
                if kwargs[query] is None:
                    return json(
                        {"error": f"query missing: {query}"},
                        status=HTTPStatus.BAD_REQUEST,
                    )
            response = await func(request, *args, **kwargs)
            return response

        return wrapper

    return decorator
