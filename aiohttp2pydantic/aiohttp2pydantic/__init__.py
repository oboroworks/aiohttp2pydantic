from functools import wraps
from pydantic import BaseModel
from typing import Type
from aiohttp import web

from typing import TypeVar, Callable

T = TypeVar("T", bound=BaseModel)


class PydanticAiohttpRequest:
    def __init__(self, request: web.Request, data: Type[T]):
        self.request = request
        self.data = data


def aiohttp_to_pydantic(model: Type[T]) -> Callable:
    def decorator(handler):
        @wraps(handler)
        async def wrapper(request: web.Request):
            method = request.method
            if method == 'GET':
                data = dict(request.query)
            elif request.content_type == 'application/json':
                data = await request.json()
            elif request.content_type == 'application/x-www-form-urlencoded':
                data = await request.post()
            else:
                data = await request.read()  # fallback

            validated = model(**data)
            pyd_request = PydanticAiohttpRequest(request, validated)
            return await handler(pyd_request)

        return wrapper
    return decorator