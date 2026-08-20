#!/usr/bin/env python3
"""Listen for macOS network/sleep/wake notifications while Logos runs.

This does not attach a debugger or change the network. It waits on Darwin
notify keys (the same class of event SystemConfiguration uses) and writes
a line to ~/Documents/LogosLiveWatch.log.

  python3 scripts/logos_notify_watch.py
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
import threading
import time
from pathlib import Path

LOG = Path.home() / "Documents/LogosLiveWatch.log"
MAIN_LOGOS = "/Applications/Logos.app/Contents/MacOS/Logos"

KEYS = (
    ("NETWORK", "com.apple.system.config.network_change"),
    ("SLEEP", "com.apple.system.sleep"),
    ("WAKE", "com.apple.system.wake"),
)


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def append(text: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = text.rstrip() + "\n"
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(line)
        handle.flush()
    print(line, end="", flush=True)


def run(args: list[str], timeout: float = 8.0) -> str:
    try:
        proc = subprocess.run(
            args, check=False, capture_output=True, text=True, timeout=timeout
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""
    return (proc.stdout or "") + (proc.stderr or "")


def logos_pid() -> str:
    text = run(["pgrep", "-n", "-f", MAIN_LOGOS])
    return text.strip().splitlines()[0] if text.strip() else ""


def nwi_summary() -> str:
    text = run(["scutil", "--nwi"])
    ifaces = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Network interfaces:"):
            return line.split(":", 1)[1].strip()
        if " : flags" in line and not line.startswith("REACH"):
            ifaces.append(line.split(":", 1)[0].strip())
    return ",".join(ifaces) or "-"


def logos_brief() -> str:
    pid = logos_pid()
    if not pid:
        return "logos=not-running"
    ps = run(["ps", "-o", "pcpu=,rss=,state=", "-p", pid]).split()
    cpu = ps[0] if len(ps) >= 1 else "?"
    rss = ps[1] if len(ps) >= 2 else "?"
    state = ps[2] if len(ps) >= 3 else "?"
    try:
        rss_mb = f"{int(rss) / 1024:.0f}MB"
    except ValueError:
        rss_mb = rss
    threads = run(["ps", "-M", "-p", pid])
    nthreads = max(0, threads.count("\n") - 1)
    return f"logos=pid {pid} cpu={cpu}% rss={rss_mb} state={state} threads={nthreads}"


def wait_loop(label: str, key: str) -> None:
    while True:
        run(["notifyutil", "-1", key], timeout=3600)
        extra = ""
        if label == "NETWORK":
            extra = f"  ifaces={nwi_summary()}"
        append(f"{now()}  NOTIFY  {label}  {key}{extra}  {logos_brief()}")


def heartbeat_loop() -> None:
    while True:
        time.sleep(300)
        append(f"{now()}  SCAN  {logos_brief()}  ifaces={nwi_summary()}")


def main() -> int:
    if sys.platform != "darwin":
        print("Martin's Mac only.", file=sys.stderr)
        return 2
    append(f"{now()}  NOTIFY-START keys=network,sleep,wake  scan=300s")
    append(f"{now()}  SCAN  {logos_brief()}  ifaces={nwi_summary()}")
    threads = [
        threading.Thread(target=wait_loop, args=item, daemon=True) for item in KEYS
    ]
    threads.append(threading.Thread(target=heartbeat_loop, daemon=True))
    for thread in threads:
        thread.start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        append(f"{now()}  NOTIFY-STOP")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
