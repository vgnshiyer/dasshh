import os
import shutil
from datetime import datetime
from typing import List, Dict

from dasshh.core.tools.decorator import tool


@tool
def current_directory() -> str:
    """Get the current working directory.

    Returns:
        str: The current working directory.
    """
    return os.getcwd()


@tool
def list_files(directory: str) -> List[Dict]:
    """List all files and directories in the specified directory.

    Args:
        directory (str): The path to the directory to list.
    """
    if not os.path.exists(directory):
        return [{"error": f"Directory '{directory}' does not exist"}]

    files = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        stat = os.stat(path)
        files.append(
            {
                "name": item,
                "path": path,
                "size": stat.st_size,
                "is_dir": os.path.isdir(path),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }
        )
    return files


@tool
def file_info(path: str) -> Dict:
    """
    Get detailed information about a file or directory.

    Args:
        path (str): The path to the file or directory to get information about.
    """
    if not os.path.exists(path):
        return {"error": f"Path '{path}' does not exist"}

    stat = os.stat(path)
    return {
        "name": os.path.basename(path),
        "path": os.path.abspath(path),
        "size": stat.st_size,
        "is_dir": os.path.isdir(path),
        "is_file": os.path.isfile(path),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
        "permissions": oct(stat.st_mode)[-3:],
    }


@tool
def read_file(path: str) -> Dict:
    """Read the contents of a file.

    Args:
        path (str): The path to the file to read.
    """
    if not os.path.exists(path):
        return {"error": f"Path '{path}' does not exist"}

    with open(path, "r") as file:
        return file.read()


@tool
def create_directory(path: str) -> Dict:
    """
    Create a new directory at the specified path.

    Args:
        path (str): The path to the new directory.
    """
    if os.path.exists(path):
        return {"error": f"Path '{path}' already exists"}

    try:
        os.makedirs(path, exist_ok=True)
        return {"success": True, "path": path}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def delete_file(path: str, recursive: bool = False) -> Dict:
    """
    Delete a file or directory.

    Args:
        path (str): The path to the file or directory to delete.
        recursive (bool): Whether to delete non-empty directories recursively.
    """
    if not os.path.exists(path):
        return {"error": f"Path '{path}' does not exist"}

    try:
        if os.path.isdir(path):
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
        else:
            os.remove(path)
        return {"success": True, "path": path}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def copy_file(source: str, destination: str) -> Dict:
    """
    Copy a file or directory from source to destination.

    Args:
        source (str): The path to the source file or directory.
        destination (str): The path to the destination file or directory.
    """
    if not os.path.exists(source):
        return {"error": f"Source '{source}' does not exist"}

    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        return {"success": True, "source": source, "destination": destination}
    except Exception as e:
        return {"success": False, "error": str(e)}


@tool
def move_file(source: str, destination: str) -> Dict:
    """
    Move a file or directory from source to destination.

    Args:
        source (str): The path to the source file or directory.
        destination (str): The path to the destination file or directory.
    """
    if not os.path.exists(source):
        return {"error": f"Source '{source}' does not exist"}

    try:
        shutil.move(source, destination)
        return {"success": True, "source": source, "destination": destination}
    except Exception as e:
        return {"success": False, "error": str(e)}
