---

description: "Task list for In-Memory Console Todo App (Phase I)"
---

# Tasks: In-Memory Console Todo App (Phase I)

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/cli-interface.md

**Tests**: Constitution Principle VII requires Test-First Development (TDD). Tests are MANDATORY and must be written before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths assume single project structure per plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/, tests/, docs/)
- [ ] T002 [P] Create __init__.py files for src/models/, src/services/, src/cli/
- [ ] T003 [P] Create __init__.py files for tests/unit/, tests/integration/, tests/performance/
- [ ] T004 [P] Create .gitignore for Python (\_\_pycache\_\_, .pytest_cache, .coverage, htmlcov/)
- [ ] T005 [P] Create pyproject.toml or setup.py with project metadata and dev dependencies (pytest, coverage, black, flake8, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 [P] Create custom exception classes in src/models/todo.py (TodoError, TodoNotFoundError, InvalidInputError, EmptyTitleError)
- [ ] T007 Create Todo dataclass in src/models/todo.py with all attributes (id, title, description, completed, created_at)
- [ ] T008 Add validation logic to Todo dataclass (__post_init__ method for title/description validation)
- [ ] T009 Create TodoManager class skeleton in src/services/todo_manager.py with __init__ method (initialize empty dict and next_id counter)
- [ ] T010 Create REPL framework in src/cli/app.py (display_menu function, main_loop function skeleton)
- [ ] T011 Create application entry point in src/main.py (imports TodoManager and starts REPL)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add todos and view their list (core value proposition)

**Independent Test**: Launch app, add 2-3 todos, view list, verify all items displayed with correct details

### Tests for User Story 1 (TDD: Write FIRST, ensure FAIL before implementation) ⚠️

- [ ] T012 [P] [US1] Write unit test for Todo creation with valid title and description in tests/unit/test_todo_model.py
- [ ] T013 [P] [US1] Write unit test for Todo creation with title only (description defaults to empty) in tests/unit/test_todo_model.py
- [ ] T014 [P] [US1] Write unit test for empty title validation (should raise EmptyTitleError) in tests/unit/test_todo_model.py
- [ ] T015 [P] [US1] Write unit test for title max length validation (200 chars) in tests/unit/test_todo_model.py
- [ ] T016 [P] [US1] Write unit test for TodoManager.add_todo() with valid inputs in tests/unit/test_todo_manager.py
- [ ] T017 [P] [US1] Write unit test for TodoManager.add_todo() assigns sequential IDs in tests/unit/test_todo_manager.py
- [ ] T018 [P] [US1] Write unit test for TodoManager.list_todos() returns empty list initially in tests/unit/test_todo_manager.py
- [ ] T019 [P] [US1] Write unit test for TodoManager.list_todos() returns todos in creation order in tests/unit/test_todo_manager.py
- [ ] T020 [P] [US1] Write integration test for add-then-view workflow in tests/integration/test_cli.py

**Run tests - ALL SHOULD FAIL** (Red phase of TDD)

### Implementation for User Story 1

- [ ] T021 [US1] Implement add_todo(title, description) method in src/services/todo_manager.py (create Todo, assign ID, store in dict, increment next_id)
- [ ] T022 [US1] Implement list_todos() method in src/services/todo_manager.py (return list of todos in creation order)
- [ ] T023 [US1] Implement handle_add_todo() command handler in src/cli/app.py (prompt for title/description, call add_todo, display success)
- [ ] T024 [US1] Implement handle_view_todos() command handler in src/cli/app.py (call list_todos, format and display todos with ID, title, description, status, created_at)
- [ ] T025 [US1] Update main_loop() in src/cli/app.py to route menu choice 1 to handle_add_todo
- [ ] T026 [US1] Update main_loop() in src/cli/app.py to route menu choice 2 to handle_view_todos

**Run tests - ALL SHOULD PASS** (Green phase of TDD)

- [ ] T027 [US1] Refactor: Extract validation logic if duplicated, improve error messages, optimize if needed

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (MVP ready!)

---

## Phase 4: User Story 2 - Mark Todos Complete (Priority: P2)

**Goal**: Enable users to mark todos as complete/incomplete (progress tracking)

**Independent Test**: Create 3 todos, mark 2 as complete, view list, verify completion status correctly shown

### Tests for User Story 2 (TDD: Write FIRST, ensure FAIL before implementation) ⚠️

- [ ] T028 [P] [US2] Write unit test for marking todo as complete in tests/unit/test_todo_manager.py
- [ ] T029 [P] [US2] Write unit test for toggling todo from complete to incomplete in tests/unit/test_todo_manager.py
- [ ] T030 [P] [US2] Write unit test for marking non-existent todo (should raise TodoNotFoundError) in tests/unit/test_todo_manager.py
- [ ] T031 [P] [US2] Write integration test for mark-complete workflow in tests/integration/test_cli.py

**Run tests - ALL SHOULD FAIL** (Red phase of TDD)

### Implementation for User Story 2

- [ ] T032 [US2] Implement mark_complete(todo_id, completed) method in src/services/todo_manager.py (lookup todo, update status, handle not found)
- [ ] T033 [US2] Implement handle_mark_complete() command handler in src/cli/app.py (prompt for ID and status, call mark_complete, display success/error)
- [ ] T034 [US2] Update main_loop() in src/cli/app.py to route menu choice 5 to handle_mark_complete
- [ ] T035 [US2] Update handle_view_todos() to clearly display completion status (use ☑ for complete, ☐ for incomplete)

**Run tests - ALL SHOULD PASS** (Green phase of TDD)

- [ ] T036 [US2] Refactor: Optimize completion status display formatting if needed

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Todo Details (Priority: P3)

**Goal**: Enable users to update todo title and description (task refinement)

**Independent Test**: Create todo, update title and description, view to verify changes

### Tests for User Story 3 (TDD: Write FIRST, ensure FAIL before implementation) ⚠️

- [ ] T037 [P] [US3] Write unit test for updating todo title only in tests/unit/test_todo_manager.py
- [ ] T038 [P] [US3] Write unit test for updating todo description only in tests/unit/test_todo_manager.py
- [ ] T039 [P] [US3] Write unit test for updating both title and description in tests/unit/test_todo_manager.py
- [ ] T040 [P] [US3] Write unit test for updating with empty title (should raise EmptyTitleError) in tests/unit/test_todo_manager.py
- [ ] T041 [P] [US3] Write unit test for updating non-existent todo (should raise TodoNotFoundError) in tests/unit/test_todo_manager.py
- [ ] T042 [P] [US3] Write integration test for update workflow in tests/integration/test_cli.py

**Run tests - ALL SHOULD FAIL** (Red phase of TDD)

### Implementation for User Story 3

- [ ] T043 [US3] Implement update_todo(todo_id, title, description) method in src/services/todo_manager.py (lookup todo, validate, update fields, handle not found)
- [ ] T044 [US3] Implement handle_update_todo() command handler in src/cli/app.py (prompt for ID, show current values, prompt for new values, call update_todo)
- [ ] T045 [US3] Update main_loop() in src/cli/app.py to route menu choice 3 to handle_update_todo

**Run tests - ALL SHOULD PASS** (Green phase of TDD)

- [ ] T046 [US3] Refactor: Extract input validation helper if code is duplicated

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional

---

## Phase 6: User Story 4 - Delete Todos (Priority: P4)

**Goal**: Enable users to delete todos (list cleanup and management)

**Independent Test**: Create 4 todos, delete 2 specific ones, view list to verify removal

### Tests for User Story 4 (TDD: Write FIRST, ensure FAIL before implementation) ⚠️

- [ ] T047 [P] [US4] Write unit test for deleting existing todo in tests/unit/test_todo_manager.py
- [ ] T048 [P] [US4] Write unit test for deleting non-existent todo (should raise TodoNotFoundError) in tests/unit/test_todo_manager.py
- [ ] T049 [P] [US4] Write unit test for deleting middle todo preserves other IDs in tests/unit/test_todo_manager.py
- [ ] T050 [P] [US4] Write integration test for delete workflow with confirmation in tests/integration/test_cli.py

**Run tests - ALL SHOULD FAIL** (Red phase of TDD)

### Implementation for User Story 4

- [ ] T051 [US4] Implement delete_todo(todo_id) method in src/services/todo_manager.py (lookup, remove from dict, handle not found)
- [ ] T052 [US4] Implement handle_delete_todo() command handler in src/cli/app.py (prompt for ID, confirm deletion, call delete_todo, display success/error)
- [ ] T053 [US4] Update main_loop() in src/cli/app.py to route menu choice 4 to handle_delete_todo

**Run tests - ALL SHOULD PASS** (Green phase of TDD)

- [ ] T054 [US4] Refactor: Consolidate confirmation prompt logic if used elsewhere

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final touches

- [ ] T055 [P] Implement handle_help() command handler in src/cli/app.py (display all commands with usage from CLI contract)
- [ ] T056 [P] Implement handle_exit() command handler in src/cli/app.py (confirm exit, clear data warning)
- [ ] T057 Update main_loop() in src/cli/app.py to route menu choices 6 (Help) and 7 (Exit)
- [ ] T058 [P] Add error handling wrapper to main_loop() in src/cli/app.py (catch all exceptions, display friendly messages, don't crash)
- [ ] T059 [P] Write performance test for 10k todos in tests/performance/test_performance.py (add, view, update, delete, mark - all <100ms)
- [ ] T060 [P] Write edge case tests for special characters and Unicode in tests/unit/test_todo_model.py
- [ ] T061 [P] Write edge case tests for max length boundaries (200, 2000 chars) in tests/unit/test_todo_model.py
- [ ] T062 [P] Create README.md with installation instructions, usage examples, and feature overview
- [ ] T063 [P] Add type hints to all functions in src/models/todo.py, src/services/todo_manager.py, src/cli/app.py
- [ ] T064 [P] Run black formatter on all source files
- [ ] T065 [P] Run flake8 linter and fix any PEP8 violations
- [ ] T066 [P] Run mypy type checker and fix any type errors
- [ ] T067 Run pytest with coverage report, ensure >80% coverage (pytest --cov=src --cov-report=html)
- [ ] T068 Run performance tests, verify all operations <100ms for 10k todos
- [ ] T069 Manual testing: Complete full user journey (add → view → update → mark → delete) on Windows, macOS, and Linux

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses list_todos from US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Independently testable

### Within Each User Story

**CRITICAL: TDD Order**
1. **RED**: Write all tests for the user story FIRST (they will fail)
2. **GREEN**: Implement code to make tests pass
3. **REFACTOR**: Clean up code while keeping tests green

**Component Order** (after tests):
- Models/Data before Services
- Services before CLI handlers
- CLI handlers before main loop integration

### Parallel Opportunities

- **All Setup tasks (T001-T005)**: Can run in parallel (different files/directories)
- **Foundational exceptions and dataclass (T006-T008)**: Can run in parallel
- **All tests within a user story**: Can be written in parallel (marked [P])
- **Once Foundational phase completes**: All user stories (US1-US4) can start in parallel if team capacity allows
- **Polish tasks (T055-T066)**: Most can run in parallel (marked [P])

---

## Parallel Execution Examples

### User Story 1 (Tests Phase)

Launch all tests for User Story 1 together:

```bash
# Parallel test writing (T012-T020)
Task T012: "Write unit test for Todo creation with valid title and description in tests/unit/test_todo_model.py"
Task T013: "Write unit test for Todo creation with title only in tests/unit/test_todo_model.py"
Task T014: "Write unit test for empty title validation in tests/unit/test_todo_model.py"
# ... all 9 test tasks can be written in parallel
```

### User Story 2 (Tests Phase)

```bash
# Parallel test writing (T028-T031)
Task T028: "Write unit test for marking todo as complete in tests/unit/test_todo_manager.py"
Task T029: "Write unit test for toggling todo from complete to incomplete in tests/unit/test_todo_manager.py"
Task T030: "Write unit test for marking non-existent todo in tests/unit/test_todo_manager.py"
Task T031: "Write integration test for mark-complete workflow in tests/integration/test_cli.py"
```

### Polish Phase

```bash
# Parallel polish tasks (T055-T066, excluding sequential ones)
Task T055: "Implement handle_help() in src/cli/app.py"
Task T056: "Implement handle_exit() in src/cli/app.py"
Task T058: "Add error handling wrapper to main_loop() in src/cli/app.py"
Task T059: "Write performance test for 10k todos in tests/performance/test_performance.py"
Task T060: "Write edge case tests for special characters in tests/unit/test_todo_model.py"
Task T062: "Create README.md"
Task T063: "Add type hints to all functions"
Task T064: "Run black formatter"
Task T065: "Run flake8 linter"
Task T066: "Run mypy type checker"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011) - CRITICAL BLOCKER
3. Complete Phase 3: User Story 1 (T012-T027)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**This delivers**: A working todo app where users can add and view todos (core value!)

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T012-T027) → Test independently → **MVP RELEASE** ✅
3. Add User Story 2 (T028-T036) → Test independently → **Progress Tracking RELEASE** ✅
4. Add User Story 3 (T037-T046) → Test independently → **Full Edit RELEASE** ✅
5. Add User Story 4 (T047-T054) → Test independently → **Complete CRUD RELEASE** ✅
6. Polish (T055-T069) → Final quality checks → **Phase I Complete** ✅

Each story adds value without breaking previous stories!

### Parallel Team Strategy

With multiple developers after Foundational phase completes:

```
Developer A: User Story 1 (T012-T027)
Developer B: User Story 2 (T028-T036)
Developer C: User Story 3 (T037-T046)
```

Stories complete and integrate independently.

---

## Task Summary

**Total Tasks**: 69

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 6 tasks
- Phase 3 (User Story 1 - P1): 16 tasks (9 tests + 7 implementation)
- Phase 4 (User Story 2 - P2): 9 tasks (4 tests + 5 implementation)
- Phase 5 (User Story 3 - P3): 10 tasks (6 tests + 4 implementation)
- Phase 6 (User Story 4 - P4): 8 tasks (4 tests + 4 implementation)
- Phase 7 (Polish): 15 tasks

**Parallelizable Tasks**: 45 tasks marked with [P] (65% can run in parallel within their phase)

**Test Tasks**: 23 tasks (33% of total - reflects TDD emphasis)

**Critical Path** (sequential dependencies):
1. Setup (5 tasks)
2. Foundational (6 tasks)
3. User Story 1 MVP (16 tasks)
4. **OR** proceed to US2-US4 in parallel

**Minimum MVP**: 27 tasks (Setup + Foundational + User Story 1)

---

## Notes

- **[P]** tasks = different files, no dependencies, can run in parallel
- **[Story]** label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD MANDATORY**: Tests must be written FIRST (Red phase), then implementation (Green phase), then refactor
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

## Constitution Compliance Checklist

Before considering Phase I complete, verify:

- [ ] All 15 functional requirements implemented and tested
- [ ] All 7 success criteria met (SC-001 through SC-007)
- [ ] Test coverage >80% (Constitution Principle VII)
- [ ] Python 3.13+ used exclusively
- [ ] Console-only interface (no GUI)
- [ ] In-memory storage only (no persistence)
- [ ] Performance <100ms for 10k todos (SC-003)
- [ ] Memory usage <50MB (SC-004)
- [ ] PEP8 compliant (flake8 passes)
- [ ] Type hints complete (mypy passes)
- [ ] TDD workflow followed for all features (Red-Green-Refactor)
- [ ] Cross-platform tested (Windows, macOS, Linux)

---

**Ready for Implementation**: Use `/sp.implement` to begin executing tasks with Claude Code following TDD workflow.
