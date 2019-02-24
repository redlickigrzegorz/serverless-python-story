import json
import typing


def http_response(status_code: int, body: typing.Optional[typing.Union[dict, list]] = None) -> dict:
    return {
        'statusCode': status_code,
        'headers': {'content-type': 'application/json'},
        'body': json.dumps(body) if body is not None else body,
    }
