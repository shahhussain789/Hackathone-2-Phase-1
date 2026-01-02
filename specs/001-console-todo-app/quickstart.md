# Quickstart Guide: In-Memory Console Todo App (Phase I)

**Feature**: 001-console-todo-app
**Date**: 2026-01-02
**Target Audience**: Python developers evaluating the Agentic Dev Stack workflow

## Overview

This guide provides a quick walkthrough of the In-Memory Console Todo App implementation, testing, and validation process. It follows the Spec-Kit Plus methodology: Spec → Plan → Tasks → Implementation.

## Prerequisites

### System Requirements

- Python 3.13 or higher
- Cross-platform: Windows, macOS, or Linux
- Terminal/console with UTF-8 support

### Development Tools (Optional)

- pytest (for running tests)
- coverage.py (for test coverage reports)
- black, flake8, mypy (for code quality)

### Installation

```bash
# Verify Python version
python --version  # Should be 3.13.x or higher

# Clone or navigate to the project
cd /path/to/project

# Install development dependencies (optional)
pip install pytest coverage black flake8 mypy
```

## Project Structure

```
project-root/
├── src/
│   ├── models/
│   │   └── todo.py              # Todo dataclass, validation
│   ├── services/
│   │   └── todo_manager.py      # CRUD operations, business logic
│   ├── cli/
│   │   └── app.py               # REPL interface, command handlers
│   └── main.py                  # Entry point
├── tests/
│   ├── unit/
│   │   ├── test_todo_model.py   # Todo model tests
│   │   └── test_todo_manager.py # TodoManager tests
│   ├── integration/
│   │   └── test_cli.py          # Full command flow tests
│   └── performance/
│       └── test_performance.py  # 10k todos performance tests
├── specs/
│   └── 001-console-todo-app/
│       ├── spec.md              # Feature specification
│       ├── plan.md              # Implementation plan
│       ├── research.md          # Technology decisions
│       ├── data-model.md        # Data model design
│       ├── quickstart.md        # This file
│       └── contracts/
│           └── cli-interface.md # CLI contract
├── README.md
└── pyproject.toml (or setup.py)
```

## Quick Start: Using the Application

### Running the App

```bash
# From project root
python src/main.py
```

### Example Session

```
========================================
    TODO APP - Phase I
========================================

Main Menu:
1. Add new todo
2. View all todos
3. Update todo
4. Delete todo
5. Mark todo complete/incomplete
6. Help
7. Exit

Enter your choice (1-7): 1

Enter todo title: Write unit tests
Enter description (optional, press Enter to skip): Add pytest tests for all CRUD operations

✓ Todo added successfully!
  ID: 1
  Title: Write unit tests
  Description: Add pytest tests for all CRUD operations
  Status: Incomplete

Enter your choice (1-7): 1

Enter todo title: Deploy to production
Enter description (optional, press Enter to skip):

✓ Todo added successfully!
  ID: 2
  Title: Deploy to production
  Description:
  Status: Incomplete

Enter your choice (1-7): 2

========================================
    ALL TODOS
========================================

[1] Write unit tests
    Description: Add pytest tests for all CRUD operations
    Status: ☐ Incomplete
    Created: 2026-01-02 14:23:15

[2] Deploy to production
    Description:
    Status: ☐ Incomplete
    Created: 2026-01-02 14:25:42

Total: 2 todos (0 complete, 2 incomplete)
========================================

Enter your choice (1-7): 5

Enter todo ID to mark: 1
Current status: Incomplete
Mark as (1=Complete, 2=Incomplete): 1

✓ Todo #1 marked as complete!

Enter your choice (1-7): 7

Are you sure you want to exit? All data will be lost. (y/n): y

========================================
Thank you for using TODO APP!
All data has been cleared.
========================================
```

## Development Workflow

### Phase 0: Research (Completed)

Research findings documented in `research.md`:
- Technology stack: Python 3.13+, pytest
- Data structure: Dict for O(1) lookup
- CLI pattern: Menu-driven REPL
- Architecture: Three-layer (models, services, CLI)

### Phase 1: Design (Completed)

Design artifacts created:
- `data-model.md`: Todo entity, validation rules, storage structure
- `contracts/cli-interface.md`: CLI command specifications
- `quickstart.md`: This guide

### Phase 2: Task Breakdown (Next Step)

Run `/sp.tasks` to generate actionable tasks from the plan:

```bash
# Tasks will be organized by user story priority (P1-P4)
# Example tasks:
# - T001: Create Todo dataclass with validation
# - T002: Implement TodoManager service
# - T003: Build REPL interface
# - T004: Add unit tests (TDD: write before implementation)
```

### Phase 3: Implementation

Follow Test-First Development (Constitution Principle VII):

1. **Red**: Write failing tests
2. **Green**: Implement minimal code to pass tests
3. **Refactor**: Clean up code while keeping tests green

```bash
# Example TDD cycle
# 1. Write test
vim tests/unit/test_todo_model.py

# 2. Run test (should fail)
pytest tests/unit/test_todo_model.py

# 3. Implement feature
vim src/models/todo.py

# 4. Run test (should pass)
pytest tests/unit/test_todo_model.py

# 5. Refactor and repeat
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_todo_model.py

# Run with coverage report
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### Test Coverage Requirements

Per Phase I constitution:
- **Minimum coverage**: 80%
- **All CRUD operations**: Unit tested
- **Edge cases**: Validated (empty input, invalid IDs, special chars)
- **Performance**: 10k todos in <100ms

### Performance Validation

```bash
# Run performance tests
pytest tests/performance/test_performance.py -v

# Expected output:
# test_add_10k_todos ... PASSED (0.85s)
# test_view_10k_todos ... PASSED (0.09s)
# test_update_10k_todos ... PASSED (0.02s per operation)
# test_delete_10k_todos ... PASSED (0.01s per operation)
```

### Memory Validation

```bash
# Profile memory usage
python -m memory_profiler src/main.py

# Expected: <50MB total for 10k todos
```

## Code Quality

### Formatting

```bash
# Format code with black
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Linting

```bash
# Run flake8
flake8 src/ tests/

# Expected: 0 violations (PEP8 compliant)
```

### Type Checking

```bash
# Run mypy
mypy src/

# Expected: Success: no issues found
```

## Validation Checklist

Use this checklist to verify Phase I completion:

### Functional Requirements (15/15)

- [ ] FR-001: Add todos with title (required) and description (optional)
- [ ] FR-002: Unique, sequential IDs assigned automatically
- [ ] FR-003: Todos stored in memory during session
- [ ] FR-004: View all todos with complete information
- [ ] FR-005: Mark todos complete/incomplete by ID
- [ ] FR-006: Update todo title/description by ID
- [ ] FR-007: Delete todos by ID
- [ ] FR-008: Title validation (non-empty)
- [ ] FR-009: Clear error messages on failures
- [ ] FR-010: Console-based command interface
- [ ] FR-011: Clear, readable display format
- [ ] FR-012: Todos ordered by creation time
- [ ] FR-013: Handle 10k todos without degradation
- [ ] FR-014: Input sanitization prevents crashes
- [ ] FR-015: Help command shows all operations

### Success Criteria (7/7)

- [ ] SC-001: Add and view todo within 5 seconds
- [ ] SC-002: All CRUD operations performable using help only
- [ ] SC-003: All operations <100ms for 10k todos
- [ ] SC-004: Memory usage <50MB
- [ ] SC-005: 100% of errors have clear messages
- [ ] SC-006: Handle 10k consecutive operations without crashes
- [ ] SC-007: 5 operations correct on first attempt after help

### Code Quality (5/5)

- [ ] Test coverage >80% (pytest --cov)
- [ ] PEP8 compliant (flake8 passes)
- [ ] Type hints on all functions (mypy passes)
- [ ] Black formatted (black --check passes)
- [ ] All tests passing (pytest exits 0)

### Constitution Compliance (8/8)

- [ ] Python 3.13+ only
- [ ] Console-based interface (no GUI)
- [ ] In-memory storage (no persistence)
- [ ] Minimal dependencies (standard library preferred)
- [ ] Cross-platform compatible (Windows, macOS, Linux)
- [ ] Performance <100ms operations, <50MB memory
- [ ] Test-first development followed (Red-Green-Refactor)
- [ ] Modular architecture for Phase II extensibility

## Common Issues & Solutions

### Issue: "Python version 3.13 not found"

**Solution**: Install Python 3.13 from python.org or use pyenv:

```bash
# Using pyenv
pyenv install 3.13.0
pyenv local 3.13.0
```

### Issue: "Import errors when running tests"

**Solution**: Ensure project root is in PYTHONPATH:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

Or use pytest's built-in path handling:

```bash
pytest --import-mode=importlib
```

### Issue: "Performance tests failing (>100ms)"

**Solution**: Check data structure implementation. Should be using dict (O(1)), not list (O(n)).

### Issue: "Memory usage exceeds 50MB"

**Solution**: Profile to identify memory leaks. Likely cause: not clearing references to deleted todos.

## Next Steps

### After Phase I Completion

1. **Create Pull Request**: Merge `001-console-todo-app` branch
2. **Tag Release**: `git tag v1.0.0-phase-i`
3. **Documentation**: Update main README with Phase I completion
4. **Demo**: Prepare demonstration for stakeholders

### Phase II Preparation

When ready to start Phase II (Full-Stack Web App):

1. **Create new feature branch**: `/sp.specify "Phase II: Full-Stack Web Todo App"`
2. **Review data model**: Verify Todo dataclass maps to SQLModel
3. **Plan API endpoints**: CLI commands → REST endpoints
4. **Migration strategy**: Document Phase I → Phase II transition

## Support & Resources

### Documentation

- Feature Spec: `specs/001-console-todo-app/spec.md`
- Implementation Plan: `specs/001-console-todo-app/plan.md`
- Data Model: `specs/001-console-todo-app/data-model.md`
- CLI Contract: `specs/001-console-todo-app/contracts/cli-interface.md`

### Constitution Reference

- Phase I Standards: `.specify/memory/constitution.md#phase-i`
- Core Principles: `.specify/memory/constitution.md#core-principles`
- Testing Requirements: `.specify/memory/constitution.md#test-first-development`

### Command Reference

- Specification: `/sp.specify <description>`
- Planning: `/sp.plan` (current phase)
- Task Generation: `/sp.tasks`
- Implementation: Use Claude Code with `/sp.implement`

## Appendix: Expected Deliverables

### Code Artifacts

- [ ] `src/models/todo.py` - Todo dataclass
- [ ] `src/services/todo_manager.py` - TodoManager class
- [ ] `src/cli/app.py` - REPL interface
- [ ] `src/main.py` - Application entry point

### Test Artifacts

- [ ] `tests/unit/test_todo_model.py` - Unit tests for Todo
- [ ] `tests/unit/test_todo_manager.py` - Unit tests for TodoManager
- [ ] `tests/integration/test_cli.py` - Integration tests for CLI
- [ ] `tests/performance/test_performance.py` - Performance tests

### Documentation Artifacts

- [ ] `README.md` - Project overview and usage
- [ ] `specs/001-console-todo-app/spec.md` - Feature specification
- [ ] `specs/001-console-todo-app/plan.md` - Implementation plan
- [ ] All design documents (research, data-model, contracts, quickstart)

## Conclusion

This quickstart guide provides the foundation for implementing the Phase I console todo application. Follow the Spec-Kit Plus workflow, adhere to the constitution principles, and maintain >80% test coverage to successfully complete Phase I.

**Ready for**: Task generation with `/sp.tasks` command.
