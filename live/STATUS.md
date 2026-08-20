# Status — 20 Aug 2026 16:47 EDT

Martin's Mac17,8, Logos **52.2.0.0019** ARM64.

**Now:** Logos **not running**. **ALERT GONE** pid **8378** at **16:45:51**. Dock Ethernet `en7` 10.0.0.163 + Wi-Fi dual-path, **AC**. Last wake **16:16:29**. **No SIGSEGV.** No new Logos `.ips`/hang.

This GONE is a **clean quit**, not a crash: Logos.log `16:45:43 Showing shutdown window` → `Shutting down application` → `Exiting.` RSS had already dropped (2171→1293 MB) during dispose.

Grabs around GONE (local only): `2026-08-20T16-45-34-D1.jpg` (and D2/D3), `2026-08-20T16-46-35-D1.jpg` (and D2/D3).

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
| **16:45:43** | **Clean shutdown** (Logos.log). Watcher ALERT GONE 16:45:51 |

## Last EVENTS

```
16:38:45  CHANGE  net=ethernet en7 dual-path power=ac
16:40:40  SCAN  pid 8378 rss=2068MB threads=96  ifaces=en7 en0
16:45:40  SCAN  pid 8378 rss=1293MB threads=96  ifaces=en7 en0
16:45:51  ALERT  logos process GONE (was pid 8378)
```

## Not a crash

No `addSessionReference` / SIGSEGV. 16:14, 16:20, and **16:45** exits were not crash-signed.

## Case

01275856 (Tommy Ball).
