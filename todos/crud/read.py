import http
import logging

from sqlalchemy import orm

from todos import auth, db
from todos.db import models
from todos import serializers
from todos.common import exceptions, parameters, responses

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@auth.require_access_token
def get_all_tasks(_event: dict, _context: dict) -> dict:
    try:
        session = db.get_session()
        tasks = session.query(models.Task).all()
    except Exception as error:
        logger.error('Error during getting all tasks: "%s"', error)
        return responses.http_response(http.HTTPStatus.SERVICE_UNAVAILABLE)
    else:
        return responses.http_response(http.HTTPStatus.OK, serializers.serialize_tasks(tasks))


@auth.require_access_token
def get_task_details(event: dict, _context: dict) -> dict:
    try:
        task = _get_task_details(event)
    except (exceptions.MissingParameter, exceptions.WrongParameterValueType, exceptions.TaskNotFound) as error:
        return responses.http_response(http.HTTPStatus.BAD_REQUEST, {"message": error.message})
    except Exception as error:
        logger.error('Error during getting all tasks: "%s"', error)
        return responses.http_response(http.HTTPStatus.SERVICE_UNAVAILABLE)
    else:
        return responses.http_response(http.HTTPStatus.OK, serializers.serialize_task(task))


def _get_task_details(event: dict) -> models.Task:
    task_id = parameters.get_task_id_from_path(event["pathParameters"])
    try:
        session = db.get_session()
        return session.query(models.Task).filter(models.Task.id == task_id).one()
    except orm.exc.NoResultFound:
        raise exceptions.TaskNotFound(task_id)
