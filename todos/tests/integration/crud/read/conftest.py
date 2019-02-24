import typing

import pytest
from sqlalchemy import orm

from todos.db import models


@pytest.fixture()
def exemplary_task_model_list(dbsession: orm.Session) -> typing.List[models.Task]:
    exemplary_tasks = [models.Task(name=f'{i} task', description=f'very important {i} task') for i in range(3)]
    dbsession.add_all(exemplary_tasks)
    dbsession.flush()
    return exemplary_tasks
