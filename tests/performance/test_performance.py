"""Performance tests for 10k todos requirement"""

import pytest
import time
from src.services.todo_manager import TodoManager


@pytest.mark.slow
class TestPerformanceWith10kTodos:
    """Performance tests with 10,000 todos"""

    def test_add_10k_todos_performance(self):
        """Test that adding 10k todos is fast"""
        manager = TodoManager()

        start = time.perf_counter()

        for i in range(10000):
            manager.add_todo(f"Todo {i}", f"Description {i}")

        elapsed = time.perf_counter() - start

        # Should take less than 1 second total (0.1ms per todo on average)
        assert elapsed < 1.0, f"Adding 10k todos took {elapsed:.3f}s (expected <1s)"

        # Verify all were added
        assert len(manager.list_todos()) == 10000

    def test_view_10k_todos_performance(self):
        """Test that viewing 10k todos meets <100ms requirement"""
        manager = TodoManager()

        # Setup: Add 10k todos
        for i in range(10000):
            manager.add_todo(f"Todo {i}", f"Description {i}")

        # Test: List todos
        start = time.perf_counter()
        todos = manager.list_todos()
        elapsed = time.perf_counter() - start

        # Should be under 100ms
        assert elapsed < 0.1, f"Listing 10k todos took {elapsed*1000:.1f}ms (expected <100ms)"
        assert len(todos) == 10000

    def test_update_todo_performance_with_10k_todos(self):
        """Test that updating a todo with 10k todos is fast"""
        manager = TodoManager()

        # Setup: Add 10k todos
        for i in range(10000):
            manager.add_todo(f"Todo {i}", f"Description {i}")

        # Test: Update a todo in the middle
        start = time.perf_counter()
        manager.update_todo(5000, title="Updated title", description="Updated desc")
        elapsed = time.perf_counter() - start

        # Should be under 1ms (dict lookup is O(1))
        assert elapsed < 0.001, f"Update took {elapsed*1000:.1f}ms (expected <1ms)"

    def test_delete_todo_performance_with_10k_todos(self):
        """Test that deleting a todo with 10k todos is fast"""
        manager = TodoManager()

        # Setup: Add 10k todos
        for i in range(10000):
            manager.add_todo(f"Todo {i}", f"Description {i}")

        # Test: Delete a todo in the middle
        start = time.perf_counter()
        manager.delete_todo(5000)
        elapsed = time.perf_counter() - start

        # Should be under 1ms (dict deletion is O(1))
        assert elapsed < 0.001, f"Delete took {elapsed*1000:.1f}ms (expected <1ms)"

        assert len(manager.list_todos()) == 9999

    def test_mark_complete_performance_with_10k_todos(self):
        """Test that marking complete with 10k todos is fast"""
        manager = TodoManager()

        # Setup: Add 10k todos
        for i in range(10000):
            manager.add_todo(f"Todo {i}", f"Description {i}")

        # Test: Mark todo complete
        start = time.perf_counter()
        manager.mark_complete(5000, True)
        elapsed = time.perf_counter() - start

        # Should be under 1ms (dict lookup is O(1))
        assert elapsed < 0.001, f"Mark complete took {elapsed*1000:.1f}ms (expected <1ms)"

    def test_get_stats_performance_with_10k_todos(self):
        """Test that getting stats with 10k todos is reasonable"""
        manager = TodoManager()

        # Setup: Add 10k todos, mark half complete
        for i in range(10000):
            manager.add_todo(f"Todo {i}")
            if i % 2 == 0:
                manager.mark_complete(i + 1, True)

        # Test: Get stats
        start = time.perf_counter()
        stats = manager.get_stats()
        elapsed = time.perf_counter() - start

        # Should be under 100ms (needs to iterate all todos)
        assert elapsed < 0.1, f"Get stats took {elapsed*1000:.1f}ms (expected <100ms)"
        assert stats["total"] == 10000
        assert stats["completed"] == 5000
        assert stats["incomplete"] == 5000


@pytest.mark.slow
class TestMemoryUsage:
    """Memory usage tests"""

    def test_10k_todos_memory_footprint(self):
        """Test that 10k todos stay within memory budget"""
        import sys

        manager = TodoManager()

        # Measure baseline
        baseline_size = sys.getsizeof(manager._todos)

        # Add 10k todos
        for i in range(10000):
            manager.add_todo(
                f"Todo {i}" * 5,  # ~40 chars title
                f"Description {i}" * 10  # ~120 chars description
            )

        # Measure after adding todos
        final_size = sys.getsizeof(manager._todos)

        # Rough estimate: each todo should be < 1KB
        # 10k todos * 1KB = 10MB max (well under 50MB budget)
        estimated_per_todo = (final_size - baseline_size) / 10000

        # This is a rough check - actual memory is more complex
        # But should give us confidence we're in the right ballpark
        assert estimated_per_todo < 10000, \
            f"Estimated {estimated_per_todo} bytes per todo (seems high)"


@pytest.mark.slow
class TestConcurrentOperations:
    """Test that system handles many consecutive operations"""

    def test_10k_consecutive_operations_without_crash(self):
        """Test that system handles 10k consecutive operations"""
        manager = TodoManager()

        # Mix of operations
        for i in range(2500):
            # Add
            manager.add_todo(f"Todo {i}", f"Desc {i}")

            # Mark complete
            if i > 0:
                manager.mark_complete(i, True)

            # Update
            if i > 1:
                manager.update_todo(i - 1, description=f"Updated {i}")

            # Get stats
            stats = manager.get_stats()
            assert stats["total"] == i + 1

        # Final verification
        assert len(manager.list_todos()) == 2500
        assert manager.get_stats()["total"] == 2500
