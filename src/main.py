"""Application entry point for the In-Memory Console Todo App"""

import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.todo_manager import TodoManager
from src.cli.app import main_loop


def main() -> None:
    """Main entry point for the Todo App"""
    # Initialize todo manager with in-memory storage
    manager = TodoManager()

    # Start the REPL interface
    main_loop(manager)


if __name__ == "__main__":
    main()
