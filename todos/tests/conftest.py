import pytest


@pytest.fixture()
def exemplary_task_id() -> int:
    return 999


@pytest.fixture()
def exemplary_task_name() -> str:
    return 'to do something'


@pytest.fixture()
def exemplary_task_description() -> str:
    return 'very important task'
