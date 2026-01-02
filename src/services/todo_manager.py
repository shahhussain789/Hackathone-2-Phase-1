"""TodoManager service for CRUD operations and business logic"""

from typing import Optional
from src.models.todo import Todo, TodoNotFoundError, InvalidInputError, EmptyTitleError


class TodoManager:
    """Manages todo items with in-memory storage.

    Provides CRUD operations (Create, Read, Update, Delete) and business logic
    for managing todo items. Uses dictionary for O(1) lookup performance.
    """

    def __init__(self) -> None:
        """Initialize TodoManager with empty storage."""
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1

    def add_todo(self, title: str, description: str = "") -> Todo:
        """Add a new todo to the list.

        Args:
            title: The todo title (required, max 200 chars)
            description: Optional description (max 2000 chars)

        Returns:
            The created Todo object with auto-generated ID

        Raises:
            EmptyTitleError: If title is empty or whitespace-only
            InvalidInputError: If title/description exceeds max length
        """
        # Create todo with next available ID (validation happens in Todo.__post_init__)
        todo = Todo(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )

        # Store todo and increment ID
        self._todos[self._next_id] = todo
        self._next_id += 1

        return todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get a todo by ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            The Todo object if found, None otherwise
        """
        return self._todos.get(todo_id)

    def list_todos(self) -> list[Todo]:
        """Get all todos in creation order.

        Returns:
            List of all todos ordered by creation time (oldest first)
        """
        return list(self._todos.values())

    def update_todo(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Todo:
        """Update todo title and/or description.

        Args:
            todo_id: The ID of the todo to update
            title: New title (None = keep current)
            description: New description (None = keep current)

        Returns:
            The updated Todo object

        Raises:
            TodoNotFoundError: If todo with given ID doesn't exist
            EmptyTitleError: If new title is empty or whitespace-only
            InvalidInputError: If new title/description exceeds max length
        """
        # Check if todo exists
        if todo_id not in self._todos:
            raise TodoNotFoundError(
                f"Todo #{todo_id} not found. Use 'view' to see all todos."
            )

        todo = self._todos[todo_id]

        # Update title if provided
        if title is not None:
            title = title.strip()
            if not title:
                raise EmptyTitleError(
                    "Title cannot be empty. Please provide a title for your todo."
                )
            if len(title) > 200:
                raise InvalidInputError(
                    f"Title too long (max 200 characters). Current length: {len(title)}"
                )
            todo.title = title

        # Update description if provided
        if description is not None:
            description = description.strip()
            if len(description) > 2000:
                raise InvalidInputError(
                    f"Description too long (max 2000 characters). Current length: {len(description)}"
                )
            todo.description = description

        return todo

    def delete_todo(self, todo_id: int) -> None:
        """Delete a todo by ID.

        Args:
            todo_id: The ID of the todo to delete

        Raises:
            TodoNotFoundError: If todo with given ID doesn't exist
        """
        if todo_id not in self._todos:
            raise TodoNotFoundError(
                f"Todo #{todo_id} not found. Use 'view' to see all todos."
            )

        del self._todos[todo_id]

    def mark_complete(self, todo_id: int, completed: bool) -> Todo:
        """Mark a todo as complete or incomplete.

        Args:
            todo_id: The ID of the todo to update
            completed: True to mark complete, False to mark incomplete

        Returns:
            The updated Todo object

        Raises:
            TodoNotFoundError: If todo with given ID doesn't exist
        """
        if todo_id not in self._todos:
            raise TodoNotFoundError(
                f"Todo #{todo_id} not found. Use 'view' to see all todos."
            )

        todo = self._todos[todo_id]
        todo.completed = completed

        return todo

    def get_stats(self) -> dict[str, int]:
        """Get statistics about todos.

        Returns:
            Dictionary with 'total', 'completed', and 'incomplete' counts
        """
        total = len(self._todos)
        completed = sum(1 for todo in self._todos.values() if todo.completed)
        incomplete = total - completed

        return {
            "total": total,
            "completed": completed,
            "incomplete": incomplete
        }
