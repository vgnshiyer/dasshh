import socket
import subprocess
import platform
import requests
from typing import Dict, Optional

from dasshh.core.tools.decorator import tool


@tool
def ping(host: str, count: int = 4) -> Dict:
    """Ping a host and return the results"""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = f"ping {param} {count} {host}"

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=10
        )

        return {
            "host": host,
            "command": command,
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
        }
    except Exception as e:
        return {"host": host, "success": False, "error": str(e)}


@tool
def get_ip_address(hostname: Optional[str] = None) -> Dict:
    """Get IP address information for a hostname or the local machine"""
    if hostname:
        try:
            ip = socket.gethostbyname(hostname)
            return {"hostname": hostname, "ip": ip}
        except socket.gaierror as e:
            return {
                "hostname": hostname,
                "error": f"Could not resolve hostname: {str(e)}",
            }
    else:
        # Get local hostname and IP
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
            return {"hostname": hostname, "ip": ip}
        except socket.gaierror as e:
            return {
                "hostname": hostname,
                "error": f"Could not resolve local hostname: {str(e)}",
            }


@tool
def check_port(port: int) -> Dict:
    """Check if a specific port is in use on a localhost"""
    host = "localhost"
    timeout = 3
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        return {"host": host, "port": port, "in_use": result == 0}
    except Exception as e:
        return {"host": host, "port": port, "error": str(e)}


@tool
def public_ip() -> Dict:
    """Get the public IP address of the current machine"""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        return response.json()
    except Exception as e:
        return {"error": f"Could not get public IP: {str(e)}"}


@tool
def traceroute(host: str) -> Dict:
    """Perform a traceroute to a host"""
    command = (
        f"traceroute {host}"
        if platform.system().lower() != "windows"
        else f"tracert {host}"
    )

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )

        return {
            "host": host,
            "command": command,
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
        }
    except Exception as e:
        return {"host": host, "success": False, "error": str(e)}
