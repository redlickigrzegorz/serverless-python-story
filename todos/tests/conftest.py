import datetime

import pytest
import pytz


@pytest.fixture()
def exemplary_task_id() -> int:
    return 999


@pytest.fixture()
def exemplary_task_name() -> str:
    return "to do something"


@pytest.fixture()
def exemplary_task_description() -> str:
    return "very important task"


@pytest.fixture()
def time_to_freeze() -> datetime.datetime:
    return datetime.datetime(2077, 6, 6, 6, 0, 0).replace(tzinfo=pytz.UTC)
