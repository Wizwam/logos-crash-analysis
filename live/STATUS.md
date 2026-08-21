# Status — 20 Aug 2026 20:16 EDT

Martin's Mac17,8, Logos **52.2.0.0019** ARM64.

**Now:** Logos PID **14227** (same since 17:10, ~186 min), ~1428 MB, **dock Ethernet** `en7` 10.0.0.163 + Wi-Fi dual-path, **AC**. Last wake **16:16:29**. **No SIGSEGV.** No new Logos `.ips`/hang.

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
| 17:38:38 | 1× `network_change` (en7+en0). PID 14227 survived. Still Ethernet dual-path |
| 18:01–18:03 | RSS 962→464 MB (same PID) |
| 18:21 | RSS 486→~277 MB (same PID) |
| 18:25:40 | WAKE+SLEEP same second. PID 14227 survived. Notify watch restarted 18:27 |
| 18:37:55 | 2× `network_change` (en7+en0). PID 14227 survived. Still Ethernet dual-path |
| 19:16 | RSS ~278→~238 MB (same PID) |
| 19:31 | RSS climbed ~238→~372 MB (same PID) |
| 19:38:52 | 2× `network_change` (en7+en0). PID 14227 survived. Still Ethernet dual-path |
| 20:12 | SCAN still ~389 MB, 76 threads, dual-path |
| **20:16** | RSS ~389→~1428 MB, cef 3→17 (same PID). Active use; panel-link errors in Logos.log |

## Last EVENTS

```
19:38:52  NOTIFY  NETWORK  network_change  ifaces=en7 en0  pid 14227
19:38:53  NOTIFY  NETWORK  network_change  ifaces=en7 en0  pid 14227
19:52:09  SCAN  pid 14227 rss=387MB threads=76  ifaces=en7 en0
19:57:09  SCAN  pid 14227 rss=388MB threads=76  ifaces=en7 en0
20:02:09  SCAN  pid 14227 rss=389MB threads=76  ifaces=en7 en0
20:07:09  SCAN  pid 14227 rss=389MB threads=76  ifaces=en7 en0
20:12:10  SCAN  pid 14227 rss=389MB threads=76  ifaces=en7 en0
```

## Not a crash

No `addSessionReference` / SIGSEGV. RSS climb and panel-link errors are same-process, not GONE.

## Case

01275856 (Tommy Ball).
