__all__ = [
    'create_new_task',
    'get_all_tasks',
    'get_task_details',
    'update_task',
]

from todos.crud.create import create_new_task
from todos.crud.read import get_all_tasks, get_task_details
from todos.crud.update import update_task
