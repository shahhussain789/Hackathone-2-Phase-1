"""Unit tests for TodoManager service"""

import pytest
from src.services.todo_manager import TodoManager
from src.models.todo import (
    Todo,
    TodoNotFoundError,
    EmptyTitleError,
    InvalidInputError
)


class TestAddTodo:
    """Tests for adding todos"""

    def test_add_todo_with_valid_inputs(self):
        """Test adding a todo with valid title and description"""
        manager = TodoManager()
        todo = manager.add_todo("Test title", "Test description")

        assert todo.id == 1
        assert todo.title == "Test title"
        assert todo.description == "Test description"
        assert todo.completed is False

    def test_add_todo_with_title_only(self):
        """Test adding a todo with title only"""
        manager = TodoManager()
        todo = manager.add_todo("Test title")

        assert todo.id == 1
        assert todo.title == "Test title"
        assert todo.description == ""

    def test_add_todo_assigns_sequential_ids(self):
        """Test that sequential IDs are assigned"""
        manager = TodoManager()

        todo1 = manager.add_todo("First")
        todo2 = manager.add_todo("Second")
        todo3 = manager.add_todo("Third")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

    def test_add_todo_with_empty_title_raises_error(self):
        """Test that adding todo with empty title raises error"""
        manager = TodoManager()

        with pytest.raises(EmptyTitleError):
            manager.add_todo("")

    def test_add_todo_with_long_title_raises_error(self):
        """Test that adding todo with title >200 chars raises error"""
        manager = TodoManager()

        with pytest.raises(InvalidInputError):
            manager.add_todo("a" * 201)


class TestListTodos:
    """Tests for listing todos"""

    def test_list_todos_returns_empty_list_initially(self):
        """Test that list_todos returns empty list for new manager"""
        manager = TodoManager()
        todos = manager.list_todos()

        assert todos == []
        assert len(todos) == 0

    def test_list_todos_returns_todos_in_creation_order(self):
        """Test that todos are returned in creation order"""
        manager = TodoManager()

        todo1 = manager.add_todo("First")
        todo2 = manager.add_todo("Second")
        todo3 = manager.add_todo("Third")

        todos = manager.list_todos()

        assert len(todos) == 3
        assert todos[0].id == 1
        assert todos[1].id == 2
        assert todos[2].id == 3
        assert todos[0].title == "First"
        assert todos[1].title == "Second"
        assert todos[2].title == "Third"


class TestMarkComplete:
    """Tests for marking todos complete/incomplete"""

    def test_mark_todo_as_complete(self):
        """Test marking a todo as complete"""
        manager = TodoManager()
        todo = manager.add_todo("Test")

        assert todo.completed is False

        updated = manager.mark_complete(1, True)

        assert updated.completed is True
        assert updated.id == 1

    def test_toggle_todo_from_complete_to_incomplete(self):
        """Test toggling a todo from complete back to incomplete"""
        manager = TodoManager()
        todo = manager.add_todo("Test")

        manager.mark_complete(1, True)
        assert todo.completed is True

        manager.mark_complete(1, False)
        assert todo.completed is False

    def test_mark_complete_non_existent_todo_raises_error(self):
        """Test that marking non-existent todo raises error"""
        manager = TodoManager()

        with pytest.raises(TodoNotFoundError) as exc_info:
            manager.mark_complete(999, True)

        assert "999" in str(exc_info.value)


class TestUpdateTodo:
    """Tests for updating todos"""

    def test_update_todo_title_only(self):
        """Test updating only the title"""
        manager = TodoManager()
        manager.add_todo("Original", "Description")

        updated = manager.update_todo(1, title="Updated")

        assert updated.title == "Updated"
        assert updated.description == "Description"

    def test_update_todo_description_only(self):
        """Test updating only the description"""
        manager = TodoManager()
        manager.add_todo("Title", "Original")

        updated = manager.update_todo(1, description="Updated description")

        assert updated.title == "Title"
        assert updated.description == "Updated description"

    def test_update_both_title_and_description(self):
        """Test updating both title and description"""
        manager = TodoManager()
        manager.add_todo("Original", "Original desc")

        updated = manager.update_todo(1, title="New title", description="New desc")

        assert updated.title == "New title"
        assert updated.description == "New desc"

    def test_update_with_empty_title_raises_error(self):
        """Test that updating with empty title raises error"""
        manager = TodoManager()
        manager.add_todo("Original")

        with pytest.raises(EmptyTitleError):
            manager.update_todo(1, title="")

    def test_update_non_existent_todo_raises_error(self):
        """Test that updating non-existent todo raises error"""
        manager = TodoManager()

        with pytest.raises(TodoNotFoundError) as exc_info:
            manager.update_todo(999, title="Test")

        assert "999" in str(exc_info.value)

    def test_update_with_none_keeps_current_values(self):
        """Test that passing None keeps current values"""
        manager = TodoManager()
        manager.add_todo("Original", "Original desc")

        updated = manager.update_todo(1, title=None, description=None)

        assert updated.title == "Original"
        assert updated.description == "Original desc"


class TestDeleteTodo:
    """Tests for deleting todos"""

    def test_delete_existing_todo(self):
        """Test deleting an existing todo"""
        manager = TodoManager()
        manager.add_todo("Test")

        manager.delete_todo(1)

        todos = manager.list_todos()
        assert len(todos) == 0

    def test_delete_non_existent_todo_raises_error(self):
        """Test that deleting non-existent todo raises error"""
        manager = TodoManager()

        with pytest.raises(TodoNotFoundError) as exc_info:
            manager.delete_todo(999)

        assert "999" in str(exc_info.value)

    def test_delete_middle_todo_preserves_other_ids(self):
        """Test that deleting middle todo preserves other IDs"""
        manager = TodoManager()

        manager.add_todo("First")
        manager.add_todo("Second")
        manager.add_todo("Third")

        manager.delete_todo(2)

        todos = manager.list_todos()
        assert len(todos) == 2
        assert todos[0].id == 1
        assert todos[1].id == 3


class TestGetTodo:
    """Tests for getting individual todos"""

    def test_get_existing_todo(self):
        """Test getting an existing todo by ID"""
        manager = TodoManager()
        added = manager.add_todo("Test", "Description")

        retrieved = manager.get_todo(1)

        assert retrieved is not None
        assert retrieved.id == added.id
        assert retrieved.title == "Test"

    def test_get_non_existent_todo_returns_none(self):
        """Test that getting non-existent todo returns None"""
        manager = TodoManager()

        result = manager.get_todo(999)

        assert result is None


class TestGetStats:
    """Tests for getting todo statistics"""

    def test_stats_with_no_todos(self):
        """Test stats with empty todo list"""
        manager = TodoManager()

        stats = manager.get_stats()

        assert stats["total"] == 0
        assert stats["completed"] == 0
        assert stats["incomplete"] == 0

    def test_stats_with_all_incomplete(self):
        """Test stats with all incomplete todos"""
        manager = TodoManager()
        manager.add_todo("Test 1")
        manager.add_todo("Test 2")
        manager.add_todo("Test 3")

        stats = manager.get_stats()

        assert stats["total"] == 3
        assert stats["completed"] == 0
        assert stats["incomplete"] == 3

    def test_stats_with_mixed_completion(self):
        """Test stats with mix of complete and incomplete"""
        manager = TodoManager()
        manager.add_todo("Test 1")
        manager.add_todo("Test 2")
        manager.add_todo("Test 3")
        manager.add_todo("Test 4")

        manager.mark_complete(1, True)
        manager.mark_complete(3, True)

        stats = manager.get_stats()

        assert stats["total"] == 4
        assert stats["completed"] == 2
        assert stats["incomplete"] == 2

    def test_stats_with_all_complete(self):
        """Test stats with all complete todos"""
        manager = TodoManager()
        manager.add_todo("Test 1")
        manager.add_todo("Test 2")

        manager.mark_complete(1, True)
        manager.mark_complete(2, True)

        stats = manager.get_stats()

        assert stats["total"] == 2
        assert stats["completed"] == 2
        assert stats["incomplete"] == 0
