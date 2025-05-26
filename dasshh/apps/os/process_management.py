import psutil
import subprocess
from typing import Dict, List, Optional

from dasshh.core.tools.decorator import tool


@tool
def process_list() -> List[Dict]:
    """
    List all running processes with basic information.
    """
    processes = []
    for proc in psutil.process_iter(
        ["pid", "name", "username", "memory_percent", "cpu_percent"]
    ):
        processes.append(proc.info)

    return processes


@tool
def find_process(name: str) -> List[Dict]:
    """
    Find all processes matching a name pattern.

    Args:
        name (str): The name pattern to search for.
    """
    matching_processes = []
    for proc in psutil.process_iter(["pid", "name", "username", "cmdline"]):
        if name.lower() in proc.info["name"].lower():
            matching_processes.append(proc.info)
    return matching_processes


@tool
def get_process_info(pid: int) -> Dict:
    """
    Get detailed information about a specific process by its PID.

    Args:
        pid (int): The PID of the process to get information about.
    """
    try:
        proc = psutil.Process(pid)
        return {
            "pid": proc.pid,
            "name": proc.name(),
            "status": proc.status(),
            "created": proc.create_time(),
            "username": proc.username(),
            "cmdline": proc.cmdline(),
            "cwd": proc.cwd(),
            "memory_info": proc.memory_info()._asdict(),
            "cpu_percent": proc.cpu_percent(interval=0.1),
            "num_threads": proc.num_threads(),
            "open_files": [f._asdict() for f in proc.open_files()],
            "connections": [c._asdict() for c in proc.connections()],
        }
    except psutil.NoSuchProcess:
        return {"error": f"No process with PID {pid} found"}
    except psutil.AccessDenied:
        return {"error": f"Access denied to process with PID {pid}"}


@tool
def kill_process(pid: int) -> Dict:
    """
    Terminate a process by its PID.

    Args:
        pid (int): The PID of the process to terminate.
    """
    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()
        proc.terminate()

        # Wait for process to terminate (max 3 seconds)
        gone, still_alive = psutil.wait_procs([proc], timeout=3)

        if still_alive:
            # If still alive, kill it more forcefully
            proc.kill()
            return {
                "success": True,
                "pid": pid,
                "name": proc_name,
                "force_killed": True,
            }
        else:
            return {
                "success": True,
                "pid": pid,
                "name": proc_name,
                "force_killed": False,
            }
    except psutil.NoSuchProcess:
        return {"error": f"No process with PID {pid} found"}
    except psutil.AccessDenied:
        return {"error": f"Access denied when trying to kill process with PID {pid}"}


@tool
def run_command(command: str, timeout: Optional[int] = None) -> Dict:
    """
    Run a shell command and return its output.

    Args:
        command (str): The command to run.
        timeout (int, optional): The timeout for the command.
    """
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout
        )

        return {
            "command": command,
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "success": False,
            "error": f"Command timed out after {timeout} seconds",
        }
    except Exception as e:
        return {"command": command, "success": False, "error": str(e)}
