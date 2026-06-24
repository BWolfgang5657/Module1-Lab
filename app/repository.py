from sqlalchemy import select
from app.models import Task


def create_task(session, title, project_id, priority="medium"):
    task = Task(title=title, project_id=project_id, priority=priority)
    session.add(task)
    session.commit()
    return task


def get_task(session, task_id):
    return session.get(Task, task_id)        # None if not found


def update_task(session, task_id, **changes):
    task = session.get(Task, task_id)
    if task is None:
        return None
    for field, value in changes.items():
        setattr(task, field, value)
    session.commit()
    return task


def delete_task(session, task_id):
    task = session.get(Task, task_id)
    if task is not None:
        session.delete(task)
        session.commit()