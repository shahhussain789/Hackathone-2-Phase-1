"""Integration tests for CLI workflows"""

import pytest
from src.services.todo_manager import TodoManager


class TestAddAndViewWorkflow:
    """Integration tests for add-then-view workflow"""

    def test_add_multiple_todos_and_view(self):
        """Test adding multiple todos and viewing them"""
        manager = TodoManager()

        # Add multiple todos
        todo1 = manager.add_todo("Write tests", "Add pytest tests for all CRUD operations")
        todo2 = manager.add_todo("Deploy app", "")
        todo3 = manager.add_todo("Update docs", "Add README with usage examples")

        # View all todos
        todos = manager.list_todos()

        assert len(todos) == 3
        assert todos[0].id == todo1.id
        assert todos[1].id == todo2.id
        assert todos[2].id == todo3.id

        # Verify data integrity
        assert todos[0].title == "Write tests"
        assert todos[0].description == "Add pytest tests for all CRUD operations"
        assert todos[1].description == ""
        assert todos[2].title == "Update docs"


class TestMarkCompleteWorkflow:
    """Integration tests for mark-complete workflow"""

    def test_add_view_mark_complete_workflow(self):
        """Test full workflow: add → view → mark complete → view"""
        manager = TodoManager()

        # Create todos
        manager.add_todo("Task 1")
        manager.add_todo("Task 2")
        manager.add_todo("Task 3")

        # Mark some as complete
        manager.mark_complete(1, True)
        manager.mark_complete(3, True)

        # Verify stats
        stats = manager.get_stats()
        assert stats["total"] == 3
        assert stats["completed"] == 2
        assert stats["incomplete"] == 1

        # Verify individual statuses
        todos = manager.list_todos()
        assert todos[0].completed is True
        assert todos[1].completed is False
        assert todos[2].completed is True


class TestUpdateWorkflow:
    """Integration tests for update workflow"""

    def test_add_view_update_workflow(self):
        """Test full workflow: add → view → update → view"""
        manager = TodoManager()

        # Create todo
        original = manager.add_todo("Original title", "Original description")

        # Update it
        updated = manager.update_todo(
            original.id,
            title="Updated title",
            description="Updated description"
        )

        # Verify update
        assert updated.id == original.id
        assert updated.title == "Updated title"
        assert updated.description == "Updated description"

        # Verify in list
        todos = manager.list_todos()
        assert len(todos) == 1
        assert todos[0].title == "Updated title"


class TestDeleteWorkflow:
    """Integration tests for delete workflow"""

    def test_add_view_delete_workflow(self):
        """Test full workflow: add → view → delete → view"""
        manager = TodoManager()

        # Create todos
        manager.add_todo("Keep 1")
        manager.add_todo("Delete me")
        manager.add_todo("Keep 2")

        # Delete middle one
        manager.delete_todo(2)

        # Verify remaining todos
        todos = manager.list_todos()
        assert len(todos) == 2
        assert todos[0].title == "Keep 1"
        assert todos[1].title == "Keep 2"


class TestCompleteUserJourney:
    """Integration tests for complete user journeys"""

    def test_complete_crud_workflow(self):
        """Test complete CRUD workflow in one session"""
        manager = TodoManager()

        # Create
        todo1 = manager.add_todo("Task 1", "Description 1")
        todo2 = manager.add_todo("Task 2", "Description 2")
        todo3 = manager.add_todo("Task 3", "Description 3")

        assert len(manager.list_todos()) == 3

        # Read
        fetched = manager.get_todo(2)
        assert fetched.title == "Task 2"

        # Update
        manager.update_todo(2, title="Updated Task 2")
        updated = manager.get_todo(2)
        assert updated.title == "Updated Task 2"

        # Mark complete
        manager.mark_complete(1, True)
        manager.mark_complete(2, True)

        # Delete
        manager.delete_todo(3)

        # Final verification
        todos = manager.list_todos()
        assert len(todos) == 2
        assert all(todo.completed for todo in todos)

    def test_error_recovery_workflow(self):
        """Test that system recovers from errors and continues"""
        manager = TodoManager()

        # Add valid todo
        manager.add_todo("Valid task")

        # Attempt invalid operations (should raise errors)
        with pytest.raises(Exception):
            manager.add_todo("")  # Empty title

        with pytest.raises(Exception):
            manager.delete_todo(999)  # Non-existent ID

        with pytest.raises(Exception):
            manager.update_todo(1, title="")  # Empty title

        # System should still work after errors
        manager.add_todo("Another valid task")
        todos = manager.list_todos()

        assert len(todos) == 2
        assert todos[0].title == "Valid task"
        assert todos[1].title == "Another valid task"
