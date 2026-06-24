# test_demo_tasks.py
from app.taskutils import parse_task, priority_score
from app.taskutils import sort_tasks
import pytest
from app.taskutils import Task

@pytest.mark.parametrize("priority,expected", [
    ("low", 1),
    ("medium", 2),
    ("high", 3),
    ("HIGH", 0)
    ])

def test_priority_score_parametrized(priority, expected):
    assert(priority_score(priority) == expected)

def test_task_complete():
    task = Task("Deploy", "high", False)
    task.complete()
    assert task.done == True

def test_task_sort_empty():
    assert sort_tasks([]) == []

def test_task_sort_single():
    assert sort_tasks([{"task": "value", "priority": "high", "done": False}]) == [{"task": "value", "priority": "high", "done": False}]
    
def test_task_sort_multiple():
    sample_tasks = [
        {"title": "  Deploy ", "priority": "high", "done": False},
        {"title": "Docs", "priority": "low", "done": False},
        {"title": "Hotfix", "priority": "high", "done": False}]
    assert sort_tasks(sample_tasks) == [
        {"title": "Deploy", "priority": "high", "done": False},
        {"title": "Hotfix", "priority": "high", "done": False},
        {"title": "Docs", "priority": "low", "done": False}
    ]
# ── Test 1: Happy path ────────────────────────────────────────────────
def test_priority_score_high_returns_three():
    # Arrange
    priority = "high"
    # Act
    result = priority_score(priority)
    # Assert
    assert result == 3

# ── Test 2: Another happy path ───────────────────────────────────────
def test_parse_task_strips_title_whitespace():
    # Arrange
    record = {"title": "   Deploy API   ", "priority": "high"}
    # Act
    result = parse_task(record)
    # Assert
    assert result["title"] == "Deploy API"    # whitespace stripped
    assert result["done"] == False            # always starts not done