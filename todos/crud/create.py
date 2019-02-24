import http
import json
import logging

from todos import auth, db
from todos.common import exceptions, parameters, responses
from todos.db import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@auth.require_access_token
def create_new_task(event: dict, _context: dict) -> dict:
    try:
        body = json.loads(event["body"])
        session = db.get_session()
        session.add(_build_task(body))
        session.commit()
    except (exceptions.MissingParameter, exceptions.WrongParameterValueType) as error:
        return responses.http_response(http.HTTPStatus.BAD_REQUEST, {"message": error.message})
    except Exception as error:
        logger.error('Error during creating new task: "%s"', error)
        return responses.http_response(http.HTTPStatus.SERVICE_UNAVAILABLE)
    else:
        return responses.http_response(http.HTTPStatus.CREATED)


def _build_task(body: dict) -> models.Task:
    return models.Task(
        name=parameters.get_task_name_from_body(body),
        description=parameters.get_task_description_from_body(body),
        priority=parameters.get_task_priority_from_body(body, required=False),
    )
