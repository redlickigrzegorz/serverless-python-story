import typing

from todos.db import models


def serialize_tasks(tasks: typing.List[models.Task]) -> typing.List[dict]:
    return [serialize_task(task) for task in tasks]


def serialize_task(task: models.Task) -> dict:
    return {
        "id": task.id,
        "name": task.name,
        "description": task.description,
        "priority": task.priority.name,
        "created_at": int(task.created_at.timestamp()),
        "completed": bool(task.completed_at),
    }
