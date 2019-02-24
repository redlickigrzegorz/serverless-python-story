import http
import json
from unittest import mock

import pytest
from sqlalchemy import orm

from todos import crud, db, serializers
from todos.db import models


@pytest.fixture()
def exemplary_event_path_parameters(exemplary_task_model: models.Task) -> dict:
    return {'task_id': exemplary_task_model.id}


@pytest.fixture()
def exemplary_event(exemplary_event_path_parameters: dict) -> dict:
    return {'pathParameters': exemplary_event_path_parameters}


def test_should_successfully_return_task_details(
        dbsession: orm.Session, exemplary_event: dict, exemplary_task_model: models.Task
) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.get_task_details(exemplary_event, {})
    assert response['statusCode'] == http.HTTPStatus.OK
    assert response['body'] == json.dumps(serializers.serialize_task(exemplary_task_model))


def test_should_return_bad_request_when_task_not_found(dbsession: orm.Session) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.get_task_details({'pathParameters': {'task_id': 999}}, {})
    assert response['statusCode'] == http.HTTPStatus.BAD_REQUEST


def test_should_return_service_unavailable_when_unexpected_error_occurs(exemplary_event: dict) -> None:
    with mock.patch.object(db, 'get_session', side_effect=Exception()):
        response = crud.get_task_details(exemplary_event, {})
    assert response['statusCode'] == http.HTTPStatus.SERVICE_UNAVAILABLE
    assert response['body'] is None
