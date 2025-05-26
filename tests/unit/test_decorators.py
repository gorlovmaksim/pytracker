"""Unit tests for custom decorators."""

from decorators import log_activity


def test_log_activity(capsys):
    """Test the log_activity decorator."""
    @log_activity
    def test_func():
        return "test"

    result = test_func()
    captured = capsys.readouterr()

    assert result == "test"
    assert "test_func executed" in captured.out