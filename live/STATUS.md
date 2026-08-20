# Status — 20 Aug 2026 17:01 EDT

Martin's Mac17,8, Logos **52.2.0.0019** ARM64.

**Now:** Logos **not running** (still, since clean quit). Dock Ethernet `en7` 10.0.0.163 + Wi-Fi dual-path, **AC**. Last wake **16:16:29**. **No SIGSEGV.** No new Logos `.ips`/hang. No relaunch.

Last GONE: pid **8378** at **16:45:51** — **clean quit**, not a crash (Logos.log shutdown window → `Shutting down` → `Exiting.`). SCANs 16:50 / 16:55 / 17:00 all `not-running`.

Watchers: live watch LaunchAgent, screen grab, notify watch still running. Goal: live catch through Friday 2026-08-22.

## Timeline today

| Time | What |
|---|---|
| 15:56 | Watcher started. Logos PID 4954 on dock Ethernet + Wi-Fi, AC |
| 16:14:01 | PID 4954 gone; relaunched 7507 (still Ethernet). Not crash-signed |
| 16:16:03 | Undock: Ethernet → Wi-Fi, AC → battery |
| 16:16:14 | Clamshell sleep ~15s; lid-open wake 16:16:29; survived 7507 |
| 16:20:41 | Window gone; new PID 8378. No SIGSEGV / no new crash report |
| 16:38:35 | Redock: AC, then 5× `network_change` (en0+en7), threads 97→102 |
| 16:38:45 | Default path Ethernet `en7`. Dual-path. PID 8378 survived the burst |
| 16:45:43 | Clean shutdown (Logos.log). Watcher ALERT GONE 16:45:51 |
| **17:01** | **Still not running.** Dual-path Ethernet, AC. Waiting for relaunch |

## Last EVENTS

```
16:45:51  ALERT  logos process GONE (was pid 8378)
16:50:40  SCAN  logos=not-running  ifaces=en7 en0
16:55:40  SCAN  logos=not-running  ifaces=en7 en0
17:00:40  SCAN  logos=not-running  ifaces=en7 en0
```

## Not a crash

No `addSessionReference` / SIGSEGV. 16:14, 16:20, and **16:45** exits were not crash-signed.

## Case

01275856 (Tommy Ball).
