import pytest
from app.taskutils import parse_task, InvalidTaskError
from app.taskutils import priority_score

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

@pytest.fixture
def sample_tasks():
    return [
        {"title": "Deploy", "priority": "high", "done": False},
        {"title": "Docs", "priority": "low", "done": False},
    ]

def test_high_priority_filter(sample_tasks):
    from app.taskutils import high_priority_titles
    assert high_priority_titles(sample_tasks) == ["Deploy"]


@pytest.mark.parametrize("priority, expected", [
    ("low", 1),
    ("medium", 2),
    ("high", 3),
    ("unknown", 0),   # boundary / unexpected input
])

def test_priority_score_mapping(priority, expected):
    assert priority_score(priority) == expected