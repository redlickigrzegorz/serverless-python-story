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


def test_should_successfully_mark_task_as_completed(
        dbsession: orm.Session,
        time_to_freeze: datetime.datetime,
        exemplary_task_model: models.Task,
        exemplary_event_path_parameters,
) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        with freezegun.freeze_time(time_to_freeze):
            response = crud.complete_task({'pathParameters': exemplary_event_path_parameters}, {})
    assert response['statusCode'] == http.HTTPStatus.OK
    assert response['body'] is None

    query = dbsession.query(models.Task).filter(
        (models.Task.id == exemplary_task_model.id) &
        (models.Task.updated_at == time_to_freeze) &
        (models.Task.completed_at == time_to_freeze)
    )
    assert dbsession.query(query.exists()).scalar()


def test_should_return_bad_request_when_task_not_found(dbsession: orm.Session) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.complete_task({'pathParameters': {'task_id': 999}}, {})
    assert response['statusCode'] == http.HTTPStatus.BAD_REQUEST


def test_should_return_service_unavailable_when_unexpected_error_occurs() -> None:
    with mock.patch.object(db, 'get_session', side_effect=Exception()):
        response = crud.complete_task({'pathParameters': {'task_id': 999}}, {})
    assert response['statusCode'] == http.HTTPStatus.SERVICE_UNAVAILABLE
    assert response['body'] is None
