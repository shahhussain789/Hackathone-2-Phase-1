"""Simple launcher for the Todo App - run this file directly"""

import sys
import os

# Change to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add to path
sys.path.insert(0, os.getcwd())

# Import and run
from src.services.todo_manager import TodoManager
from src.cli.app import main_loop

if __name__ == "__main__":
    print("Starting Todo App...\n")
    manager = TodoManager()
    main_loop(manager)
