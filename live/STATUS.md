# Status — 20 Aug 2026 17:47 EDT

Martin's Mac17,8, Logos **52.2.0.0019** ARM64.

**Now:** Logos PID **14227** (same since 17:10), ~962 MB, **dock Ethernet** `en7` 10.0.0.163 + Wi-Fi dual-path, **AC**. Last wake **16:16:29**. **No SIGSEGV.** No new Logos `.ips`/hang.

Watchers: live watch LaunchAgent, screen grab, notify watch. Goal: live catch through Friday 2026-08-22.

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
| 17:10:04 | Relaunch PID 14227 on dock Ethernet + Wi-Fi, AC |
| 17:25:40 | Brief SLEEP+WAKE same second. PID 14227 survived. No net CHANGE |
| **17:38:38** | 1× `network_change` (en7+en0). PID **14227 survived**. Still Ethernet dual-path |

## Last EVENTS

```
17:35:41  SCAN  pid 14227 rss=962MB threads=78  ifaces=en7 en0
17:38:38  NOTIFY  NETWORK  network_change  ifaces=en7 en0  pid 14227
17:40:41  SCAN  pid 14227 rss=962MB threads=77  ifaces=en7 en0
17:45:41  SCAN  pid 14227 rss=962MB threads=77  ifaces=en7 en0
```

## Not a crash

No `addSessionReference` / SIGSEGV. 16:14, 16:20, and 16:45 exits were not crash-signed. 17:25 sleep/wake and 17:38 network_change did not kill Logos.

## Case

01275856 (Tommy Ball).
