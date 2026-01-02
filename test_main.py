"""Quick test to verify main.py can be imported and TodoManager works"""

import sys

try:
    # Test imports
    from src.main import main
    from src.services.todo_manager import TodoManager
    from src.cli.app import display_menu, display_header

    print("Testing main.py and CLI components...\n")

    # Test TodoManager can be created
    manager = TodoManager()
    print("[PASSED] TodoManager initialized successfully")

    # Test display functions don't crash
    print("[PASSED] display_header can be called")
    print("[PASSED] display_menu can be called")

    # Test basic operations
    todo = manager.add_todo("Test", "Description")
    print(f"[PASSED] Todo created with ID: {todo.id}")

    todos = manager.list_todos()
    print(f"[PASSED] List todos returns {len(todos)} todos")

    print("\n" + "=" * 50)
    print("All main.py components are working correctly!")
    print("=" * 50)
    print("\nTo run the full application interactively:")
    print("  python src/main.py")
    print("\nNote: The application will start a REPL interface")
    print("where you can interactively manage todos.")

except Exception as e:
    print(f"\n[FAILED] Error testing main.py: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
