import http
import json
import typing
from unittest import mock

import pytest
from sqlalchemy import orm

from todos import crud, db, serializers
from todos.db import models


@pytest.fixture()
def exemplary_event(exemplary_headers_with_access_token: dict) -> dict:
    return {'headers': exemplary_headers_with_access_token}


@pytest.mark.usefixtures('exemplary_access_token')
def test_should_return_unauthorized_when_access_token_is_missing() -> None:
    response = crud.get_all_tasks({}, {})
    assert response['statusCode'] == http.HTTPStatus.UNAUTHORIZED
    assert response['body'] is None


def test_should_successfully_return_list_of_tasks(
        dbsession: orm.Session, exemplary_event: dict, exemplary_task_model_list: typing.List[models.Task]
) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.get_all_tasks(exemplary_event, {})
    assert response['statusCode'] == http.HTTPStatus.OK
    assert response['body'] == json.dumps(serializers.serialize_tasks(exemplary_task_model_list))


def test_should_return_empty_list_when_no_tasks(dbsession: orm.Session, exemplary_event: dict) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.get_all_tasks(exemplary_event, {})
    assert response['statusCode'] == http.HTTPStatus.OK
    assert response['body'] == json.dumps([])


def test_should_return_service_unavailable_when_unexpected_error_occurs(exemplary_event: dict) -> None:
    with mock.patch.object(db, 'get_session', side_effect=Exception()):
        response = crud.get_all_tasks(exemplary_event, {})
    assert response['statusCode'] == http.HTTPStatus.SERVICE_UNAVAILABLE
    assert response['body'] is None
