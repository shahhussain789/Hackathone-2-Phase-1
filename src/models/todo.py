"""Todo data model with validation logic and custom exceptions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# Custom Exception Classes
class TodoError(Exception):
    """Base exception for all todo-related errors"""
    pass


class TodoNotFoundError(TodoError):
    """Raised when a todo with the specified ID is not found"""
    pass


class InvalidInputError(TodoError):
    """Raised when input validation fails"""
    pass


class EmptyTitleError(InvalidInputError):
    """Raised when todo title is empty or whitespace-only"""
    pass


@dataclass
class Todo:
    """Represents a todo item with title, description, and completion status.

    Attributes:
        id: Unique identifier for the todo
        title: Short description of the task (required, max 200 chars)
        description: Detailed description of the task (optional, max 2000 chars)
        completed: Completion status of the todo (defaults to False)
        created_at: Timestamp when todo was created (auto-generated)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate todo attributes after initialization.

        Raises:
            EmptyTitleError: If title is empty or whitespace-only
            InvalidInputError: If title or description exceeds max length
        """
        # Strip whitespace from title and description
        self.title = self.title.strip()
        self.description = self.description.strip()

        # Validate title is not empty
        if not self.title:
            raise EmptyTitleError(
                "Title cannot be empty. Please provide a title for your todo."
            )

        # Validate title length
        if len(self.title) > 200:
            raise InvalidInputError(
                f"Title too long (max 200 characters). Current length: {len(self.title)}"
            )

        # Validate description length
        if len(self.description) > 2000:
            raise InvalidInputError(
                f"Description too long (max 2000 characters). Current length: {len(self.description)}"
            )

    def __str__(self) -> str:
        """Return a user-friendly string representation of the todo"""
        status = "✓ Complete" if self.completed else "☐ Incomplete"
        desc = f"\n    Description: {self.description}" if self.description else ""
        return (
            f"[{self.id}] {self.title}{desc}\n"
            f"    Status: {status}\n"
            f"    Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
