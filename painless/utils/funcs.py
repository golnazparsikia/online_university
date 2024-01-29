import os
from typing import Union, NoReturn
from pathlib import Path

from ..helper.exceptions import PathDoesNotExist 


def is_path_exist(path: Union[str, Path]) -> bool:
    """
    Check if a given path exists.

    Args:
        path (Union[str, Path]): The path to be checked.

    Raises:
        PathDoesNotExist: If the path does not exist or is of an invalid type.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    if isinstance(path, Path):
        is_exist = path.exists()
    elif isinstance(path, str):
        path = Path(path)
        is_exist = path.exists()
    else:
        raise PathDoesNotExist(
            f"{path} does not exist or wrong type is provided for path. "
            f"Acceptable types: str and Path, got: {type(path)}")

    return is_exist


def create_dir(file_path: str) -> NoReturn:
    """Create a new path (including nested paths)."""
    path = os.path.dirname(file_path)
    os.makedirs(path)


def create_directories(base_dir: str, directories: list[tuple[str]]):
    """
    Creates a series of directories based on the input parameters.

    Args:
    - base_dir (str): The base directory in which the subdirectories will be created.
    - directories (list of tuples): A list of tuples where each tuple represents a subdirectory to create. 
      The first element of each tuple is the name of the subdirectory, and the rest of the elements (if any) 
      represent subdirectories within the previous directory.

    Example:
    base_dir = '/path/to/base'
    directories = [('logs',), ('logs', 'auth'), ('logs', 'core')]
    create_directories(base_dir, directories)

    This will create the following directories:
    - /path/to/base/logs
    - /path/to/base/logs/auth
    - /path/to/base/logs/core
    """
    for directory in directories:
        path = os.path.join(base_dir, *directory)
        if not os.path.exists(path):
            os.makedirs(path)
