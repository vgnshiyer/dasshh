import platform
import psutil
from typing import Dict

from dasshh.core.tools.decorator import tool


@tool
def system_info() -> Dict:
    """
    Get detailed information about the operating system.
    """
    info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
    return info


@tool
def cpu_info() -> Dict:
    """
    Get CPU information and current usage.
    """
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)

    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": cpu_count,
        "usage_per_core": cpu_percent,
        "total_usage": sum(cpu_percent) / len(cpu_percent),
        "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
    }


@tool
def memory_info() -> Dict:
    """
    Get memory (RAM) information and usage.
    """
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_percent": swap.percent,
    }


@tool
def disk_info(path: str = "/") -> Dict:
    """
    Get disk space information for the specified path.
    """
    disk = psutil.disk_usage(path)

    return {
        "path": path,
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent,
    }


@tool
def network_info() -> Dict:
    """
    Get network interface information.
    """
    interfaces = psutil.net_if_addrs()
    io_counters = psutil.net_io_counters(pernic=True)

    result = {}
    for interface, addresses in interfaces.items():
        result[interface] = {
            "addresses": [addr._asdict() for addr in addresses],
            "stats": io_counters.get(interface)._asdict()
            if interface in io_counters
            else None,
        }

    return result
