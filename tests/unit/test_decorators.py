"""
Unit tests for custom decorators.
"""

from decorators import log_activity


def test_log_activity(capsys):
    """Test the log_activity decorator.

    Args:
        capsys (pytest.CaptureFixture): Pytest fixture to capture stdout/stderr.
    """

    @log_activity
    def test_func():
        return "test"

    result = test_func()
    captured = capsys.readouterr()

    assert result == "test"
    assert "test_func executed" in captured.out
