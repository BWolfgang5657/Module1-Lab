from app.taskutils import priority_score

def test_priority_score_unknown_zero():
    assert priority_score("unknown") == 0
