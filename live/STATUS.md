# STATUS — 1 Sep 2026 20:17 EDT (post network-plist reset)

Martin's Mac17,8. Logos **53.1.0.0002** ARM64. Case **01280447** (Tommy Ball).

## Now

Logos **running** PID **1236**, up ~2 min at first sample, rss climbing ~1.1–1.6 GB, dock Ethernet `en7` 10.0.0.163 + Wi-Fi `en0` 10.0.0.110, **AC**, dual-path, tm=idle.

Watchers:

- `ca.logoslivewatch` (LaunchAgent) `watch --interval 10 --heartbeat 60`
- `logos_live_watch.py grab --every 60`
- `logos_notify_watch.py` (network / sleep / wake + Logos unified-log errors)

No new `.ips` since reboot. `systemextensionsctl list` → **0 extension(s)** (Malwarebytes gone).

## Tommy step 1 (31 Aug) — done tonight

Reset macOS network prefs, then reboot:

- Moved `NetworkInterfaces.plist` and `preferences.plist` out of `/Library/Preferences/SystemConfiguration/`
- Backup: `~/Desktop/Logos-NetworkPrefs-backup-20260901-200936`
- `com.apple.airport.preferences.plist` could not be moved (macOS blocked it)
- macOS regenerated `NetworkInterfaces.plist` and `preferences.plist` at 20:13 after reboot
- Fresh user account **not** created (Tommy: only if crashes continue)

## Last real crash

**30 Aug 14:37** — Logos 53.1.0.0002, PID 9879, ~41 h up, **Wi-Fi only**. Same `0x01004008910043f8` / `addSessionReference` / 23 `NetworkConfigWatcher`. See `live/2026-08-30/crash/`.

20 Aug 21:13 catch is in `live/2026-08-20/`.

## Tonight GONE packages (not crashes)

Watch packaged PID 29906 (pre-reboot quit) and PID 854 (splash vs main at relaunch). No SIGSEGV.
