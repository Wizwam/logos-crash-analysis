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
- Do **not** wipe `WATCH-PLAN.md`, `grabs/`, or other root/docs files when you refresh `live/`.
- Leave the rolling 2-hour JPEG buffer on disk at `~/Documents/LogosLiveWatch-screens/` (too large for the timer — do **not** push that folder). Pick a few email-ready stills into `grabs/` as specified below. On a real crash, immediately update STATUS/EVENTS with the crash signature and times, then commit the 2–4 grabs nearest that timestamp (and the new Logos.log / crash report if you have them).
- If Logos dies without `SIGSEGV` / `addSessionReference`, still log the PID change and say it was not crash-signed.
- Do **not** email Tommy from the Mac. Hiro (Luke) pulls selected grabs from GitHub for the support email. No Tommy email until a real crash.

## Last snapshot Hiro has (2026-08-20 4:28pm ET)

- Logos PID **8378**, ~1.9 GB, Wi-Fi, battery, no SIGSEGV.
- Timeline:
  - Watcher 3:56pm: PID 4954, dock Ethernet
  - 4:14: PID 4954 gone, relaunched 7507
  - 4:16: undock Ethernet→Wi-Fi, AC→battery, lid sleep ~15s, survived 7507
  - ~4:20: window gone, new PID 8378
- Crash-stack threads loaded and idle: many `NetworkConfigWatcher` + `NetworkNotificationThreadMac` + .NET Network Address Change.

## Screen grabs for Tommy (Grok on Martin's Mac)

Start sending a few **email-ready** stills to git. Hiro (Luke) will pull them from GitHub for the Tommy email (case **01275856**). **Do not email Tommy from the Mac.**

**Do not** push the rolling 2-hour JPEG buffer (`~/Documents/LogosLiveWatch-screens/`, already ~14 MB+). Too large, and not useful in email.

**Do** pick a few good stills and commit them under `grabs/YYYY-MM-DD/` at the repo root (not under `live/`, so the 15-minute live refresh cannot wipe them).

What “a few good” means:

- Small JPEGs (screen capture as jpg is fine; keep each reasonable for email, not full-quality 14 MB dumps).
- Logos window actually visible (not a lock screen, not an empty desktop).
- Prefer shots that show context Tommy can use: Logos running at the desk (docked), Logos after undock / on Wi-Fi, and any shot around a crash, hang, or unexpected window-gone.
- Cadence: a couple per session / after a notable handoff or PID change — not every 60 seconds. On a real crash, attach the 2–4 grabs nearest that timestamp plus update STATUS/EVENTS as already specified.
- Name files with local time, e.g. `grabs/2026-08-20/1645-docked-logos.jpg`.

When you refresh `live/`, do **not** wipe `WATCH-PLAN.md`, `grabs/`, or other root/docs files.

## Support note

Intel QEMU / Intel DMG on Luke's side will **not** reproduce this ARM + SystemConfiguration + CalDigit crash. Live catch on Martin's Mac is the useful path.

## How to sync

- `git pull` on Martin's checkout to see this plan.
- Keep pushing `live/` so Hiro can see it.
- Also push a few email-ready stills under `grabs/` (not the rolling JPEG buffer).
- Luke's Mac Mini git is currently broken (Xcode CLT), so Hiro reads `live/` from GitHub raw, not from `~/dev/logosapp`.
