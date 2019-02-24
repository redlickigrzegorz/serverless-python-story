import enum

import sqlalchemy as sa
from sqlalchemy.sql import sqltypes

from todos.db.models import meta


class Priority(enum.Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task(meta.Base):
    __tablename__ = "tasks"

    id = sa.Column(sqltypes.Integer, primary_key=True)
    name = sa.Column(sqltypes.String(50), nullable=False)
    description = sa.Column(sqltypes.String(255), nullable=True)
    priority = sa.Column(sqltypes.Enum(Priority), default=Priority.LOW, nullable=False)
    created_at = sa.Column(sqltypes.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    updated_at = sa.Column(sqltypes.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    completed_at = sa.Column(sqltypes.DateTime(timezone=True), nullable=True)
