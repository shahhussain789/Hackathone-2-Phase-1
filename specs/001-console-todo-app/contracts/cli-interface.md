# CLI Interface Contract: In-Memory Console Todo App (Phase I)

**Feature**: 001-console-todo-app
**Date**: 2026-01-02
**Interface Type**: Console REPL (Read-Eval-Print Loop)

## Overview

This contract defines the console interface for the todo application. It specifies the command structure, input/output formats, error handling, and user interaction patterns.

## Interface Pattern: Menu-Driven REPL

### Application Flow

```
[Start] → Display Welcome
    ↓
Display Main Menu
    ↓
Read User Choice
    ↓
Execute Command
    ↓
Display Result
    ↓
Loop to Main Menu (unless Exit chosen)
```

## Main Menu

### Display Format

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

Enter your choice (1-7): _
```

### Input Specification

- **Type**: Integer (1-7)
- **Validation**: Must be valid menu option
- **Error handling**: Invalid input shows error and re-displays menu

### Error Messages

```
✗ Invalid choice. Please enter a number between 1 and 7.
```

## Command 1: Add New Todo

### Input Flow

```
Enter todo title: _
[User enters title]

Enter description (optional, press Enter to skip): _
[User enters description or presses Enter]
```

### Input Specifications

| Field | Type | Required | Max Length | Validation |
|-------|------|----------|------------|------------|
| Title | str | Yes | 200 chars | Non-empty, stripped |
| Description | str | No | 2000 chars | Stripped, defaults to "" |

### Success Output

```
✓ Todo added successfully!
  ID: 5
  Title: Write unit tests
  Description: Add pytest tests for todo manager
  Status: Incomplete
```

### Error Outputs

**Empty title**:
```
✗ Error: Title cannot be empty. Please provide a title for your todo.
```

**Title too long**:
```
✗ Error: Title too long (max 200 characters). Current length: 247
```

**Description too long**:
```
✗ Error: Description too long (max 2000 characters). Current length: 2156
```

## Command 2: View All Todos

### Input Flow

```
[Automatically displays all todos, no user input required]
```

### Success Output (With Todos)

```
========================================
    ALL TODOS
========================================

[1] Write unit tests
    Description: Add pytest tests for todo manager
    Status: ☐ Incomplete
    Created: 2026-01-02 14:23:15

[2] Deploy to production
    Description:
    Status: ☑ Complete
    Created: 2026-01-02 14:25:42

[3] Review pull requests
    Description: Review open PRs in the team repo
    Status: ☐ Incomplete
    Created: 2026-01-02 14:30:01

Total: 3 todos (1 complete, 2 incomplete)
========================================
```

### Success Output (No Todos)

```
========================================
    ALL TODOS
========================================

No todos found. Use option 1 to add a new todo.

========================================
```

### Display Format Specification

- **Status symbols**: ☑ Complete, ☐ Incomplete
- **Timestamp format**: YYYY-MM-DD HH:MM:SS
- **Empty description**: Show as blank (no placeholder text)
- **Ordering**: Creation time (oldest first) per FR-012

## Command 3: Update Todo

### Input Flow

```
Enter todo ID to update: _
[User enters ID]

Current title: Write unit tests
Enter new title (or press Enter to keep current): _
[User enters new title or presses Enter]

Current description: Add pytest tests for todo manager
Enter new description (or press Enter to keep current): _
[User enters new description or presses Enter]
```

### Input Specifications

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Todo ID | int | Yes | Must exist |
| New Title | str | No | If provided: non-empty, max 200 chars |
| New Description | str | No | If provided: max 2000 chars |

### Success Output

```
✓ Todo updated successfully!
  ID: 2
  Title: Write integration tests
  Description: Add pytest integration tests for the application
  Status: ☐ Incomplete
```

### Error Outputs

**Todo not found**:
```
✗ Error: Todo #999 not found. Use option 2 to see all todos.
```

**Invalid ID format**:
```
✗ Error: Invalid todo ID: 'abc'. Please enter a number.
```

**Empty title**:
```
✗ Error: Title cannot be empty. Please provide a title for your todo.
```

**No changes made**:
```
ℹ No changes made to todo #2.
```

## Command 4: Delete Todo

### Input Flow

```
Enter todo ID to delete: _
[User enters ID]

Are you sure you want to delete this todo? (y/n): _
[User confirms with y/n]
```

### Input Specifications

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Todo ID | int | Yes | Must exist |
| Confirmation | str | Yes | Must be 'y' or 'n' (case-insensitive) |

### Success Output

```
✓ Todo #5 deleted successfully.
```

### Cancelled Output

```
ℹ Deletion cancelled.
```

### Error Outputs

**Todo not found**:
```
✗ Error: Todo #777 not found. Use option 2 to see all todos.
```

**Invalid ID format**:
```
✗ Error: Invalid todo ID: 'xyz'. Please enter a number.
```

## Command 5: Mark Todo Complete/Incomplete

### Input Flow

```
Enter todo ID to mark: _
[User enters ID]

Current status: Incomplete
Mark as (1=Complete, 2=Incomplete): _
[User chooses 1 or 2]
```

### Input Specifications

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Todo ID | int | Yes | Must exist |
| Status Choice | int | Yes | Must be 1 or 2 |

### Success Output

**Marked complete**:
```
✓ Todo #3 marked as complete!
```

**Marked incomplete**:
```
✓ Todo #3 marked as incomplete!
```

### Error Outputs

**Todo not found**:
```
✗ Error: Todo #888 not found. Use option 2 to see all todos.
```

**Invalid status choice**:
```
✗ Error: Invalid choice. Enter 1 for Complete or 2 for Incomplete.
```

## Command 6: Help

### Output

```
========================================
    HELP - TODO APP COMMANDS
========================================

1. Add new todo
   - Create a new todo item with title and optional description
   - Title is required (max 200 characters)
   - Description is optional (max 2000 characters)

2. View all todos
   - Display all todos with their ID, title, description, status, and creation time
   - Todos are shown in creation order (oldest first)

3. Update todo
   - Modify the title and/or description of an existing todo
   - Enter the todo ID and provide new values
   - Press Enter to keep current values unchanged

4. Delete todo
   - Remove a todo from your list
   - Requires confirmation before deletion
   - This action cannot be undone

5. Mark todo complete/incomplete
   - Toggle the completion status of a todo
   - Mark tasks as complete when done
   - Mark back to incomplete if needed

6. Help
   - Display this help message

7. Exit
   - Close the application
   - All data will be lost (in-memory storage)

========================================
Performance: Supports up to 10,000 todos
All operations complete in <100ms
========================================
```

## Command 7: Exit

### Input Flow

```
Are you sure you want to exit? All data will be lost. (y/n): _
[User confirms with y/n]
```

### Success Output

```
========================================
Thank you for using TODO APP!
All data has been cleared.
========================================
```

### Cancelled Output

```
ℹ Exit cancelled. Returning to main menu.
```

## Error Handling Standards

### General Error Format

```
✗ Error: [Specific error message]
```

### Exception Mapping

| Exception Type | User Message Pattern |
|---------------|---------------------|
| TodoNotFoundError | "Todo #{id} not found. Use option 2 to see all todos." |
| EmptyTitleError | "Title cannot be empty. Please provide a title for your todo." |
| InvalidInputError | "[Specific validation error with guidance]" |
| ValueError (ID parsing) | "Invalid todo ID: '{input}'. Please enter a number." |
| Unexpected errors | "An unexpected error occurred. Please try again." |

### Error Recovery

All errors return user to main menu after displaying error message. Application should never crash from user input.

## Input/Output Specifications

### Input Reading

- **Method**: `input()` function (Python standard library)
- **Encoding**: UTF-8 (Unicode support for special characters)
- **Whitespace handling**: Strip leading/trailing whitespace from all inputs
- **Empty input**: Treat as empty string, validate accordingly

### Output Display

- **Method**: `print()` function (Python standard library)
- **Encoding**: UTF-8 (Unicode support)
- **Line separators**: Platform-native (os.linesep)
- **Color**: None (plain text for cross-platform compatibility)

### Special Characters

**Supported**:
- Unicode characters (emoji, accented letters, etc.)
- Newlines in descriptions (displayed as newlines)
- Special punctuation

**Not supported** (edge cases, but handled gracefully):
- Control characters (stripped during validation)
- Null bytes (rejected during validation)

## Performance Requirements

From SC-003 and SC-004:

- **Response time**: All commands complete in <100ms for lists up to 10,000 todos
- **Menu display**: Instant (<10ms)
- **Todo listing**: <100ms for 10,000 todos
- **Memory usage**: <50MB total application memory

## Usability Requirements

From SC-002 and SC-007:

- **Discoverability**: All operations accessible from main menu
- **Help availability**: Help command (option 6) explains all operations
- **Error guidance**: Error messages include next steps (e.g., "Use option 2 to see all todos")
- **Confirmation**: Destructive operations (delete, exit) require confirmation
- **Success feedback**: All successful operations show confirmation message

## Testing Contract

### Manual Testing Scenarios

1. **Happy path**: Add → View → Update → Mark Complete → Delete → Exit
2. **Error handling**: Invalid IDs, empty titles, out-of-range menu choices
3. **Edge cases**: Very long titles/descriptions, special characters, 10k todos
4. **Usability**: First-time user relying only on help command (SC-007)

### Automated Testing Approach

**Input simulation**: Use `unittest.mock.patch('builtins.input')` to simulate user input

**Output capture**: Use `unittest.mock.patch('builtins.print')` or `io.StringIO` to capture output

**Test structure**:
```python
# Conceptual test structure (not implementation)
def test_add_todo_happy_path():
    # Mock input: menu choice 1, title, description
    # Assert: Success message printed
    # Assert: Todo added to storage
```

## Phase II Migration Path

### API Endpoint Mapping

This CLI interface maps directly to REST API endpoints in Phase II:

| CLI Command | Phase II Endpoint | HTTP Method |
|-------------|------------------|-------------|
| Add todo | POST /api/todos | POST |
| View all | GET /api/todos | GET |
| Update | PUT /api/todos/{id} | PUT |
| Delete | DELETE /api/todos/{id} | DELETE |
| Mark complete | PATCH /api/todos/{id}/complete | PATCH |

### Request/Response Format (Phase II Preview)

```json
// POST /api/todos (Add todo)
Request: {
  "title": "Write unit tests",
  "description": "Add pytest tests for todo manager"
}

Response: {
  "id": 5,
  "title": "Write unit tests",
  "description": "Add pytest tests for todo manager",
  "completed": false,
  "created_at": "2026-01-02T14:23:15Z"
}
```

The CLI command handlers can be refactored into API controllers with minimal business logic changes.

## Conclusion

This contract satisfies:
- ✅ FR-010: Console-based command interface
- ✅ FR-011: Clear, readable format for all operations
- ✅ FR-015: Help command with usage information
- ✅ SC-002: Operations performable without external docs (help command sufficient)
- ✅ SC-007: 5 operations correct on first attempt after help
- ✅ Usability principle: Intuitive interface following console conventions

**Ready for**: Quickstart guide creation.
