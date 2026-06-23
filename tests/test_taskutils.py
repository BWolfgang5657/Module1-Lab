import pytest
from app.taskutils import parse_task, InvalidTaskError


def test_parse_task_valid_returns_normalized():
    # Arrange
    record = {"title": " Ship ", "priority": "HIGH"}
    # Act
    result = parse_task(record)
    # Assert
    assert result == {"title": "Ship", "priority": "high", "done": False}


def test_parse_task_missing_title_raises():
    with pytest.raises(InvalidTaskError):
        parse_task({})


def test_parse_task_whitespace_title_raises():
    with pytest.raises(InvalidTaskError):
        parse_task({"title": "   "})