ALLOWED_PRIORITIES = {"low", "medium", "high"}
MAXLEN = 200


import os
from dotenv import load_dotenv 

load_dotenv()


class Task:
    def __init__(self, title: str, priority: str = "medium", done: bool = False):
        self.title = title
        self.priority = priority
        self.done = done

    def complete(self) -> None:
        self.done = True

    def __repr__(self) -> str:
        return f"Task(title={self.title!r}, priority={self.priority!r}, done={self.done})"
    
    @classmethod
    def from_dict(cls, record: dict) -> "Task":
        data = parse_task(record)
        return cls(title=data['title'], priority=data['priority'], done=data.get('done', False))


class InvalidTaskError(ValueError):
    """Raised when a task is invalid."""


def parse_task(record: dict) -> dict:
    """Normalize a raw task record; raise InvalidTaskError on bad input."""
    # TODO: strip the title, reject empty/missing titles with InvalidTaskError,
    #       normalize priority to an allowed value, and return a clean dict
    #       shaped like {"title": ..., "priority": ..., "done": False}.
    title = record.get('title', '').strip()
    if not title:
        raise InvalidTaskError("Title is required")
    if len(title) > MAXLEN:
        raise InvalidTaskError("Title is too long. Maximum length is 200 characters.")
    priority = record.get('priority', 'medium').strip().lower()
    if priority not in ALLOWED_PRIORITIES:
        priority = 'medium'
    return {"title": title, "priority": priority, "done": False}


def priority_score(priority: str) -> int:
    """Return a numeric weight for sorting tasks by priority."""
    # TODO: map low/medium/high -> 1/2/3 and default unknown values to 0.
    weights = {"low": 1, "medium": 2, "high": 3}
    return weights.get(priority, 0)

def sort_tasks(tasks: list[dict]) -> list[dict]:
    return sorted(tasks, key=lambda t: priority_score(t['priority']), reverse=True)


# 🧩 Debug/Fix: this function has the classic mutable-default-argument bug.
# The default list is created ONCE at definition time and shared by every call,
# so tags accumulate across separate calls.
def add_tag(tag, tags: list[str] | None = None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

def high_priority_titles(tasks):
    highPriority = []
    for t in tasks:
        if priority_score(t['priority']) > 2:
            highPriority.append(t['title'])
    return highPriority
             
if __name__ == "__main__":
    if os.environ.get("DATABASE_URL"):
        print("Database URL found")
    else:
        print("Database URL not found")
    shipRelease = Task(title='Ship release', priority='high', done=False)
    print(shipRelease)
    shipRelease.complete()
    print(shipRelease)

    raw = [
        {"title": "  Deploy ", "priority": "HIGH"},
        {"title": "Docs", "priority": "low"},
        {"title": "Hotfix", "priority": "high"},
    ]

    parsed = [parse_task(r) for r in raw]

    print("high priority:", high_priority_titles(parsed))
    print("parsed:", parsed)
    print(add_tag("urgent"))   # expected: ['urgent']
    print(add_tag("urgent"))   # buggy:    ['urgent', 'urgent']
    print(add_tag("urgent"))   # buggy:    ['urgent', 'urgent', 'urgent']
