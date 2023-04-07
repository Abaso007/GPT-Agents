"""
This module gets the paths for different modules in the project.
"""

import os


def __create_dir(path):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_project_root():
    """Returns project root folder."""
    # Prefers ~/.gpt-agents and makes it if it doesn't exist
    home = os.path.expanduser("~")
    project_root = os.path.join(home, ".gpt-agents")
    return __create_dir(project_root)


def get_memory_path():
    """Returns the path to the memory file."""
    memory_path = os.path.join(get_project_root(), "memory")
    # Make directory if it doesn't exist
    return __create_dir(memory_path)
