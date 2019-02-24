import typing

from todos.common import exceptions
from todos.db.models import task


def get_task_name_from_body(body: dict, required: bool = True) -> typing.Optional[str]:
    return _get_body_attribute(body, "name", required)


def get_task_description_from_body(body: dict, required: bool = True) -> typing.Optional[str]:
    return _get_body_attribute(body, "description", required)


def get_task_priority_from_body(body: dict, required: bool = True) -> typing.Optional[task.Priority]:
    priority = _get_body_attribute(body, "priority", required)
    try:
        return getattr(task.Priority, priority) if priority is not None else priority
    except AttributeError:
        raise exceptions.WrongParameterValueType("priority")


def _get_body_attribute(body: dict, parameter: str, required: bool = True) -> typing.Optional[str]:
    value = body.get(parameter)
    if value or not required:
        return str(value) if value is not None else value
    raise exceptions.MissingParameter(parameter)


def get_task_id_from_path(path_parameters: dict) -> int:
    try:
        return int(path_parameters["task_id"])
    except KeyError:
        raise exceptions.MissingParameter("task_id")
    except ValueError:
        raise exceptions.WrongParameterValueType("task_id")
