"""
Custom decorators for application functionality.
"""

from functools import wraps


def log_activity(func):
    """Decorator that logs activity when a function is called.

    Args:
        func (function): The function to be wrapped.

    Returns:
        function: The wrapped function with logging.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Activity: {func.__name__} executed")
        return func(*args, **kwargs)

    return wrapper
