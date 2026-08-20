# Status — 20 Aug 2026 16:28 EDT

Martin's Mac17,8, Logos **52.2.0.0019** ARM64, Word also open.

**Now:** Logos PID **8378**, ~1.9 GB, ~10 CEF processes, **Wi-Fi** `en0` 10.0.0.43, **battery**. Last wake **16:16:29**. No SIGSEGV yet.

## Timeline today

| Time | What |
|---|---|
| 15:56 | Watcher started. Logos PID 4954 on **dock Ethernet** (`en7` 10.0.0.163) + Wi-Fi dual-path, AC |
| 16:14:01 | PID 4954 gone; Logos relaunched PID 7507 (still Ethernet) |
| 16:16:03 | **CHANGE** Ethernet → Wi-Fi, AC → battery (undock) |
| 16:16:14 | Clamshell sleep ~15s; TeamViewer dropped |
| 16:16:29 | Wake because **lid opened**. Logos survived (same PID 7507) |
| 16:20:41 | Logos started again PID 8378 (no SIGSEGV, no new crash report). Window was gone at 16:20:30 grab |

## Thread sample (16:24, PID 8378)

15× `NetworkConfigWatcher`, 1× `NetworkNotificationThreadMac`, 1× `.NET Network Address Change`. SystemConfiguration.framework loaded. That is the crash-stack mix, idle until a handoff.

## Not a crash yet

No `addSessionReference` / SIGSEGV in today's `Logos.log`. Cover-download and panel-link errors are normal startup noise.

## Case

01275856 (Tommy Ball).
