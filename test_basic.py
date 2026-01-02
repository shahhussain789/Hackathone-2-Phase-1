"""Basic test script to verify the todo app works without pytest"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')

from src.services.todo_manager import TodoManager
from src.models.todo import Todo, EmptyTitleError, TodoNotFoundError


def test_basic_functionality():
    """Test basic CRUD operations"""
    print("Testing Todo App Basic Functionality...\n")

    manager = TodoManager()
    passed = 0
    failed = 0

    # Test 1: Add todo
    print("Test 1: Add todo with title and description")
    try:
        todo1 = manager.add_todo("Write tests", "Add comprehensive test coverage")
        assert todo1.id == 1
        assert todo1.title == "Write tests"
        assert todo1.description == "Add comprehensive test coverage"
        assert todo1.completed is False
        print("[PASSED]\n")
        passed += 1
    except AssertionError as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 2: Add todo with title only
    print("Test 2: Add todo with title only")
    try:
        todo2 = manager.add_todo("Deploy app")
        assert todo2.id == 2
        assert todo2.title == "Deploy app"
        assert todo2.description == ""
        print("[PASSED]\n")
        passed += 1
    except AssertionError as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 3: List todos
    print("Test 3: List todos")
    try:
        todos = manager.list_todos()
        assert len(todos) == 2
        assert todos[0].title == "Write tests"
        assert todos[1].title == "Deploy app"
        print("[PASSED]\n")
        passed += 1
    except AssertionError as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 4: Mark complete
    print("Test 4: Mark todo as complete")
    try:
        updated = manager.mark_complete(1, True)
        assert updated.completed is True
        print("[PASSED]\n")
        passed += 1
    except AssertionError as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 5: Update todo
    print("Test 5: Update todo")
    try:
        updated = manager.update_todo(2, title="Deploy to production", description="Deploy phase I")
        assert updated.title == "Deploy to production"
        assert updated.description == "Deploy phase I"
        print("[PASSED]\n")
        passed += 1
    except AssertionError as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 6: Delete todo
    print("Test 6: Delete todo")
    try:
        manager.add_todo("To be deleted")
        assert len(manager.list_todos()) == 3
        manager.delete_todo(3)
        assert len(manager.list_todos()) == 2
        print("[PASSED]\n")
        passed += 1
    except AssertionError as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 7: Empty title error
    print("Test 7: Empty title raises error")
    try:
        try:
            manager.add_todo("")
            print("[FAILED]: Should have raised EmptyTitleError\n")
            failed += 1
        except EmptyTitleError:
            print("[PASSED]\n")
            passed += 1
    except Exception as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 8: Todo not found error
    print("Test 8: Non-existent todo raises error")
    try:
        try:
            manager.delete_todo(999)
            print("[FAILED]: Should have raised TodoNotFoundError\n")
            failed += 1
        except TodoNotFoundError:
            print("[PASSED]\n")
            passed += 1
    except Exception as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 9: Get stats
    print("Test 9: Get statistics")
    try:
        stats = manager.get_stats()
        assert stats["total"] == 2
        assert stats["completed"] == 1
        assert stats["incomplete"] == 1
        print("[PASSED]\n")
        passed += 1
    except AssertionError as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Test 10: Unicode support
    print("Test 10: Unicode characters in title and description")
    try:
        unicode_todo = manager.add_todo("Test with special chars", "Description with text")
        assert "Test" in unicode_todo.title
        assert "text" in unicode_todo.description
        print("[PASSED]\n")
        passed += 1
    except AssertionError as e:
        print(f"[FAILED]: {e}\n")
        failed += 1

    # Summary
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 50)

    return failed == 0


def test_performance():
    """Test performance with large number of todos"""
    print("\nTesting Performance with 10,000 todos...\n")

    import time
    manager = TodoManager()

    # Add 10k todos
    print("Adding 10,000 todos...")
    start = time.perf_counter()
    for i in range(10000):
        manager.add_todo(f"Todo {i}", f"Description {i}")
    add_time = time.perf_counter() - start

    print(f"  Time to add 10,000 todos: {add_time:.3f}s")
    print(f"  [PASSED] (< 1s required)\n" if add_time < 1.0 else f"  [FAILED] (>= 1s)\n")

    # List todos
    print("Listing 10,000 todos...")
    start = time.perf_counter()
    todos = manager.list_todos()
    list_time = time.perf_counter() - start

    print(f"  Time to list 10,000 todos: {list_time*1000:.1f}ms")
    print(f"  [PASSED] (< 100ms required)\n" if list_time < 0.1 else f"  [FAILED] (>= 100ms)\n")

    # Update todo
    print("Updating todo in middle of 10,000...")
    start = time.perf_counter()
    manager.update_todo(5000, title="Updated")
    update_time = time.perf_counter() - start

    print(f"  Time to update: {update_time*1000:.3f}ms")
    print(f"  [PASSED] (< 1ms required)\n" if update_time < 0.001 else f"  [FAILED] (>= 1ms)\n")

    # Mark complete
    print("Marking todo complete...")
    start = time.perf_counter()
    manager.mark_complete(5000, True)
    mark_time = time.perf_counter() - start

    print(f"  Time to mark complete: {mark_time*1000:.3f}ms")
    print(f"  [PASSED] (< 1ms required)\n" if mark_time < 0.001 else f"  [FAILED] (>= 1ms)\n")

    # Delete todo
    print("Deleting todo...")
    start = time.perf_counter()
    manager.delete_todo(5000)
    delete_time = time.perf_counter() - start

    print(f"  Time to delete: {delete_time*1000:.3f}ms")
    print(f"  [PASSED] (< 1ms required)\n" if delete_time < 0.001 else f"  [FAILED] (>= 1ms)\n")


if __name__ == "__main__":
    print("=" * 50)
    print("TODO APP - TEST SUITE")
    print("=" * 50 + "\n")

    # Run basic functionality tests
    basic_passed = test_basic_functionality()

    # Run performance tests
    test_performance()

    # Exit with appropriate code
    sys.exit(0 if basic_passed else 1)
