# Implementation Plan: In-Memory Console Todo App (Phase I)

**Branch**: `001-console-todo-app` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo-app/spec.md`

**Note**: This plan was created by the `/sp.plan` command following the Spec-Kit Plus methodology.

## Summary

Build a console-based todo application with in-memory storage for Phase I of the Multi-Phase Todo Application project. Target audience is Python developers evaluating the Agentic Dev Stack workflow (Claude Code + Spec-Kit Plus). Core functionality includes CRUD operations (Add, View, Update, Delete, Mark Complete) via a menu-driven REPL interface with comprehensive input validation and error handling.

**Technical Approach**: Three-layer architecture (models, services, CLI) using Python 3.13+, dataclasses for the Todo entity, dict-based in-memory storage for O(1) lookup performance, and pytest for >80% test coverage. Design prioritizes modularity and extensibility to support Phase II migration to FastAPI/SQLModel/Neon DB without architectural rewrites.

## Technical Context

**Language/Version**: Python 3.13+ (latest stable for enhanced type system and performance improvements)

**Primary Dependencies**:
- Python standard library (core functionality - no external dependencies)
- pytest (testing framework - development only)
- coverage.py (test coverage reporting - development only)
- black, flake8, mypy (code quality tools - optional)

**Storage**: In-memory dict (key=todo_id:int, value=Todo dataclass) - no persistence, no database

**Testing**: pytest with fixtures for in-memory state, >80% coverage requirement, performance tests for 10k todos

**Target Platform**: Cross-platform (Windows, macOS, Linux) via Python standard library

**Project Type**: Single project (console application)

**Performance Goals**:
- <100ms operation latency for all CRUD operations with up to 10,000 todos (SC-003)
- <50MB total application memory usage (SC-004, Phase I constitution requirement)
- Instant menu display (<10ms)

**Constraints**:
- Console-only interface (no GUI, no web)
- In-memory storage only (no file I/O, no database)
- Single-user, single-process operation
- Minimal external dependencies (standard library preferred)
- Cross-platform compatibility required
- 1 week timeline from specification approval

**Scale/Scope**:
- Support up to 10,000 todos without performance degradation
- 15 functional requirements
- 4 prioritized user stories (P1-P4)
- 7 measurable success criteria

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Requirements (from Constitution)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| **Language: Python 3.11+** | ✅ PASS | Using Python 3.13+ (spec, research.md) |
| **Interface: Console-based only** | ✅ PASS | REPL menu interface (cli-interface.md) |
| **Storage: In-memory only** | ✅ PASS | Dict-based storage, no persistence (data-model.md) |
| **Core Features: Add, Update, Delete, List, Mark Complete** | ✅ PASS | All 5 features in functional requirements (spec.md) |
| **Testing: Unit tests, >80% coverage** | ✅ PASS | pytest planned, coverage requirement in testing strategy (research.md, quickstart.md) |
| **Dependencies: Minimal, standard library preferred** | ✅ PASS | Zero production dependencies, pytest for dev only (research.md) |
| **Constraints: No web, no database, no file I/O** | ✅ PASS | Console REPL, in-memory dict, no persistence (all design docs) |

### Core Principles (from Constitution)

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. Functionality** | ✅ PASS | All 15 FRs testable and measurable (spec.md) |
| **II. Modularity** | ✅ PASS | Three-layer architecture (models, services, CLI) with clear interfaces (research.md) |
| **III. Reliability** | ✅ PASS | Comprehensive error handling, input validation, custom exception hierarchy (research.md, data-model.md) |
| **IV. Extensibility** | ✅ PASS | Design anticipates Phase II migration to FastAPI/SQLModel (research.md "Phase II Migration") |
| **V. Usability** | ✅ PASS | Menu-driven REPL, help command, clear error messages (cli-interface.md) |
| **VI. Performance** | ✅ PASS | <100ms ops, <50MB memory, dict for O(1) lookup (data-model.md, research.md) |
| **VII. Test-First Development** | ✅ PASS | TDD workflow planned: Red-Green-Refactor (quickstart.md "Development Workflow") |

### Gate Result: ✅ PASS - Proceed with Phase 0 Research

**Post-Phase 1 Re-check**: ✅ PASS - All design decisions align with constitution principles and Phase I requirements. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── plan.md                         # This file (/sp.plan command output)
├── spec.md                         # Feature specification (/sp.specify output)
├── research.md                     # Phase 0 research & technology decisions
├── data-model.md                   # Phase 1 data model design
├── quickstart.md                   # Phase 1 development guide
├── contracts/
│   └── cli-interface.md           # CLI command specifications
├── checklists/
│   └── requirements.md             # Specification quality checklist (from /sp.specify)
└── tasks.md                        # Phase 2 task breakdown (/sp.tasks - NOT YET CREATED)
```

### Source Code (repository root)

**Selected Structure**: Option 1 - Single project (console application)

```text
src/
├── models/
│   └── todo.py                    # Todo dataclass, validation logic, custom exceptions
├── services/
│   └── todo_manager.py            # TodoManager class: CRUD operations, business logic
├── cli/
│   └── app.py                     # REPL interface, menu display, command handlers
└── main.py                        # Application entry point, starts REPL

tests/
├── unit/
│   ├── test_todo_model.py         # Unit tests for Todo dataclass and validation
│   └── test_todo_manager.py       # Unit tests for TodoManager CRUD operations
├── integration/
│   └── test_cli.py                # Integration tests for full command flows
└── performance/
    └── test_performance.py        # Performance tests for 10k todos (<100ms requirement)

specs/                             # Design documentation (shown above)

.specify/                          # Spec-Kit Plus templates and scripts
├── memory/
│   └── constitution.md            # Project constitution
├── templates/
│   ├── spec-template.md
│   ├── plan-template.md
│   └── tasks-template.md
└── scripts/
    └── powershell/
        ├── create-new-feature.ps1
        ├── setup-plan.ps1
        └── update-agent-context.ps1

history/prompts/
├── constitution/
│   └── 001-multi-phase-todo-constitution.constitution.prompt.md
└── 001-console-todo-app/
    ├── 001-phase-i-spec.spec.prompt.md
    └── [plan PHR will be added here]

README.md                          # Project overview and usage instructions
pyproject.toml                     # Python project configuration (optional)
.gitignore                         # Git ignore rules
```

**Structure Decision**: Single project structure selected because:
- Phase I is a standalone console application (no frontend/backend split)
- No web components (reserved for Phase II)
- No mobile components (reserved for future phases)
- Simple hierarchy supports the Modularity principle (clear layer separation)
- Easy to extend in Phase II by adding `backend/` and `frontend/` directories

**Layer Responsibilities**:
- **models/**: Data entities, validation rules, exception definitions
- **services/**: Business logic, CRUD operations, state management
- **cli/**: User interface, input/output, command routing
- **main.py**: Entry point, application bootstrap

## Complexity Tracking

> **No violations** - Constitution Check passed without exceptions. This section is empty.

## Phase 0: Research & Technology Decisions

**Status**: ✅ Completed
**Artifact**: [research.md](./research.md)

### Key Decisions

1. **Data Structure**: Dict for O(1) lookup (performance requirement)
2. **CLI Pattern**: Menu-driven REPL (usability, discoverability)
3. **Validation**: Custom exception hierarchy (reliability, clear errors)
4. **Testing**: pytest + coverage.py (constitution requirement)
5. **Architecture**: Three-layer separation (modularity, extensibility)

### Rationale Summary

All decisions documented in research.md with:
- Decision statement
- Rationale (why this choice)
- Alternatives considered (what was rejected and why)
- Phase II migration considerations

## Phase 1: Design & Contracts

**Status**: ✅ Completed
**Artifacts**: [data-model.md](./data-model.md), [contracts/cli-interface.md](./contracts/cli-interface.md), [quickstart.md](./quickstart.md)

### Data Model Summary

**Entity**: Todo
- Attributes: id (int), title (str), description (str), completed (bool), created_at (datetime)
- Validation: Title non-empty (max 200), description optional (max 2000), special chars allowed
- Storage: Dict mapping id→Todo, sequential ID generation
- Performance: O(1) lookup, <400 bytes per todo, supports 100k+ todos in <50MB

### CLI Contract Summary

**Commands** (7 total):
1. Add new todo (title required, description optional)
2. View all todos (ordered by creation time)
3. Update todo (by ID, title and/or description)
4. Delete todo (by ID, requires confirmation)
5. Mark complete/incomplete (by ID, toggleable)
6. Help (shows all commands and usage)
7. Exit (clears data, requires confirmation)

**Error Handling**: Try-except at CLI boundary, friendly error messages, no crashes from user input

**Performance**: All operations <100ms for 10k todos, verified via performance tests

### Quickstart Guide Summary

Development workflow documented:
- Prerequisites (Python 3.13+, pytest)
- Project structure walkthrough
- Example usage session
- TDD cycle (Red-Green-Refactor)
- Validation checklist (15 FRs, 7 SCs, 8 constitution requirements)

## Implementation Strategy

### Test-First Development (TDD)

Per Constitution Principle VII:

1. **Red**: Write failing tests first
   - Unit tests for Todo model validation
   - Unit tests for TodoManager CRUD operations
   - Integration tests for CLI command flows
   - Performance tests for 10k todos

2. **Green**: Implement minimal code to pass tests
   - Todo dataclass with validation
   - TodoManager service with dict storage
   - REPL interface with command handlers

3. **Refactor**: Clean up while keeping tests green
   - Extract common validation logic
   - Improve error messages
   - Optimize performance if needed

### Development Order

Recommended sequence (aligned with user story priorities P1-P4):

**Foundation** (required for all user stories):
1. Todo dataclass (models/todo.py)
2. Custom exceptions (models/todo.py)
3. TodoManager base structure (services/todo_manager.py)
4. REPL framework (cli/app.py)

**P1: Add and View Todos** (MVP):
1. Tests: test_add_todo, test_view_todos
2. Implementation: add_todo(), list_todos()
3. CLI: Commands 1, 2

**P2: Mark Complete**:
1. Tests: test_mark_complete, test_toggle_status
2. Implementation: mark_complete()
3. CLI: Command 5

**P3: Update Todo**:
1. Tests: test_update_todo, test_partial_update
2. Implementation: update_todo()
3. CLI: Command 3

**P4: Delete Todo**:
1. Tests: test_delete_todo, test_delete_confirmation
2. Implementation: delete_todo()
3. CLI: Command 4

**Polish**:
1. Help command (Command 6)
2. Exit with confirmation (Command 7)
3. Performance tests (10k todos)
4. Memory profiling
5. Code quality (black, flake8, mypy)

### File Implementation Order

```
1. src/models/todo.py              # Data model foundation
2. tests/unit/test_todo_model.py   # Model tests (TDD: write first)
3. src/services/todo_manager.py    # Business logic
4. tests/unit/test_todo_manager.py # Service tests (TDD: write first)
5. src/cli/app.py                  # User interface
6. tests/integration/test_cli.py   # CLI tests
7. src/main.py                     # Entry point
8. tests/performance/test_performance.py  # Performance validation
9. README.md                       # User documentation
```

## Testing Strategy

### Coverage Requirements

- **Minimum**: 80% (constitution requirement)
- **Target**: 90%+ for core logic (models, services)
- **Exclusions**: main.py entry point, __init__ files

### Test Categories

| Category | Purpose | Example Tests |
|----------|---------|---------------|
| **Unit - Models** | Todo validation, state transitions | Empty title raises error, max length validation |
| **Unit - Services** | CRUD operations, business logic | Add todo returns correct ID, delete removes from storage |
| **Integration - CLI** | Full command flows | Add → view → update → delete workflow |
| **Performance** | 10k todos <100ms requirement | Measure add/view/update/delete with 10k todos |
| **Edge Cases** | Special chars, invalid IDs, empty input | Unicode in title, ID=999 not found |

### Test Execution

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=term-missing --cov-report=html

# Performance tests only
pytest tests/performance/ -v

# Fast tests only (exclude slow performance tests)
pytest -m "not slow"
```

## Performance Validation

### Benchmarking Plan

**Scenario**: 10,000 todos in memory

**Operations to measure**:
1. Add todo: Should be <0.1ms (dict insert)
2. View all todos: Should be <100ms (iterate 10k items)
3. Update todo: Should be <0.1ms (dict lookup + update)
4. Delete todo: Should be <0.1ms (dict delete)
5. Mark complete: Should be <0.1ms (dict lookup + boolean toggle)

**Tools**:
- `time.perf_counter()` for operation timing
- `memory_profiler` for memory usage
- pytest markers for performance tests

**Acceptance Criteria**:
- All operations <100ms for 10k todos (SC-003)
- Total memory <50MB with 10k todos (SC-004)

### Memory Profiling

```python
# Example performance test structure (conceptual)
def test_10k_todos_performance():
    manager = TodoManager()

    # Add 10k todos
    start = time.perf_counter()
    for i in range(10000):
        manager.add_todo(f"Todo {i}", f"Description {i}")
    add_time = time.perf_counter() - start
    assert add_time < 1.0  # 10k adds in <1s = <0.1ms per add

    # View all
    start = time.perf_counter()
    todos = manager.list_todos()
    view_time = time.perf_counter() - start
    assert view_time < 0.1  # <100ms

    # Update
    start = time.perf_counter()
    manager.update_todo(5000, "Updated title", "Updated description")
    update_time = time.perf_counter() - start
    assert update_time < 0.001  # <1ms
```

## Code Quality Standards

### PEP8 Compliance

- **Formatter**: black (88 char line length)
- **Linter**: flake8 with E203, W503 ignored (black compatibility)
- **Target**: 0 violations

### Type Hints

- **Type checker**: mypy in strict mode
- **Coverage**: All function signatures, class attributes
- **Target**: mypy passes with no errors

```python
# Example type hints
from typing import Optional

class TodoManager:
    def add_todo(self, title: str, description: str = "") -> Todo:
        ...

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        ...

    def update_todo(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Todo:
        ...
```

### Documentation

- **Docstrings**: All public classes and functions
- **Format**: Google-style docstrings
- **Content**: Brief description, args, returns, raises

```python
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
```

## Phase II Migration Readiness

### Extensibility Considerations

**Design decisions supporting Phase II**:

1. **TodoManager as interface**: Can swap dict storage for database repository
   ```python
   # Phase I
   class TodoManager:
       def __init__(self):
           self._todos: dict[int, Todo] = {}

   # Phase II (conceptual)
   class TodoManager:
       def __init__(self, session: Session):
           self._session = session  # SQLModel database session
   ```

2. **Todo dataclass → SQLModel**: Direct mapping with minimal changes
   ```python
   # Phase I (dataclass)
   @dataclass
   class Todo:
       id: int
       title: str
       # ...

   # Phase II (SQLModel)
   class Todo(SQLModel, table=True):
       id: Optional[int] = Field(primary_key=True)
       title: str = Field(max_length=200)
       # ...
   ```

3. **CLI commands → API endpoints**: Command handlers become controller functions
   ```python
   # Phase I (CLI)
   def handle_add_todo():
       title = input("Enter title: ")
       todo = manager.add_todo(title)
       print(f"✓ Todo added: {todo.id}")

   # Phase II (FastAPI)
   @app.post("/api/todos")
   def create_todo(request: TodoCreate):
       todo = manager.add_todo(request.title, request.description)
       return todo
   ```

4. **Validation logic**: Reusable in FastAPI request validation
   - EmptyTitleError → 400 Bad Request
   - TodoNotFoundError → 404 Not Found
   - Same error messages in API responses

### Not Implementing (YAGNI)

**Avoiding over-engineering**:
- ❌ Abstract base classes for TodoManager (no alternate implementations in Phase I)
- ❌ Repository pattern (dict IS the repository for in-memory)
- ❌ Dependency injection (single TodoManager instance sufficient)
- ❌ Configuration files (no configurable settings yet)
- ❌ Logging infrastructure (print() sufficient for console app)

These will be added in Phase II when actually needed.

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation | Verification |
|------|-----------|--------|------------|--------------|
| Performance degradation with 10k todos | Low | Medium | Dict for O(1) lookup, performance tests | pytest tests/performance/ |
| Memory exceeds 50MB budget | Low | Low | 400 bytes/todo supports 100k todos | memory_profiler during tests |
| Cross-platform console issues | Low | Medium | Platform-agnostic Python features, test on Win/Mac/Linux | Manual testing on 3 platforms |
| Input validation gaps | Medium | Medium | Comprehensive edge case tests, fuzzing with special chars | pytest with edge case fixtures |
| Test coverage <80% | Low | High | TDD enforced, coverage.py monitoring, CI checks | pytest --cov threshold |

## Deliverables Checklist

### Code Artifacts

- [ ] `src/models/todo.py` - Todo dataclass with validation
- [ ] `src/services/todo_manager.py` - TodoManager with CRUD operations
- [ ] `src/cli/app.py` - REPL interface and command handlers
- [ ] `src/main.py` - Application entry point

### Test Artifacts

- [ ] `tests/unit/test_todo_model.py` - Todo model unit tests
- [ ] `tests/unit/test_todo_manager.py` - TodoManager unit tests
- [ ] `tests/integration/test_cli.py` - CLI integration tests
- [ ] `tests/performance/test_performance.py` - Performance validation tests
- [ ] Coverage report >80%

### Documentation Artifacts

- [ ] `README.md` - Project overview, installation, usage
- [ ] `specs/001-console-todo-app/spec.md` - Feature specification ✅
- [ ] `specs/001-console-todo-app/plan.md` - This file ✅
- [ ] `specs/001-console-todo-app/research.md` - Technology decisions ✅
- [ ] `specs/001-console-todo-app/data-model.md` - Data model design ✅
- [ ] `specs/001-console-todo-app/quickstart.md` - Development guide ✅
- [ ] `specs/001-console-todo-app/contracts/cli-interface.md` - CLI contract ✅
- [ ] `specs/001-console-todo-app/tasks.md` - Task breakdown (next: /sp.tasks)

### Quality Gates

- [ ] All 15 functional requirements implemented and tested
- [ ] All 7 success criteria met and verified
- [ ] pytest passes (exit code 0)
- [ ] Coverage >80% (pytest --cov)
- [ ] flake8 passes (0 violations)
- [ ] mypy passes (0 errors)
- [ ] black formatted (--check passes)
- [ ] Performance tests pass (<100ms, <50MB)
- [ ] Manual testing on Windows, macOS, Linux

## Next Steps

### Immediate (Current Phase)

1. **Generate tasks**: Run `/sp.tasks` to create actionable task breakdown
2. **Review tasks**: Validate task order, dependencies, and completeness
3. **Begin implementation**: Follow TDD workflow (Red-Green-Refactor)

### Implementation Phase

1. **Setup project structure**: Create src/, tests/ directories
2. **Implement P1 (MVP)**: Add and View todos (highest priority)
3. **Validate MVP**: Ensure basic functionality works end-to-end
4. **Implement P2-P4**: Mark complete, Update, Delete (in priority order)
5. **Polish**: Help, Exit, performance optimization, documentation

### Completion Phase

1. **Validation**: Run full test suite, coverage report, quality checks
2. **Documentation**: Complete README with usage examples
3. **Demo**: Prepare demonstration for stakeholders
4. **Pull Request**: Merge `001-console-todo-app` branch to main
5. **Tag Release**: `git tag v1.0.0-phase-i`
6. **Retrospective**: Document lessons learned for Phase II

### Phase II Preparation

- Review Phase II constitution requirements (FastAPI, Next.js, Neon DB)
- Plan data migration strategy (though Phase I has no persisted data)
- Design API endpoints based on CLI command mapping
- Prepare Phase II specification

## Conclusion

This implementation plan provides:
- ✅ Complete technical context and architecture decisions
- ✅ Constitution compliance validation (all gates passed)
- ✅ Detailed design artifacts (research, data model, contracts, quickstart)
- ✅ Clear implementation strategy with TDD workflow
- ✅ Performance and quality validation approach
- ✅ Phase II extensibility considerations
- ✅ Risk mitigation and deliverables checklist

**Ready for**: Task generation (`/sp.tasks`) and implementation phase.

**Design artifacts location**: `specs/001-console-todo-app/`
- research.md (technology decisions)
- data-model.md (entity design)
- contracts/cli-interface.md (command specifications)
- quickstart.md (development guide)

**Next command**: `/sp.tasks` to generate actionable, dependency-ordered tasks from this plan.
