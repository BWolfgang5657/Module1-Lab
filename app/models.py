"""TaskFlow SQLAlchemy models — Module 04 reference solution.

Defines the TaskFlow schema as a one-to-many relationship: one ``Project`` has
many ``Task`` rows. It uses the modern **SQLAlchemy 2.x** declarative style:
``DeclarativeBase``, ``Mapped``, ``mapped_column``, and ``relationship``.

Your models *are* your schema — change the Python here and the generated SQL
follows. Importing this module does **not** touch a database; it only describes
the tables. Connecting and creating tables happens in :mod:`app.db`.

This single file collects the answers to several lab items:
  * Task 1 / 🧠 Your Turn — ``Project``/``Task`` with a foreign key + relationship.
  * Exercise A — the nullable ``due_date`` column.
  * Exercise B — the ``UNIQUE`` constraint on ``Project.name``.
  * Exercise C — the ``CHECK`` constraint restricting ``Task.priority``.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """The shared declarative base every TaskFlow model inherits from.

    ``Base.metadata`` collects every table defined below, which is what
    ``create_all`` (in :mod:`app.db`) uses to emit ``CREATE TABLE`` statements.
    """


class Project(Base):
    # ``__tablename__`` is the actual table name created in the database.
    __tablename__ = "projects"

    # Primary key: SQLAlchemy makes integer PKs auto-incrementing by default.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Exercise B — UNIQUE constraint: the database itself rejects two projects
    # with the same name. This guard lives in the DB, so no application bug can
    # bypass it. ``String(100)`` bounds the column length.
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # A timezone-aware creation timestamp. Using a lambda defers "now" to insert
    # time (not import time). ``datetime.now(timezone.utc)`` is the modern,
    # non-deprecated replacement for ``datetime.utcnow``.
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    # The "one" side of one-to-many. ``back_populates`` must name the matching
    # attribute on the other side (``Task.project``). ``cascade`` so deleting a
    # project also removes its orphaned tasks.
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Project(id={self.id!r}, name={self.name!r})"


class Task(Base):
    __tablename__ = "tasks"

    # Exercise C — a table-level CHECK constraint. The database guarantees
    # ``priority`` is always one of the allowed values; an attempt to insert
    # 'urgent' fails at the DB level, independent of any Python validation.
    __table_args__ = (
        CheckConstraint(
            "priority in ('low','medium','high')", name="ck_task_priority"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))

    # Defaults applied at the ORM level when not provided on insert.
    priority: Mapped[str] = mapped_column(String(10), default="medium")
    done: Mapped[bool] = mapped_column(default=False)

    # Exercise A — an OPTIONAL due date. ``datetime | None`` + ``nullable=True``
    # means a task can exist without a due date.
    due_date: Mapped[datetime | None] = mapped_column(nullable=True)

    # 🧠 Your Turn — the foreign key that links a task to its project.
    # ``ForeignKey("projects.id")`` references the ``projects`` table's PK.
    # It is nullable here so a task can be created before being filed under a
    # project; make it non-nullable if every task MUST belong to a project.
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"), nullable=True
    )

    # The "many" side of the relationship. The ``back_populates`` name must match
    # the attribute on ``Project`` (``tasks``). Appending a ``Task`` to
    # ``project.tasks`` lets SQLAlchemy set ``project_id`` automatically once the
    # project has an id — you never hand-assign the FK.
    project: Mapped["Project | None"] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, title={self.title!r}, "
            f"priority={self.priority!r}, done={self.done})"
        )