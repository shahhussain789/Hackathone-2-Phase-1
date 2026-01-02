"""Unit tests for Todo model"""

import pytest
from datetime import datetime
from src.models.todo import Todo, EmptyTitleError, InvalidInputError


class TestTodoCreation:
    """Tests for Todo creation"""

    def test_create_todo_with_title_only(self):
        """Test creating todo with title only (description defaults to empty)"""
        todo = Todo(id=1, title="Test todo")

        assert todo.id == 1
        assert todo.title == "Test todo"
        assert todo.description == ""
        assert todo.completed is False
        assert isinstance(todo.created_at, datetime)

    def test_create_todo_with_title_and_description(self):
        """Test creating todo with both title and description"""
        todo = Todo(
            id=2,
            title="Test todo",
            description="Test description"
        )

        assert todo.id == 2
        assert todo.title == "Test todo"
        assert todo.description == "Test description"
        assert todo.completed is False

    def test_todo_strips_whitespace(self):
        """Test that title and description are stripped of whitespace"""
        todo = Todo(
            id=1,
            title="  Test title  ",
            description="  Test description  "
        )

        assert todo.title == "Test title"
        assert todo.description == "Test description"


class TestTodoValidation:
    """Tests for Todo validation"""

    def test_empty_title_raises_error(self):
        """Test that empty title raises EmptyTitleError"""
        with pytest.raises(EmptyTitleError) as exc_info:
            Todo(id=1, title="")

        assert "Title cannot be empty" in str(exc_info.value)

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises EmptyTitleError"""
        with pytest.raises(EmptyTitleError):
            Todo(id=1, title="   ")

    def test_title_max_length_validation(self):
        """Test that title exceeding 200 characters raises InvalidInputError"""
        long_title = "a" * 201

        with pytest.raises(InvalidInputError) as exc_info:
            Todo(id=1, title=long_title)

        assert "Title too long" in str(exc_info.value)
        assert "201" in str(exc_info.value)

    def test_title_at_max_length_is_valid(self):
        """Test that title at exactly 200 characters is valid"""
        max_title = "a" * 200
        todo = Todo(id=1, title=max_title)

        assert len(todo.title) == 200

    def test_description_max_length_validation(self):
        """Test that description exceeding 2000 characters raises InvalidInputError"""
        long_description = "b" * 2001

        with pytest.raises(InvalidInputError) as exc_info:
            Todo(id=1, title="Test", description=long_description)

        assert "Description too long" in str(exc_info.value)
        assert "2001" in str(exc_info.value)

    def test_description_at_max_length_is_valid(self):
        """Test that description at exactly 2000 characters is valid"""
        max_description = "b" * 2000
        todo = Todo(id=1, title="Test", description=max_description)

        assert len(todo.description) == 2000


class TestTodoEdgeCases:
    """Tests for edge cases"""

    def test_unicode_in_title(self):
        """Test that Unicode characters are allowed in title"""
        todo = Todo(id=1, title="Test 你好 🎉")

        assert todo.title == "Test 你好 🎉"

    def test_unicode_in_description(self):
        """Test that Unicode characters are allowed in description"""
        todo = Todo(id=1, title="Test", description="Description with 中文 and emojis 🚀✨")

        assert "中文" in todo.description
        assert "🚀" in todo.description

    def test_special_characters_in_title(self):
        """Test that special characters are allowed in title"""
        todo = Todo(id=1, title="Test @#$%^&*()_+-=[]{}|;':\",./<>?")

        assert "@#$%^&*()" in todo.title

    def test_newlines_in_description(self):
        """Test that newlines in description are preserved"""
        todo = Todo(id=1, title="Test", description="Line 1\nLine 2\nLine 3")

        assert "\n" in todo.description
        assert "Line 1" in todo.description


class TestTodoStringRepresentation:
    """Tests for Todo string representation"""

    def test_str_representation_with_description(self):
        """Test string representation of todo with description"""
        todo = Todo(
            id=1,
            title="Test title",
            description="Test description",
            completed=False
        )

        str_repr = str(todo)

        assert "[1]" in str_repr
        assert "Test title" in str_repr
        assert "Test description" in str_repr
        assert "☐ Incomplete" in str_repr

    def test_str_representation_without_description(self):
        """Test string representation of todo without description"""
        todo = Todo(id=2, title="Test title")

        str_repr = str(todo)

        assert "[2]" in str_repr
        assert "Test title" in str_repr
        assert "Description" not in str_repr or "Description:" not in str_repr

    def test_str_representation_completed(self):
        """Test string representation of completed todo"""
        todo = Todo(id=3, title="Test title", completed=True)

        str_repr = str(todo)

        assert "✓ Complete" in str_repr
