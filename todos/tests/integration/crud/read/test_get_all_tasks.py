import http
import json
import typing
from unittest import mock

from sqlalchemy import orm

from todos import crud, db, serializers
from todos.db import models


def test_should_successfully_return_list_of_tasks(
        dbsession: orm.Session, exemplary_task_model_list: typing.List[models.Task]
) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.get_all_tasks({}, {})
    assert response['statusCode'] == http.HTTPStatus.OK
    assert response['body'] == json.dumps(serializers.serialize_tasks(exemplary_task_model_list))


def test_should_return_empty_list_when_no_tasks(dbsession: orm.Session) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.get_all_tasks({}, {})
    assert response['statusCode'] == http.HTTPStatus.OK
    assert response['body'] == json.dumps([])


def test_should_return_service_unavailable_when_unexpected_error_occurs() -> None:
    with mock.patch.object(db, 'get_session', side_effect=Exception()):
        response = crud.get_all_tasks({}, {})
    assert response['statusCode'] == http.HTTPStatus.SERVICE_UNAVAILABLE
    assert response['body'] is None
