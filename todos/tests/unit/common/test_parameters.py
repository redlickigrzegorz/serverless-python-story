import pytest

from todos.common import exceptions, parameters
from todos.db.models import task


def test_should_successfully_return_name_from_body(exemplary_task_name: str) -> None:
    actual_name = parameters.get_task_name_from_body({'name': exemplary_task_name})
    assert actual_name == exemplary_task_name


def test_should_return_none_when_name_is_not_required() -> None:
    actual_name = parameters.get_task_name_from_body({}, required=False)
    assert actual_name is None


def test_should_raise_missing_parameter_when_name_is_not_present() -> None:
    with pytest.raises(exceptions.MissingParameter):
        parameters.get_task_name_from_body({})


def test_should_successfully_return_description_from_body(exemplary_task_description: str) -> None:
    actual_description = parameters.get_task_description_from_body({'description': exemplary_task_description})
    assert actual_description == exemplary_task_description


def test_should_return_none_when_description_is_not_required() -> None:
    actual_description = parameters.get_task_description_from_body({}, required=False)
    assert actual_description is None


def test_should_raise_missing_parameter_when_description_is_not_present() -> None:
    with pytest.raises(exceptions.MissingParameter):
        parameters.get_task_description_from_body({})


def test_should_successfully_return_priority_from_body() -> None:
    actual_priority = parameters.get_task_priority_from_body({'priority': task.Priority.HIGH.name})
    assert actual_priority == task.Priority.HIGH


def test_should_return_none_when_priority_is_not_required() -> None:
    actual_priority = parameters.get_task_priority_from_body({}, required=False)
    assert actual_priority is None


def test_should_raise_missing_parameter_when_priority_is_not_present() -> None:
    with pytest.raises(exceptions.MissingParameter):
        parameters.get_task_priority_from_body({})


def test_should_raise_wrong_value_type_when_priority_is_not_proper() -> None:
    with pytest.raises(exceptions.WrongParameterValueType):
        parameters.get_task_priority_from_body({'priority': 'not_proper_prioritu'})
