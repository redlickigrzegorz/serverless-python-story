import datetime
import http
import json
from unittest import mock

import freezegun
import pytest
from sqlalchemy import orm

from todos import crud, db
from todos.db import models
from todos.db.models import task


@pytest.fixture()
def exemplary_changed_task_name() -> str:
    return "changed task name"


@pytest.fixture()
def exemplary_changed_task_description() -> str:
    return "changed task description"


@pytest.fixture()
def exemplary_event_path_parameters(exemplary_task_model: models.Task) -> dict:
    return {"task_id": exemplary_task_model.id}


@pytest.mark.usefixtures("exemplary_access_token")
def test_should_return_unauthorized_when_access_token_is_missing() -> None:
    response = crud.update_task({}, {})
    assert response["statusCode"] == http.HTTPStatus.UNAUTHORIZED
    assert response["body"] is None


def test_should_successfully_update_task_name(
    dbsession: orm.Session,
    time_to_freeze: datetime.datetime,
    exemplary_changed_task_name: str,
    exemplary_task_description: str,
    exemplary_headers_with_access_token: dict,
    exemplary_event_path_parameters: dict,
) -> None:
    event = {
        "headers": exemplary_headers_with_access_token,
        "body": json.dumps({"name": exemplary_changed_task_name}),
        "pathParameters": exemplary_event_path_parameters,
    }
    with mock.patch.object(db, "get_session", return_value=dbsession):
        with freezegun.freeze_time(time_to_freeze):
            response = crud.update_task(event, {})
    assert response["statusCode"] == http.HTTPStatus.OK
    assert response["body"] is None

    query = dbsession.query(models.Task).filter(
        (models.Task.name == exemplary_changed_task_name)
        & (models.Task.description == exemplary_task_description)
        & (models.Task.priority == task.Priority.HIGH)
        & (models.Task.updated_at == time_to_freeze)
    )
    assert dbsession.query(query.exists()).scalar()


def test_should_successfully_update_task_description(
    dbsession: orm.Session,
    time_to_freeze: datetime.datetime,
    exemplary_task_name: str,
    exemplary_changed_task_description: str,
    exemplary_headers_with_access_token: dict,
    exemplary_event_path_parameters: dict,
) -> None:
    event = {
        "headers": exemplary_headers_with_access_token,
        "body": json.dumps({"description": exemplary_changed_task_description}),
        "pathParameters": exemplary_event_path_parameters,
    }
    with mock.patch.object(db, "get_session", return_value=dbsession):
        with freezegun.freeze_time(time_to_freeze):
            response = crud.update_task(event, {})
    assert response["statusCode"] == http.HTTPStatus.OK
    assert response["body"] is None

    query = dbsession.query(models.Task).filter(
        (models.Task.name == exemplary_task_name)
        & (models.Task.description == exemplary_changed_task_description)
        & (models.Task.priority == task.Priority.HIGH)
        & (models.Task.updated_at == time_to_freeze)
    )
    assert dbsession.query(query.exists()).scalar()


def test_should_successfully_update_task_priority(
    dbsession: orm.Session,
    time_to_freeze: datetime.datetime,
    exemplary_task_name: str,
    exemplary_task_description: str,
    exemplary_headers_with_access_token: dict,
    exemplary_event_path_parameters: dict,
) -> None:
    event = {
        "headers": exemplary_headers_with_access_token,
        "body": json.dumps({"priority": task.Priority.LOW.name}),
        "pathParameters": exemplary_event_path_parameters,
    }
    with mock.patch.object(db, "get_session", return_value=dbsession):
        with freezegun.freeze_time(time_to_freeze):
            response = crud.update_task(event, {})
    assert response["statusCode"] == http.HTTPStatus.OK
    assert response["body"] is None

    query = dbsession.query(models.Task).filter(
        (models.Task.name == exemplary_task_name)
        & (models.Task.description == exemplary_task_description)
        & (models.Task.priority == task.Priority.LOW)
        & (models.Task.updated_at == time_to_freeze)
    )
    assert dbsession.query(query.exists()).scalar()


def test_should_return_bad_request_when_task_not_found(
    dbsession: orm.Session, exemplary_headers_with_access_token: dict
) -> None:
    event = {"headers": exemplary_headers_with_access_token, "body": json.dumps({}), "pathParameters": {"task_id": 999}}
    with mock.patch.object(db, "get_session", return_value=dbsession):
        response = crud.update_task(event, {})
    assert response["statusCode"] == http.HTTPStatus.BAD_REQUEST


def test_should_return_service_unavailable_when_unexpected_error_occurs(
    exemplary_headers_with_access_token: dict
) -> None:
    event = {"headers": exemplary_headers_with_access_token, "body": json.dumps({}), "pathParameters": {"task_id": 999}}
    with mock.patch.object(db, "get_session", side_effect=Exception()):
        response = crud.get_task_details(event, {})
    assert response["statusCode"] == http.HTTPStatus.SERVICE_UNAVAILABLE
    assert response["body"] is None
