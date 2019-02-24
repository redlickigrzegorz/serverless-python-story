import copy
import http
import json
from unittest import mock

import pytest
from sqlalchemy import orm

from todos import crud, db
from todos.db import models
from todos.db.models import task


@pytest.fixture()
def exemplary_event_body(exemplary_task_name: str, exemplary_task_description: str) -> dict:
    return {'name': exemplary_task_name, 'description': exemplary_task_description, 'priority': task.Priority.HIGH.name}


@pytest.fixture()
def exemplary_event(exemplary_headers_with_access_token: dict, exemplary_event_body: dict) -> dict:
    return {'headers': exemplary_headers_with_access_token, 'body': json.dumps(exemplary_event_body)}


@pytest.mark.usefixtures('exemplary_access_token')
def test_should_return_unauthorized_when_access_token_is_missing() -> None:
    response = crud.create_new_task({}, {})
    assert response['statusCode'] == http.HTTPStatus.UNAUTHORIZED
    assert response['body'] is None


def test_should_successfully_create_new_task(
        dbsession: orm.Session, exemplary_event_body: dict, exemplary_event: dict
) -> None:
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.create_new_task(exemplary_event, {})
    assert response['statusCode'] == http.HTTPStatus.CREATED
    assert response['body'] is None

    query = dbsession.query(models.Task).filter(
        (models.Task.name == exemplary_event_body['name']) &
        (models.Task.description == exemplary_event_body['description']) &
        (models.Task.priority == exemplary_event_body['priority'])
    )
    assert dbsession.query(query.exists()).scalar()


def test_should_return_bad_request_when_name_is_missing(
        dbsession: orm.Session, exemplary_headers_with_access_token: dict, exemplary_event_body: dict
) -> None:
    event_body = copy.deepcopy(exemplary_event_body)
    event_body.pop('name')
    event = {'headers': exemplary_headers_with_access_token, 'body': json.dumps(event_body)}
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.create_new_task(event, {})
    assert response['statusCode'] == http.HTTPStatus.BAD_REQUEST


def test_should_return_bad_request_when_description_is_missing(
        dbsession: orm.Session, exemplary_headers_with_access_token: dict, exemplary_event_body: dict
) -> None:
    event_body = copy.deepcopy(exemplary_event_body)
    event_body.pop('description')
    event = {'headers': exemplary_headers_with_access_token, 'body': json.dumps(event_body)}
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.create_new_task(event, {})
    assert response['statusCode'] == http.HTTPStatus.BAD_REQUEST


def test_should_return_bad_request_when_priority_is_not_proper(
        dbsession: orm.Session, exemplary_headers_with_access_token: dict, exemplary_event_body: dict
) -> None:
    event_body = copy.deepcopy(exemplary_event_body)
    event_body['priority'] = 'not_proper_priority'
    event = {'headers': exemplary_headers_with_access_token, 'body': json.dumps(event_body)}
    with mock.patch.object(db, 'get_session', return_value=dbsession):
        response = crud.create_new_task(event, {})
    assert response['statusCode'] == http.HTTPStatus.BAD_REQUEST


def test_should_return_service_unavailable_when_unexpected_error_occurs(exemplary_event: dict) -> None:
    with mock.patch.object(db, 'get_session', side_effect=Exception()):
        response = crud.create_new_task(exemplary_event, {})
    assert response['statusCode'] == http.HTTPStatus.SERVICE_UNAVAILABLE
    assert response['body'] is None
