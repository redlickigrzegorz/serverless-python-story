import pytest
from sqlalchemy import orm

from todos.db import models
from todos.db.models import task


@pytest.fixture()
def exemplary_task_model(
        dbsession: orm.Session, exemplary_task_name: str, exemplary_task_description: str
) -> models.Task:
    exemplary_task = models.Task(
        name=exemplary_task_name,
        description=exemplary_task_description,
        priority=task.Priority.HIGH,
    )
    dbsession.add(exemplary_task)
    dbsession.flush()
    return exemplary_task
