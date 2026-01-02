"""Command-line interface for the Todo App"""

from src.services.todo_manager import TodoManager
from src.models.todo import (
    TodoError,
    TodoNotFoundError,
    InvalidInputError,
    EmptyTitleError
)


def display_header() -> None:
    """Display the application header"""
    print("\n" + "=" * 40)
    print("    TODO APP - Phase I")
    print("=" * 40 + "\n")


def display_menu() -> None:
    """Display the main menu"""
    print("Main Menu:")
    print("1. Add new todo")
    print("2. View all todos")
    print("3. Update todo")
    print("4. Delete todo")
    print("5. Mark todo complete/incomplete")
    print("6. Help")
    print("7. Exit\n")


def get_choice() -> str:
    """Get user's menu choice.

    Returns:
        User's choice as a string
    """
    return input("Enter your choice (1-7): ").strip()


def handle_add_todo(manager: TodoManager) -> None:
    """Handle adding a new todo.

    Args:
        manager: TodoManager instance
    """
    print()
    title = input("Enter todo title: ").strip()
    description = input("Enter description (optional, press Enter to skip): ").strip()

    try:
        todo = manager.add_todo(title, description)
        print(f"\n✓ Todo added successfully!")
        print(f"  ID: {todo.id}")
        print(f"  Title: {todo.title}")
        if todo.description:
            print(f"  Description: {todo.description}")
        print(f"  Status: Incomplete\n")
    except (EmptyTitleError, InvalidInputError) as e:
        print(f"\n✗ Error: {e}\n")


def handle_view_todos(manager: TodoManager) -> None:
    """Handle viewing all todos.

    Args:
        manager: TodoManager instance
    """
    todos = manager.list_todos()

    if not todos:
        print("\nNo todos found. Add your first todo!\n")
        return

    stats = manager.get_stats()

    print("\n" + "=" * 40)
    print("    ALL TODOS")
    print("=" * 40 + "\n")

    for todo in todos:
        print(str(todo))
        print()

    print(f"Total: {stats['total']} todos "
          f"({stats['completed']} complete, {stats['incomplete']} incomplete)")
    print("=" * 40 + "\n")


def handle_update_todo(manager: TodoManager) -> None:
    """Handle updating a todo.

    Args:
        manager: TodoManager instance
    """
    print()
    try:
        todo_id = int(input("Enter todo ID to update: ").strip())

        # Get current todo
        todo = manager.get_todo(todo_id)
        if not todo:
            print(f"\n✗ Error: Todo #{todo_id} not found. Use 'view' to see all todos.\n")
            return

        # Show current values
        print(f"\nCurrent title: {todo.title}")
        print(f"Current description: {todo.description}")

        # Get new values
        new_title = input("\nEnter new title (or press Enter to keep current): ").strip()
        new_description = input("Enter new description (or press Enter to keep current): ").strip()

        # Update only if values provided
        title_to_update = new_title if new_title else None
        description_to_update = new_description if new_description else None

        if title_to_update is None and description_to_update is None:
            print("\n✗ No changes made.\n")
            return

        updated_todo = manager.update_todo(todo_id, title_to_update, description_to_update)
        print(f"\n✓ Todo #{todo_id} updated successfully!")
        print(f"  Title: {updated_todo.title}")
        print(f"  Description: {updated_todo.description}\n")

    except ValueError:
        print("\n✗ Error: Invalid todo ID. Please enter a number.\n")
    except (TodoNotFoundError, EmptyTitleError, InvalidInputError) as e:
        print(f"\n✗ Error: {e}\n")


def handle_delete_todo(manager: TodoManager) -> None:
    """Handle deleting a todo.

    Args:
        manager: TodoManager instance
    """
    print()
    try:
        todo_id = int(input("Enter todo ID to delete: ").strip())

        # Get todo to show what will be deleted
        todo = manager.get_todo(todo_id)
        if not todo:
            print(f"\n✗ Error: Todo #{todo_id} not found. Use 'view' to see all todos.\n")
            return

        print(f"\nYou are about to delete:")
        print(f"  [{todo.id}] {todo.title}")

        confirm = input("\nAre you sure? (y/n): ").strip().lower()

        if confirm == 'y' or confirm == 'yes':
            manager.delete_todo(todo_id)
            print(f"\n✓ Todo #{todo_id} deleted successfully!\n")
        else:
            print("\n✗ Deletion cancelled.\n")

    except ValueError:
        print("\n✗ Error: Invalid todo ID. Please enter a number.\n")
    except TodoNotFoundError as e:
        print(f"\n✗ Error: {e}\n")


def handle_mark_complete(manager: TodoManager) -> None:
    """Handle marking a todo as complete/incomplete.

    Args:
        manager: TodoManager instance
    """
    print()
    try:
        todo_id = int(input("Enter todo ID to mark: ").strip())

        # Get current todo
        todo = manager.get_todo(todo_id)
        if not todo:
            print(f"\n✗ Error: Todo #{todo_id} not found. Use 'view' to see all todos.\n")
            return

        print(f"Current status: {'Complete' if todo.completed else 'Incomplete'}")
        choice = input("Mark as (1=Complete, 2=Incomplete): ").strip()

        if choice == '1':
            completed = True
        elif choice == '2':
            completed = False
        else:
            print("\n✗ Invalid choice. Use 1 for Complete or 2 for Incomplete.\n")
            return

        updated_todo = manager.mark_complete(todo_id, completed)
        status_text = "complete" if completed else "incomplete"
        print(f"\n✓ Todo #{todo_id} marked as {status_text}!\n")

    except ValueError:
        print("\n✗ Error: Invalid input. Please enter a number.\n")
    except TodoNotFoundError as e:
        print(f"\n✗ Error: {e}\n")


def handle_help() -> None:
    """Display help information"""
    print("\n" + "=" * 40)
    print("    HELP - TODO APP COMMANDS")
    print("=" * 40 + "\n")

    print("1. Add new todo")
    print("   - Add a todo with title (required) and description (optional)")
    print("   - Titles must be non-empty and max 200 characters")
    print("   - Descriptions max 2000 characters\n")

    print("2. View all todos")
    print("   - Display all todos with their details")
    print("   - Shows ID, title, description, status, and creation time")
    print("   - Todos are ordered by creation time (oldest first)\n")

    print("3. Update todo")
    print("   - Modify title and/or description of an existing todo")
    print("   - You need the todo ID (from 'View all todos')")
    print("   - Press Enter to keep current values\n")

    print("4. Delete todo")
    print("   - Permanently remove a todo")
    print("   - You need the todo ID (from 'View all todos')")
    print("   - Confirmation required before deletion\n")

    print("5. Mark todo complete/incomplete")
    print("   - Toggle completion status of a todo")
    print("   - You need the todo ID (from 'View all todos')\n")

    print("6. Help")
    print("   - Display this help information\n")

    print("7. Exit")
    print("   - Exit the application")
    print("   - WARNING: All data will be lost (in-memory storage)\n")

    print("=" * 40 + "\n")


def handle_exit(manager: TodoManager) -> bool:
    """Handle exiting the application.

    Args:
        manager: TodoManager instance

    Returns:
        True if user confirms exit, False otherwise
    """
    print()
    confirm = input("Are you sure you want to exit? All data will be lost. (y/n): ").strip().lower()

    if confirm == 'y' or confirm == 'yes':
        print("\n" + "=" * 40)
        print("Thank you for using TODO APP!")
        print("All data has been cleared.")
        print("=" * 40 + "\n")
        return True

    print("\n✗ Exit cancelled.\n")
    return False


def main_loop(manager: TodoManager) -> None:
    """Main application loop.

    Args:
        manager: TodoManager instance
    """
    display_header()

    while True:
        try:
            display_menu()
            choice = get_choice()

            if choice == '1':
                handle_add_todo(manager)
            elif choice == '2':
                handle_view_todos(manager)
            elif choice == '3':
                handle_update_todo(manager)
            elif choice == '4':
                handle_delete_todo(manager)
            elif choice == '5':
                handle_mark_complete(manager)
            elif choice == '6':
                handle_help()
            elif choice == '7':
                if handle_exit(manager):
                    break
            else:
                print("\n✗ Invalid choice. Please enter a number between 1 and 7.\n")

        except KeyboardInterrupt:
            print("\n\n✗ Operation interrupted. Returning to main menu...\n")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            print("Please try again or contact support if the problem persists.\n")
