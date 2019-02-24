import typing

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


@pytest.fixture()
def exemplary_task_model_list(dbsession: orm.Session) -> typing.List[models.Task]:
    exemplary_tasks = [models.Task(name=f'{i} task', description=f'very important {i} task') for i in range(3)]
    dbsession.add_all(exemplary_tasks)
    dbsession.flush()
    return exemplary_tasks
