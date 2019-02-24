import datetime
import http
import logging

import pytz

from todos import db
from todos.common import exceptions, responses, parameters
from todos.db import models

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def complete_task(event: dict, _context: dict) -> dict:
    try:
        _complete_task(event)
    except (exceptions.MissingParameter, exceptions.WrongParameterValueType, exceptions.TaskNotFound) as error:
        return responses.http_response(http.HTTPStatus.BAD_REQUEST, {'message': error.message})
    except Exception as error:
        logger.error('Error during updating task: "%s"', error)
        return responses.http_response(http.HTTPStatus.SERVICE_UNAVAILABLE)
    else:
        return responses.http_response(http.HTTPStatus.OK)


def _complete_task(event: dict) -> None:
    task_id = parameters.get_task_id_from_path(event['pathParameters'])
    session = db.get_session()
    current_date = datetime.datetime.now(tz=pytz.UTC)
    result = session.query(models.Task).filter(models.Task.id == task_id).update(
        {'updated_at': current_date, 'completed_at': current_date}
    )
    if not result:
        raise exceptions.TaskNotFound(task_id)
    session.commit()
