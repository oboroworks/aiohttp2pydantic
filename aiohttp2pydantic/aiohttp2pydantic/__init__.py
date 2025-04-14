from functools import wraps
from typing import TypeVar, Callable, Type
from aiohttp import web
from pydantic import BaseModel, ValidationError as PydanticValidationError

T = TypeVar("T", bound=BaseModel)


class PydanticAiohttpRequest:
    def __init__(self, request: web.Request, data: T):
        self.request = request
        self.data = data


def aiohttp_to_pydantic(model: Type[T]) -> Callable:
    def decorator(handler):
        @wraps(handler)
        async def wrapper(request: web.Request):
            try:
                if request.method == 'GET':
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

            except PydanticValidationError as e:
                return web.json_response(
                    {
                        "errors": [
                            {
                                "loc": err['loc'],
                                "msg": err['msg'],
                                "type": err['type']
                            } for err in e.errors()
                        ]
                    },
                    status=400
                )

        return wrapper
    return decorator
