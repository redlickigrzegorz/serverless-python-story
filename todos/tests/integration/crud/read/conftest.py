import datetime
import typing

import pytest
from sqlalchemy import orm

from todos.db import models
from todos.db.models import task


@pytest.fixture()
def exemplary_task_model_list(dbsession: orm.Session) -> typing.List[models.Task]:
    exemplary_tasks = []
    for priority in task.Priority:
        exemplary_tasks.append(models.Task(name=f"Exemplary {priority.name} task", priority=priority))
    dbsession.add_all(exemplary_tasks)
    dbsession.flush()
    return exemplary_tasks


@pytest.fixture()
def exemplary_completed_task_model_list(
    dbsession: orm.Session, time_to_freeze: datetime.datetime
) -> typing.List[models.Task]:
    exemplary_tasks = []
    for priority in task.Priority:
        exemplary_tasks.append(
            models.Task(
                name=f"Exemplary completed {priority.name} task", priority=priority, completed_at=time_to_freeze
            )
        )
    dbsession.add_all(exemplary_tasks)
    dbsession.flush()
    return exemplary_tasks
