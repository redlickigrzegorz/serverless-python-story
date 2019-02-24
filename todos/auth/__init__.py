import functools
import http
import os
import typing

from todos.common import responses


def require_access_token(fun: typing.Callable) -> typing.Callable:

    @functools.wraps(fun)
    def wrapped(event: dict, context: dict) -> dict:
        access_token = event.get('headers', {}).get('X-access-token')
        if access_token != os.environ['ACCESS_TOKEN']:
            return responses.http_response(http.HTTPStatus.UNAUTHORIZED)
        return fun(event, context)
    return wrapped
