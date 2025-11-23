"""
Base action interface using Command pattern.
"""
from abc import ABC, abstractmethod


class BaseAction(ABC):
    """
    Abstract base class for application actions.

    Implements the Command pattern to encapsulate action logic
    and decouple it from UI components.
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the action.

        This method should contain the main logic for the action.
        """
        pass

    def can_execute(self) -> bool:
        """
        Check if the action can be executed.

        Returns:
            True if action can be executed, False otherwise
        """
        return True
