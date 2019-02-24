import datetime
import http
from unittest import mock

import freezegun
import pytest
from sqlalchemy import orm

from todos import crud, db
from todos.db import models


@pytest.fixture()
def exemplary_event_path_parameters(exemplary_task_model: models.Task) -> dict:
    return {'task_id': exemplary_task_model.id}


@pytest.fixture()
def exemplary_event(exemplary_headers_with_access_token: dict, exemplary_event_path_parameters: dict) -> dict:
    return {'headers': exemplary_headers_with_access_token, 'pathParameters': exemplary_event_path_parameters}


@pytest.mark.usefixtures('exemplary_access_token')
def test_should_return_unauthorized_when_access_token_is_missing() -> None:
    response = crud.complete_task({}, {})
    assert response['statusCode'] == http.HTTPStatus.UNAUTHORIZED
    assert response['body'] is None


def test_should_successfully_mark_task_as_completed(
        dbsession: orm.Session,
        time_to_freeze: datetime.datetime,
        exemplary_task_model: models.Task,
        exemplary_event: dict,
) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        with freezegun.freeze_time(time_to_freeze):
            response = crud.complete_task(exemplary_event, {})
    assert response['statusCode'] == http.HTTPStatus.OK
    assert response['body'] is None

    query = dbsession.query(models.Task).filter(
        (models.Task.id == exemplary_task_model.id) &
        (models.Task.updated_at == time_to_freeze) &
        (models.Task.completed_at == time_to_freeze)
    )
    assert dbsession.query(query.exists()).scalar()


def test_should_return_bad_request_when_task_not_found(
        dbsession: orm.Session, exemplary_headers_with_access_token: dict
) -> None:
    event = {'headers': exemplary_headers_with_access_token, 'pathParameters': {'task_id': 999}}
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.complete_task(event, {})
    assert response['statusCode'] == http.HTTPStatus.BAD_REQUEST


def test_should_return_service_unavailable_when_unexpected_error_occurs(
        exemplary_headers_with_access_token: dict
) -> None:
    event = {'headers': exemplary_headers_with_access_token, 'pathParameters': {'task_id': 999}}
    with mock.patch.object(db, 'get_session', side_effect=Exception()):
        response = crud.complete_task(event, {})
    assert response['statusCode'] == http.HTTPStatus.SERVICE_UNAVAILABLE
    assert response['body'] is None
