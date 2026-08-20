# Status — 20 Aug 2026 16:42 EDT

Martin's Mac17,8, Logos **52.2.0.0019** ARM64, Word also open.

**Now:** Logos PID **8378** (same since 16:20), ~2.0 GB, **dock Ethernet** `en7` 10.0.0.163 + Wi-Fi dual-path, **AC**. Last wake **16:16:29**. **No SIGSEGV.**

Watchers: live watch LaunchAgent, screen grab, notify watch. Hiro's `WATCH-PLAN.md` received (repo root). Goal: live catch through Friday 2026-08-22.

## Timeline today

| Time | What |
|---|---|
| 15:56 | Watcher started. Logos PID 4954 on dock Ethernet + Wi-Fi, AC |
| 16:14:01 | PID 4954 gone; relaunched 7507 (still Ethernet). Not crash-signed |
| 16:16:03 | Undock: Ethernet → Wi-Fi, AC → battery |
| 16:16:14 | Clamshell sleep ~15s; lid-open wake 16:16:29; survived 7507 |
| 16:20:41 | Window gone; new PID 8378. No SIGSEGV / no new crash report |
| **16:38:35** | **Redock:** AC, then 5× `network_change` (en0+en7), threads 97→102 |
| **16:38:45** | Default path **Ethernet** `en7`. Dual-path. PID 8378 survived the burst |

## Threads

At 16:24 (Wi-Fi): 15× `NetworkConfigWatcher` + `NetworkNotificationThreadMac` + `.NET Network Address Change`. At dock burst, thread count 94–102 then 96.

## Not a crash yet

No `addSessionReference` / SIGSEGV. 16:14 and 16:20 PID changes were not crash-signed.

## Case

01275856 (Tommy Ball).
