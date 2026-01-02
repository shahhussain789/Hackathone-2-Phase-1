# Data Model: In-Memory Console Todo App (Phase I)

**Feature**: 001-console-todo-app
**Date**: 2026-01-02
**Phase**: 1 (Design)

## Overview

This document defines the data model for Phase I of the console todo application. The model is intentionally simple for in-memory storage but designed with extensibility in mind for Phase II database migration (SQLModel/Neon DB).

## Entity: Todo

### Description

Represents a single todo item with title, description, completion status, and metadata for ordering and identification.

### Attributes

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | int | Yes | Auto-generated | Unique, sequential, > 0 | Unique identifier for the todo |
| `title` | str | Yes | - | Non-empty, max 200 chars | Short description of the task |
| `description` | str | No | "" (empty string) | Max 2000 chars | Detailed description of the task |
| `completed` | bool | Yes | False | True or False | Completion status of the todo |
| `created_at` | datetime | Yes | Auto-generated | ISO 8601 format | Timestamp when todo was created |

### Validation Rules

From functional requirements (FR-008, FR-009, FR-014):

1. **Title validation**:
   - MUST NOT be empty or whitespace-only
   - MUST be stripped of leading/trailing whitespace before storage
   - Maximum length: 200 characters
   - Special characters allowed (Unicode support)

2. **Description validation**:
   - Optional, can be empty
   - MUST be stripped of leading/trailing whitespace before storage
   - Maximum length: 2000 characters
   - Special characters allowed (Unicode support)

3. **ID validation**:
   - Auto-generated, sequential starting from 1
   - MUST be unique across all todos in the session
   - Cannot be modified after creation

4. **Completion status validation**:
   - Boolean only (True/False)
   - Defaults to False (incomplete) on creation
   - Can be toggled via mark complete/incomplete operations

5. **Created timestamp validation**:
   - Auto-generated on todo creation
   - Immutable after creation
   - Used for ordering todos by creation time (FR-012)

### State Transitions

```
[Creation] → Incomplete (completed=False)
    ↓
Incomplete ←→ Complete (via mark complete/incomplete)
    ↓
[Deletion] → Removed from storage
```

**Valid transitions**:
- New todo → Incomplete (default state)
- Incomplete → Complete (user marks done)
- Complete → Incomplete (user toggles back)
- Any state → Deleted (user removes todo)

**Invalid transitions**:
- None (all state changes are valid for todos)

## Data Storage Structure

### In-Memory Storage (Phase I)

**Primary structure**: Dictionary mapping todo ID to Todo object

```python
# Storage representation (conceptual, not implementation)
todos: dict[int, Todo] = {
    1: Todo(id=1, title="Write tests", description="Add pytest tests",
            completed=False, created_at=datetime(...)),
    2: Todo(id=2, title="Deploy app", description="",
            completed=True, created_at=datetime(...)),
    # ... more todos
}

# Metadata
next_id: int = 3  # Next available ID
```

**Rationale**:
- O(1) lookup by ID (performance requirement: <100ms for 10k todos)
- Maintains insertion order (Python 3.7+ dict feature)
- Simple to implement and test
- Low memory overhead (<50MB budget)

### ID Generation Strategy

**Approach**: Sequential integer counter

```python
# Conceptual ID generation logic
current_id = next_id
next_id += 1
return current_id
```

**Properties**:
- Predictable IDs (user-friendly)
- No collisions (sequential)
- Simple implementation
- Supports up to 2^31 - 1 todos (practically unlimited for Phase I)

**Alternatives considered**:
- UUID: Over-engineering, wastes memory, not user-friendly for console
- Random numbers: Collision risk, no ordering
- Hash-based: Unnecessary complexity

### Ordering Strategy

**Primary sort**: Creation timestamp (oldest first)

**Implementation**: Python dict maintains insertion order, iterate values() to get creation order

**Rationale**:
- FR-012 requires "maintain todo order by creation time"
- Dict insertion order is deterministic in Python 3.7+
- No additional data structure needed (memory efficient)

## Python Implementation Details

### Dataclass Definition

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Todo:
    """Represents a todo item with title, description, and completion status."""

    id: int
    title: str
    completed: bool = False
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate todo attributes after initialization."""
        # Validation logic here (see validation rules above)
```

**Design choices**:
- `@dataclass`: Reduces boilerplate, generates __init__, __repr__, __eq__
- Type hints: Full typing for mypy static analysis
- `field(default_factory=datetime.now)`: Proper mutable default handling
- `__post_init__`: Custom validation after dataclass initialization

### Type Hints

```python
from typing import Optional

# Service layer types
TodoID = int
TodoDict = dict[TodoID, Todo]

# Function signatures
def add_todo(title: str, description: str = "") -> Todo: ...
def get_todo(todo_id: TodoID) -> Optional[Todo]: ...
def update_todo(todo_id: TodoID, title: Optional[str],
                description: Optional[str]) -> Todo: ...
def delete_todo(todo_id: TodoID) -> None: ...
def mark_complete(todo_id: TodoID, completed: bool) -> Todo: ...
def list_todos() -> list[Todo]: ...
```

## Relationships

### Phase I (No relationships)

Since Phase I is a single-user, in-memory console app, there are no entity relationships:
- No users (single-user session)
- No categories/tags (out of scope per spec)
- No subtasks (out of scope per spec)

### Phase II Migration Path

**Planned relationships for future phases**:

```
User (Phase II)
  ↓ has many
Todo
  ↓ optionally has many
Category/Tag (Phase II or III)
```

**Database schema preview** (Phase II with SQLModel):

```python
# Conceptual Phase II model (NOT implemented in Phase I)
class Todo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(foreign_key="user.id")  # New in Phase II
```

## Memory Considerations

### Memory Budget

**Target**: <50MB total application memory (Phase I constitution requirement)

**Estimated memory per todo**:
- id (int): 28 bytes (Python int object)
- title (str, avg 50 chars): ~100 bytes
- description (str, avg 100 chars): ~150 bytes
- completed (bool): 28 bytes
- created_at (datetime): 48 bytes
- Python object overhead: ~50 bytes
- **Total per todo**: ~400 bytes

**Capacity calculation**:
- 50MB budget = 50,000,000 bytes
- Reserve 10MB for Python runtime: 40,000,000 bytes available
- 40MB / 400 bytes per todo ≈ **100,000 todos**

**Conclusion**: Memory budget comfortably supports 10,000 todo requirement (SC-003) with 10x headroom.

### Memory Optimization Notes

**Not needed for Phase I** (budget comfortable), but documented for future:
- Use `__slots__` in Todo class: Saves ~40% memory per instance
- Intern strings for repeated values: Minimal benefit for unique titles
- Use generators for large list operations: Only if iterating 50k+ todos

## Validation Error Messages

Per FR-009 ("clear error messages"), define specific messages:

| Error Condition | Exception Type | User Message |
|----------------|----------------|--------------|
| Empty title | EmptyTitleError | "Title cannot be empty. Please provide a title for your todo." |
| Title too long | InvalidInputError | "Title too long (max 200 characters). Current length: {len}" |
| Description too long | InvalidInputError | "Description too long (max 2000 characters). Current length: {len}" |
| Todo not found | TodoNotFoundError | "Todo #{id} not found. Use 'view' to see all todos." |
| Invalid ID format | InvalidInputError | "Invalid todo ID: '{input}'. Please enter a number." |

## Testing Strategy

### Unit Tests for Todo Model

1. **Creation tests**:
   - Create with title only (description defaults to "")
   - Create with title and description
   - Verify ID auto-assigned
   - Verify created_at auto-generated
   - Verify completed defaults to False

2. **Validation tests**:
   - Empty title raises EmptyTitleError
   - Whitespace-only title raises EmptyTitleError
   - Title >200 chars raises InvalidInputError
   - Description >2000 chars raises InvalidInputError
   - Special characters in title/description accepted (Unicode)

3. **State transition tests**:
   - Toggle completed from False → True
   - Toggle completed from True → False

### Integration Tests for Storage

1. **CRUD operations**:
   - Add 1000 todos, verify all stored with unique IDs
   - Retrieve todos by ID, verify correct data
   - Update todo title/description, verify changes persist
   - Delete todo, verify removed from storage
   - Mark complete, verify status updates

2. **Ordering tests**:
   - Add todos in random order
   - Retrieve list, verify sorted by created_at (oldest first)

3. **Performance tests** (SC-003):
   - Create 10,000 todos
   - Measure time for each operation: add, get, update, delete, list
   - Assert all operations <100ms

4. **Memory tests** (SC-004):
   - Create 10,000 todos
   - Measure memory usage with memory_profiler
   - Assert total usage <50MB

## Phase II Migration Notes

### Direct SQLModel Mapping

Phase I dataclass → Phase II SQLModel with minimal changes:

```python
# Phase I (dataclass)
@dataclass
class Todo:
    id: int
    title: str
    completed: bool = False
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)

# Phase II (SQLModel) - Migration path
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    title: str = Field(max_length=200)
    completed: bool = Field(default=False)
    description: str = Field(default="", max_length=2000)
    created_at: datetime = Field(default_factory=datetime.now)
```

**Changes needed**:
- Add `SQLModel` inheritance
- Add `Field()` constraints
- Make `id` Optional for auto-generation
- Add database session management (not in model)

### Data Migration Strategy (Phase I → Phase II)

**Not applicable**: Phase I has no persistence, so no data migration needed. Each phase starts fresh until Phase II introduces persistence.

## Conclusion

Data model satisfies all requirements:
- ✅ Supports all 15 functional requirements
- ✅ Meets performance budget (<100ms, <50MB)
- ✅ Validates input per FR-008, FR-009, FR-014
- ✅ Designed for Phase II extensibility (Modularity, Extensibility principles)
- ✅ Simple enough for in-memory storage (no over-engineering)

**Ready for**: Contract definition and quickstart guide.
