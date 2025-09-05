import platform
import psutil
import socket
import os
import json
import getpass
import datetime
import uuid
import subprocess

def get_system_info():
    info = {}

    # Basic system info
    info["system"] = platform.system()
    info["node"] = platform.node()
    info["release"] = platform.release()
    info["version"] = platform.version()
    info["machine"] = platform.machine()
    # info["processor"] = platform.processor()
    info["architecture"] = platform.architecture()
    info["username"] = getpass.getuser()
    info["boot_time"] = str(datetime.datetime.fromtimestamp(psutil.boot_time()))

    # Unique ID (based on MAC)
    info["uuid"] = str(uuid.uuid1())

    return info

def get_cpu_info():
    cpu_info = {}
    cpu_info["physical_cores"] = psutil.cpu_count(logical=False)
    cpu_info["total_cores"] = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        cpu_info["max_frequency"] = cpu_freq.max
        cpu_info["min_frequency"] = cpu_freq.min
        cpu_info["current_frequency"] = cpu_freq.current
    cpu_info["cpu_usage_per_core"] = psutil.cpu_percent(percpu=True, interval=1)
    cpu_info["total_cpu_usage"] = psutil.cpu_percent()
    return cpu_info

def get_memory_info():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "percentage": memory.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_free": swap.free,
        "swap_percentage": swap.percent
    }

def get_disk_info():
    partitions_info = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        partitions_info.append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "fstype": partition.fstype,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent
        })
    return partitions_info

def get_network_info():
    net_info = {}
    hostname = socket.gethostname()
    net_info["hostname"] = hostname
    net_info["ip_address"] = socket.gethostbyname(hostname)
    net_info["interfaces"] = {}
    for interface, addrs in psutil.net_if_addrs().items():
        net_info["interfaces"][interface] = []
        for addr in addrs:
            net_info["interfaces"][interface].append({
                "family": str(addr.family),
                "address": addr.address,
                "netmask": addr.netmask,
                "broadcast": addr.broadcast
            })
    net_info["connections"] = str(psutil.net_connections())
    return net_info

def get_process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return processes

def get_environment_vars():
    return dict(os.environ)

def get_installed_packages():
    try:
        result = subprocess.check_output(["pip", "list"], text=True)
        return result
    except Exception:
        return "Unable to fetch installed packages."

def main():
    system_report = {
        "system_info": get_system_info(),
        "cpu_info": get_cpu_info(),
        "memory_info": get_memory_info(),
        "disk_info": get_disk_info(),
        "network_info": get_network_info(),
        # "processes": get_process_info(),
        "environment_variables": get_environment_vars(),
        "installed_packages": get_installed_packages(),
    }

    with open("system_report.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(system_report, indent=4))

    print("✅ System scan completed. Report saved as 'system_report.txt'")


if __name__ == "__main__":
    main()
