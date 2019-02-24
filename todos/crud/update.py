import datetime
import http
import json
import logging

import pytz

from todos import db
from todos.common import exceptions, parameters, responses
from todos.db import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def update_task(event: dict, _context: dict) -> dict:
    try:
        _update_task(event)
    except (exceptions.MissingParameter, exceptions.WrongParameterValueType, exceptions.TaskNotFound) as error:
        return responses.http_response(http.HTTPStatus.BAD_REQUEST, {'message': error.message})
    except Exception as error:
        logger.error('Error during updating task: "%s"', error)
        return responses.http_response(http.HTTPStatus.SERVICE_UNAVAILABLE)
    else:
        return responses.http_response(http.HTTPStatus.OK)


def _update_task(event: dict) -> None:
    task_id = parameters.get_task_id_from_path(event['pathParameters'])
    body = json.loads(event['body'])
    session = db.get_session()
    result = session.query(models.Task).filter(models.Task.id == task_id).update(_get_values_to_update(body))
    if not result:
        raise exceptions.TaskNotFound(task_id)
    session.commit()


def _get_values_to_update(body: dict) -> dict:
    values = {'updated_at': datetime.datetime.now(tz=pytz.UTC)}
    task_name = parameters.get_task_name_from_body(body, required=False)
    if task_name:
        values['name'] = task_name
    task_description = parameters.get_task_description_from_body(body, required=False)
    if task_description:
        values['description'] = task_description
    task_priority = parameters.get_task_priority_from_body(body, required=False)
    if task_priority:
        values['priority'] = task_priority
    return values
