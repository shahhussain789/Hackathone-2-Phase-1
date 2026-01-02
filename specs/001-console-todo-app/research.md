# Research & Technology Decisions: In-Memory Console Todo App (Phase I)

**Feature**: 001-console-todo-app
**Date**: 2026-01-02
**Phase**: 0 (Research & Architecture)

## Executive Summary

This document captures research findings and architectural decisions for Phase I of the Multi-Phase Todo Application. The focus is on establishing a solid foundation with Python 3.13+, console interface, and in-memory storage that can evolve into subsequent phases (web, AI, Kubernetes, cloud).

## Technology Stack Decisions

### Programming Language

**Decision**: Python 3.13+

**Rationale**:
- **Constitution requirement**: Phase I explicitly requires Python 3.11+ (using 3.13 for latest features)
- **Target audience fit**: Python developers reviewing Agentic Dev Stack workflow
- **Type hints improvements**: Python 3.13 includes enhanced type system features for better static analysis
- **Performance**: Improved interpreter performance in 3.13 (faster than 3.11/3.12)
- **Future-proof**: Latest stable version ensures long-term support through Phase II-V
- **Cross-platform**: Native support for Windows, macOS, Linux (constitution requirement)

**Alternatives considered**:
- Python 3.11/3.12: Would work but miss latest improvements
- Other languages (Go, Rust, Node.js): Rejected - constitution mandates Python for Phase I

### Data Structures

**Decision**: Dictionary (dict) for primary storage with sequential ID generation

**Rationale**:
- **O(1) lookup**: Dict provides constant-time access by todo ID (critical for 10k+ todos performance requirement)
- **Memory efficient**: Native Python dict is optimized for memory usage (<50MB budget)
- **Ordered preservation**: Python 3.7+ dicts maintain insertion order (supports creation time ordering requirement FR-012)
- **Simple serialization**: Easy to extend to JSON/database in Phase II
- **Type safety**: Works well with dataclasses and type hints

**Implementation approach**:
```python
# Conceptual structure (not implementation code)
todos: dict[int, Todo] = {}
next_id: int = 1
```

**Alternatives considered**:
- **List**: O(n) lookup, would fail performance requirement for 10k todos
- **OrderedDict**: Redundant in Python 3.7+, dict already ordered
- **SQLite in-memory**: Violates "no database connections" constraint from constitution
- **Custom linked list**: Over-engineering for requirements

### CLI Interface Pattern

**Decision**: Command-based REPL (Read-Eval-Print Loop) with menu system

**Rationale**:
- **Usability principle**: Menu shows available commands, reducing cognitive load
- **Constitution alignment**: "Interfaces must be intuitive" - menu provides discoverability
- **Help command requirement**: FR-015 requires help showing all operations
- **Error handling**: REPL allows graceful error recovery without app restart
- **Session continuity**: Maintains in-memory state across commands during session

**Command structure**:
```
Main Menu:
1. Add todo
2. View all todos
3. Update todo
4. Delete todo
5. Mark todo complete/incomplete
6. Help
7. Exit

Choice: _
```

**Alternatives considered**:
- **CLI flags** (e.g., `todo.py --add "title"`): Poor for multi-operation sessions, loses in-memory state
- **Interactive prompts per operation**: More verbose, harder to automate testing
- **Natural language**: Reserved for Phase III (AI-powered chatbot)

### Input Validation Strategy

**Decision**: Centralized validation with custom exception hierarchy

**Rationale**:
- **Reliability principle**: "Handle errors gracefully, ensure consistent behavior"
- **Clear error messages**: FR-009 requires actionable error messages
- **DRY principle**: Single source of truth for validation rules
- **Testability**: Easy to unit test validation logic separately
- **Extensibility**: Custom exceptions support future error handling enhancements

**Exception hierarchy**:
```python
class TodoError(Exception): pass
class TodoNotFoundError(TodoError): pass
class InvalidInputError(TodoError): pass
class EmptyTitleError(InvalidInputError): pass
```

**Alternatives considered**:
- **Return codes**: Less Pythonic, harder to trace errors
- **Generic exceptions**: Poor error messages, violates FR-009
- **Inline validation**: Code duplication, hard to maintain

### Testing Framework

**Decision**: pytest with coverage.py

**Rationale**:
- **Constitution requirement**: "Unit tests required for all CRUD operations, >80% coverage"
- **Industry standard**: pytest is the de facto testing framework for Python
- **Rich assertions**: Better error messages than unittest
- **Fixtures**: Simplifies test setup/teardown for in-memory state
- **Coverage integration**: coverage.py integrates seamlessly with pytest
- **Parameterized tests**: Efficiently test edge cases (empty input, invalid IDs, etc.)

**Test categories**:
1. **Unit tests**: Todo class, validation functions, CLI command handlers
2. **Integration tests**: Full command flows (add → view → update → delete)
3. **Performance tests**: 10k todos operations <100ms (SC-003)
4. **Edge case tests**: Empty input, invalid IDs, special characters

**Alternatives considered**:
- **unittest**: More verbose, less ergonomic fixtures
- **doctest**: Insufficient for complex test scenarios
- **nose**: Deprecated, pytest is the modern choice

### Code Quality Tools

**Decision**: black (formatting), flake8 (linting), mypy (type checking)

**Rationale**:
- **Constitution requirement**: "PEP8 compliance" for Python code
- **black**: Opinionated formatter, eliminates formatting debates
- **flake8**: Catches PEP8 violations, code smells
- **mypy**: Static type checking with Python 3.13 type hints
- **CI/CD ready**: All tools support automated checks

**Configuration**:
- black: default settings (88 char line length)
- flake8: E203, W503 ignored (black compatibility)
- mypy: strict mode with explicit type hints required

**Alternatives considered**:
- **pylint**: More opinionated, slower, flake8 sufficient for Phase I
- **autopep8**: Less consistent than black
- **Manual review only**: Doesn't scale, human error-prone

## Architecture Decisions

### Module Structure

**Decision**: Three-layer architecture (models, services, CLI)

**Rationale**:
- **Modularity principle**: "Components must be loosely coupled with clear interfaces"
- **Extensibility principle**: "Designed to integrate new technologies in subsequent phases"
- **Separation of concerns**: Data model, business logic, presentation cleanly separated
- **Testability**: Each layer can be tested independently
- **Phase II migration**: Easy to replace CLI layer with FastAPI, keep models/services

**Structure**:
```
src/
├── models/
│   └── todo.py          # Todo dataclass, validation
├── services/
│   └── todo_manager.py  # CRUD operations, business logic
├── cli/
│   └── app.py           # REPL interface, command handlers
└── main.py              # Entry point
```

**Alternatives considered**:
- **Single file**: Violates modularity, hard to test, doesn't scale to Phase II
- **More layers** (repository, DTO): Over-engineering for Phase I requirements
- **Functional approach**: Less natural for CRUD operations, harder to extend

### Error Handling Strategy

**Decision**: Try-except at CLI boundary, raise exceptions in services

**Rationale**:
- **User experience**: Catch all errors at CLI, show friendly messages
- **Service purity**: Services raise exceptions, don't print to console
- **Testability**: Services can be tested without capturing stdout
- **Logging**: Errors logged before user-friendly message shown

**Pattern**:
```python
# Service layer
def delete_todo(todo_id: int) -> None:
    if todo_id not in todos:
        raise TodoNotFoundError(f"Todo {todo_id} not found")
    # ... deletion logic

# CLI layer
try:
    service.delete_todo(todo_id)
    print("✓ Todo deleted successfully")
except TodoNotFoundError as e:
    print(f"✗ Error: {e}")
```

**Alternatives considered**:
- **Return None/False on error**: Ambiguous, loses error context
- **Print errors in service**: Couples service to console, hard to test
- **Global error handler**: Over-engineering for Phase I

### Performance Optimization Strategy

**Decision**: Lazy evaluation with efficient data structures, profile if needed

**Rationale**:
- **Performance principle**: "<100ms operation latency, <50MB memory"
- **Premature optimization**: Start with clean code, optimize if benchmarks fail
- **Profiling approach**: Use cProfile/memory_profiler if SC-003 not met
- **Efficient structures**: Dict (O(1)) already optimal for requirements

**Benchmarking plan**:
1. Create 10k todos
2. Measure each operation (add, view, update, delete, mark complete)
3. Verify all operations <100ms
4. Measure memory usage with memory_profiler
5. Optimize only if requirements not met

**Alternatives considered**:
- **Upfront optimization**: Premature, adds complexity
- **No performance testing**: Violates SC-003, SC-004 requirements
- **C extensions**: Massive over-engineering for in-memory dict operations

## Development Workflow Decisions

### Version Control Strategy

**Decision**: Git with feature branch workflow (already on 001-console-todo-app)

**Rationale**:
- **Spec-Kit Plus workflow**: Spec → Plan → Tasks → Implementation
- **Constitution compliance**: Code review requirements need branches
- **Phase II readiness**: Branch supports clean PR for Phase I completion

**Commit strategy**:
- Test commits first (TDD: Red-Green-Refactor)
- Implementation commits reference tasks
- Follow conventional commits format

**Alternatives considered**:
- **Trunk-based**: Too simple for multi-phase project
- **Gitflow**: Over-engineering for single-developer Phase I

### Development Environment

**Decision**: Cross-platform with minimal dependencies

**Rationale**:
- **Constitution constraint**: "Platform: Cross-platform (Windows, macOS, Linux)"
- **Target audience**: Python developers on various platforms
- **Minimal dependencies**: Standard library preferred per constitution

**Requirements**:
- Python 3.13+ (runtime)
- pytest, coverage.py (testing)
- black, flake8, mypy (optional, code quality)

**Alternatives considered**:
- **Docker environment**: Over-engineering for Phase I, reserved for Phase IV
- **Virtual environment**: Recommended but not enforced (user choice)

## Risk Mitigation

### Performance Risk: Large Todo Lists

**Risk**: Operations slow with 10k+ todos

**Mitigation**:
- Dict provides O(1) lookup (architecture decision)
- Performance tests verify <100ms requirement
- Profiling plan ready if benchmarks fail

### Memory Risk: Approaching 50MB Limit

**Risk**: Large descriptions push memory usage over budget

**Mitigation**:
- Memory profiler in test suite
- Document practical limits in README
- Description length warnings if memory monitoring shows issues

### Cross-Platform Risk: Platform-Specific Behavior

**Risk**: Console behavior differs on Windows vs Linux/macOS

**Mitigation**:
- Use platform-agnostic Python features (input(), print())
- Test on Windows, macOS, Linux before Phase I completion
- Avoid platform-specific console codes (colors, clearing)

### Input Validation Risk: Edge Cases

**Risk**: Special characters, Unicode, very long strings break app

**Mitigation**:
- Comprehensive edge case tests (FR-014 requirement)
- Input sanitization in validation layer
- Exception handling at CLI boundary

## Phase II Migration Considerations

### Extensibility Planning

**Decision**: Design interfaces that anticipate Phase II needs

**Rationale**:
- **Extensibility principle**: "Architecture must be designed to integrate new technologies"
- **Modularity principle**: "Code structured for easy upgrades across phases"

**Phase II readiness**:
1. **TodoManager interface**: Can swap in-memory dict for database repository
2. **Todo model**: Directly maps to SQLModel entities (Phase II tech stack)
3. **Validation logic**: Reusable in FastAPI endpoints
4. **Test suite**: Becomes contract tests for API in Phase II

**Not implementing now**:
- Abstract base classes (YAGNI for Phase I)
- Database schema (out of scope per constitution)
- API contracts (Phase II concern)

## Conclusion

All technology decisions align with:
- ✅ Constitution Phase I requirements (Python 3.13+, console, in-memory, <50MB, <100ms)
- ✅ Functional requirements (15 FRs from spec)
- ✅ Success criteria (7 SCs from spec)
- ✅ Core principles (Functionality, Modularity, Reliability, Extensibility, Usability, Performance, Test-First)

**Ready for Phase 1**: Data model design and contract definition.
