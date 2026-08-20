# Watch plan — Hiro (Luke) ↔ Grok on Martin's Mac

Coordination for case **01275856** (Tommy Ball). Logos **52.2.0.0019 ARM64** on Martin's **Mac17,8**.

## Goal (through Friday night 2026-08-22 ET)

Keep the live watch running and try to witness a real crash (`SIGSEGV` / `addSessionReference` / new crash report). Luke and Hiro want a live catch.

Hiro's watch ends Friday night **2026-08-22** (or sooner if a real crash is reported). After that: one wrap-up and stop.

## What Hiro does

Hiro (Luke's Grok Bot) polls GitHub `live/` about every 15 minutes on weekdays **8am–10pm ET**. Stays silent if nothing changed. Pings Luke on a real crash or a new undock / sleep / wake / unexpected PID death.

## What Grok on Martin's Mac should keep doing

- Keep `scripts/logos_live_watch.py` (LaunchAgent `ca.logoslivewatch`), screen grab, and notify watch running while Martin uses Logos.
- Keep pushing `live/STATUS.md` and `live/YYYY-MM-DD/EVENTS.log` about every 15 minutes. Push `THREADS.txt` when the process or network mix changes.
- Do **not** wipe `WATCH-PLAN.md` or other root/docs files when you refresh `live/`.
- Leave screen JPEGs on disk at `~/Documents/LogosLiveWatch-screens/` (too large for the timer). On a real crash, immediately update STATUS/EVENTS with the crash signature and times, then attach/push the grabs around that timestamp (and the new Logos.log / crash report if you have them).
- If Logos dies without `SIGSEGV` / `addSessionReference`, still log the PID change and say it was not crash-signed.

## Last snapshot Hiro has (2026-08-20 4:28pm ET)

- Logos PID **8378**, ~1.9 GB, Wi-Fi, battery, no SIGSEGV.
- Timeline:
  - Watcher 3:56pm: PID 4954, dock Ethernet
  - 4:14: PID 4954 gone, relaunched 7507
  - 4:16: undock Ethernet→Wi-Fi, AC→battery, lid sleep ~15s, survived 7507
  - ~4:20: window gone, new PID 8378
- Crash-stack threads loaded and idle: many `NetworkConfigWatcher` + `NetworkNotificationThreadMac` + .NET Network Address Change.

## Support note

Intel QEMU / Intel DMG on Luke's side will **not** reproduce this ARM + SystemConfiguration + CalDigit crash. Live catch on Martin's Mac is the useful path.

## How to sync

- `git pull` on Martin's checkout to see this plan.
- Keep pushing `live/` so Hiro can see it.
- Luke's Mac Mini git is currently broken (Xcode CLT), so Hiro reads `live/` from GitHub raw, not from `~/dev/logosapp`.
