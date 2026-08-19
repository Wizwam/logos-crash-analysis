#!/usr/bin/env python3
"""Logos dock/Wi-Fi diagnostic helper for macOS.

This does NOT force a faster Ethernet switch and does NOT send keep-alives.
Those would create more network transitions, which is what crashes Logos.

What it does:
  status            Print Wi-Fi vs Ethernet right now
  watch             Append a line whenever the default route changes
                    (and a heartbeat every --interval seconds)
  disable-ethernet  Turn OFF dock/USB/Thunderbolt Ethernet services so
                    the Mac stays on Wi-Fi even when the dock is plugged in
  enable-ethernet   Turn those Ethernet services back ON
  install-watch     Install a per-user LaunchAgent (macOS replacement for cron)
  uninstall-watch   Remove that LaunchAgent

Log file default: ~/Documents/LogosNetworkWatch.log
"""

from __future__ import annotations

import argparse
import datetime as dt
import plistlib
import shutil
import subprocess
import sys
import time
from pathlib import Path

LAUNCH_LABEL = "ca.logosnetworkwatch.plist"
LAUNCH_AGENT = Path.home() / "Library/LaunchAgents" / LAUNCH_LABEL
DEFAULT_LOG = Path.home() / "Documents/LogosNetworkWatch.log"

ETHERNET_HINTS = (
    "ethernet",
    "thunderbolt",
    "usb 10",
    "usb 10/100",
    "lan",
    "dock",
    "realtek",
    "ax881",
)


def run(args: list[str]) -> str:
    try:
        proc = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""
    return (proc.stdout or "") + (proc.stderr or "")


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hardware_ports() -> list[dict[str, str]]:
    text = run(["networksetup", "-listallhardwareports"])
    ports: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Hardware Port:"):
            if current:
                ports.append(current)
            current = {"port": line.split(":", 1)[1].strip()}
        elif line.startswith("Device:") and current:
            current["device"] = line.split(":", 1)[1].strip()
        elif line.startswith("Ethernet Address:") and current:
            current["mac"] = line.split(":", 1)[1].strip()
    if current:
        ports.append(current)
    return ports


def service_order() -> list[str]:
    text = run(["networksetup", "-listnetworkserviceorder"])
    names: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        # "(1) Wi-Fi"
        if line.startswith("(") and ")" in line:
            names.append(line.split(")", 1)[1].strip())
    return names


def service_enabled(name: str) -> bool:
    out = run(["networksetup", "-getnetworkserviceenabled", name]).strip().lower()
    return out.startswith("enabled")


def default_route() -> dict[str, str]:
    text = run(["route", "-n", "get", "default"])
    info = {"interface": "", "gateway": ""}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("interface:"):
            info["interface"] = line.split(":", 1)[1].strip()
        elif line.startswith("gateway:"):
            info["gateway"] = line.split(":", 1)[1].strip()
    return info


def ifconfig_inet(device: str) -> str:
    if not device:
        return ""
    text = run(["ifconfig", device])
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("inet "):
            parts = line.split()
            if len(parts) >= 2:
                return parts[1]
    return ""


def classify_port(port_name: str) -> str:
    lower = port_name.lower()
    if "wi-fi" in lower or "wifi" in lower or "airport" in lower:
        return "wifi"
    if any(hint in lower for hint in ETHERNET_HINTS):
        return "ethernet"
    return "other"


def snapshot() -> dict:
    ports = hardware_ports()
    route = default_route()
    services = []
    for name in service_order():
        kind = classify_port(name)
        device = ""
        for port in ports:
            if port.get("port") == name:
                device = port.get("device", "")
                break
        services.append(
            {
                "name": name,
                "kind": kind,
                "enabled": service_enabled(name),
                "device": device,
                "ipv4": ifconfig_inet(device) if device else "",
            }
        )
    default_kind = "unknown"
    for port in ports:
        if port.get("device") == route["interface"]:
            default_kind = classify_port(port.get("port", ""))
            break
    return {
        "time": now(),
        "default_interface": route["interface"],
        "default_gateway": route["gateway"],
        "default_kind": default_kind,
        "default_ipv4": ifconfig_inet(route["interface"]),
        "services": services,
    }


def format_snapshot(snap: dict) -> str:
    lines = [
        f"{snap['time']}  default={snap['default_kind'] or 'unknown'}"
        f"  iface={snap['default_interface'] or '-'}"
        f"  ip={snap['default_ipv4'] or '-'}"
        f"  gw={snap['default_gateway'] or '-'}"
    ]
    for svc in snap["services"]:
        flag = "on " if svc["enabled"] else "off"
        ip = svc["ipv4"] or "-"
        lines.append(
            f"    [{flag}] {svc['kind']:8}  {svc['name']}"
            f"  {svc['device'] or '-'}  {ip}"
        )
    return "\n".join(lines)


def ethernet_services(snap: dict) -> list[dict]:
    return [s for s in snap["services"] if s["kind"] == "ethernet"]


def cmd_status(_args: argparse.Namespace) -> int:
    snap = snapshot()
    print(format_snapshot(snap))
    ether = ethernet_services(snap)
    if not ether:
        print("\nNo dock/USB/Thunderbolt Ethernet service found.")
        print("If the dock is plugged in, open System Settings → Network and tell Luke the name.")
        return 0
    if snap["default_kind"] == "ethernet":
        print("\nThis Mac is currently using DOCK ETHERNET as its internet path.")
        print("That is the handoff we suspect in the Logos crashes.")
    elif snap["default_kind"] == "wifi":
        print("\nThis Mac is currently using Wi-Fi as its internet path.")
    return 0


def append_log(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text.rstrip() + "\n")


def cmd_watch(args: argparse.Namespace) -> int:
    log_path = Path(args.log).expanduser()
    last_key = None
    print(f"Watching network changes. Log: {log_path}", file=sys.stderr)
    print("Stay on Wi-Fi for the test; Ctrl+C to stop.", file=sys.stderr)
    while True:
        snap = snapshot()
        key = (
            snap["default_kind"],
            snap["default_interface"],
            snap["default_ipv4"],
            tuple((s["name"], s["enabled"], s["ipv4"]) for s in snap["services"]),
        )
        heartbeat = last_key is None or args.always
        changed = key != last_key
        if changed or heartbeat:
            block = format_snapshot(snap)
            if changed and last_key is not None:
                block = "CHANGE\n" + block
            append_log(log_path, block + "\n")
            print(block)
            last_key = key
        time.sleep(max(5, args.interval))


def set_ethernet_enabled(enabled: bool, dry_run: bool) -> int:
    snap = snapshot()
    ether = ethernet_services(snap)
    if not ether:
        print("No dock/USB/Thunderbolt Ethernet service found.")
        return 1
    action = "enable" if enabled else "disable"
    for svc in ether:
        print(f"{action}: {svc['name']} (currently {'on' if svc['enabled'] else 'off'})")
        if dry_run:
            continue
        flag = "on" if enabled else "off"
        out = run(["networksetup", "-setnetworkserviceenabled", svc["name"], flag])
        if out.strip():
            print(out.strip())
    if dry_run:
        print("Dry run only. Re-run without --dry-run to apply.")
        return 0
    print("\nNew status:")
    print(format_snapshot(snapshot()))
    return 0


def cmd_disable_ethernet(args: argparse.Namespace) -> int:
    print("This turns OFF dock Ethernet so the Mac keeps using Wi-Fi.")
    print("Displays on the dock can stay plugged in.")
    return set_ethernet_enabled(False, args.dry_run)


def cmd_enable_ethernet(args: argparse.Namespace) -> int:
    return set_ethernet_enabled(True, args.dry_run)


def cmd_install_watch(args: argparse.Namespace) -> int:
    script = Path(__file__).resolve()
    python = shutil.which("python3") or sys.executable
    log_path = str(Path(args.log).expanduser())
    plist = {
        "Label": "ca.logosnetworkwatch",
        "ProgramArguments": [
            python,
            str(script),
            "watch",
            "--interval",
            str(args.interval),
            "--log",
            log_path,
        ],
        "RunAtLoad": True,
        "KeepAlive": True,
        "StandardOutPath": str(Path.home() / "Library/Logs/LogosNetworkWatch.out.log"),
        "StandardErrorPath": str(Path.home() / "Library/Logs/LogosNetworkWatch.err.log"),
    }
    LAUNCH_AGENT.parent.mkdir(parents=True, exist_ok=True)
    with LAUNCH_AGENT.open("wb") as handle:
        plistlib.dump(plist, handle)
    run(["launchctl", "unload", str(LAUNCH_AGENT)])
    loaded = run(["launchctl", "load", str(LAUNCH_AGENT)])
    print(f"Installed {LAUNCH_AGENT}")
    print(f"Log file: {log_path}")
    if loaded.strip():
        print(loaded.strip())
    print("This is a LaunchAgent (the macOS equivalent of cron). It only logs.")
    print("It does not change Wi-Fi/Ethernet or ping anything.")
    return 0


def cmd_uninstall_watch(_args: argparse.Namespace) -> int:
    run(["launchctl", "unload", str(LAUNCH_AGENT)])
    if LAUNCH_AGENT.exists():
        LAUNCH_AGENT.unlink()
        print(f"Removed {LAUNCH_AGENT}")
    else:
        print("No LaunchAgent installed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Log Wi-Fi vs dock Ethernet. Do not force-switch or keep-alive."
    )
    parser.add_argument(
        "--log",
        default=str(DEFAULT_LOG),
        help="Log file path (default: ~/Documents/LogosNetworkWatch.log)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Seconds between watch samples (default: 30)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show Wi-Fi vs Ethernet right now")
    watch = sub.add_parser("watch", help="Log default-route changes")
    watch.add_argument(
        "--always",
        action="store_true",
        help="Write a heartbeat on every interval, not only on changes",
    )
    disable = sub.add_parser(
        "disable-ethernet",
        help="Turn off dock Ethernet so the Mac stays on Wi-Fi",
    )
    disable.add_argument("--dry-run", action="store_true")
    enable = sub.add_parser("enable-ethernet", help="Turn dock Ethernet back on")
    enable.add_argument("--dry-run", action="store_true")
    sub.add_parser("install-watch", help="Install LaunchAgent logger")
    sub.add_parser("uninstall-watch", help="Remove LaunchAgent logger")
    return parser


def main() -> int:
    if sys.platform != "darwin":
        print("This script is for Martin's Mac. Run it there with python3.", file=sys.stderr)
        return 2
    parser = build_parser()
    args = parser.parse_args()
    commands = {
        "status": cmd_status,
        "watch": cmd_watch,
        "disable-ethernet": cmd_disable_ethernet,
        "enable-ethernet": cmd_enable_ethernet,
        "install-watch": cmd_install_watch,
        "uninstall-watch": cmd_uninstall_watch,
    }
    return commands[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
