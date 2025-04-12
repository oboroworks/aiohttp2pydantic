from functools import wraps
from pydantic import BaseModel
from typing import Type, TypeVar
from aiohttp import web

T = TypeVar("T", bound=BaseModel)

class PydanticAiohttpRequest:
    def __init__(self, request: web.Request, data: T):
        self.request = request
        self.data = data

def aiohttp_to_pydantic(model: Type[BaseModel]):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(request: web.Request):
            payload = await request.json()
            validated = model(**payload)
            pyd_request = PydanticAiohttpRequest(request, validated)
            return await handler(pyd_request)

        return wrapper
    return decorator