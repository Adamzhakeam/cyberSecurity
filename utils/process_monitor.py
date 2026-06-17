import psutil
from datetime import datetime
from utils.risk_calculator import build_event_item

WATCH_PATH_KEYWORDS = ["temp", "downloads", "appdata"]


def collect_process_data():
    """Collect running processes and generate alerts for suspicious ones.

    Iterates over system processes using `psutil`, constructs a lightweight
    dict for each process and creates alert events for processes that
    match suspicious heuristics.

    Returns:
        tuple: (processes: list, alerts: list)
    """
    processes = []
    alerts = []
    seen_alerts = set()

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "exe"]):
        try:
            pid = proc.info.get("pid")
            name = proc.info.get("name") or "unknown"
            cpu = round(proc.info.get("cpu_percent", 0.0), 1)
            memory = round(proc.info.get("memory_percent", 0.0), 1)
            path = proc.info.get("exe") or "N/A"

            process_entry = {
                "pid": pid,
                "name": name,
                "cpu": cpu,
                "memory": memory,
                "path": path,
            }
            processes.append(process_entry)

            if is_suspicious_process(cpu, memory, path):
                event_key = f"{pid}-{name}-{path}"
                if event_key not in seen_alerts:
                    seen_alerts.add(event_key)
                    alerts.append(
                        build_event_item(
                            event_type="PROCESS_ALERT",
                            description=f"Suspicious process detected: {name} (CPU={cpu}%, MEM={memory}%)",
                            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        )
                    )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return processes, alerts


def is_suspicious_process(cpu, memory, path):
    """Determine whether a process is suspicious based on heuristics.

    Heuristics:
    - CPU > 80%
    - Memory > 80%
    - Executable path contains common ephemeral folders

    Args:
        cpu (float): CPU percent
        memory (float): memory percent
        path (str): executable path

    Returns:
        bool: True when suspicious
    """
    if cpu > 80 or memory > 80:
        return True
    lower_path = path.lower()
    return any(keyword in lower_path for keyword in WATCH_PATH_KEYWORDS)
