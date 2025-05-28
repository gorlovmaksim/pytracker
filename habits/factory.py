"""Factory class to create Habit instances.

Provides a centralized way to create Habit objects with consistent initialization.
"""

from models import Habit


class HabitFactory:
    """Factory for creating Habit objects with proper initialization."""

    @staticmethod
    def create(name: str, periodicity: str, user_id: int, target_days: int) -> Habit:
        """Create a new Habit instance.

        Args:
            name: Name of the habit
            periodicity: 'daily' or 'weekly'
            user_id: ID of the owning user
            target_days: Target duration in days

        Returns:
            Habit: Newly created Habit instance
        """
        return Habit(
            name=name, periodicity=periodicity, user_id=user_id, target_days=target_days
        )
