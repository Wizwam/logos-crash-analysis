# Live watch (Martin's Mac, 20 Aug 2026)

Grok on Martin's MacBook is watching Logos while he works. This folder is overwritten about every 15 minutes so Luke can pull on a PC.

```
git pull
live/STATUS.md                 # current snapshot
live/2026-08-20/EVENTS.log     # handoff / sleep / pid / crash lines only
live/2026-08-20/LogosLiveWatch.log   # full watcher log (when synced)
live/2026-08-20/THREADS.txt    # NetworkConfigWatcher / .NET threads from a 1s sample
```

Screen JPEGs stay on Martin's Mac (`~/Documents/LogosLiveWatch-screens/`, last 2 hours). They are not pushed on the timer (too large). On a real crash we will attach the grabs around that timestamp.

Watchers running on the Mac:

- `scripts/logos_live_watch.py watch` (LaunchAgent `ca.logoslivewatch`)
- `scripts/logos_live_watch.py grab --every 60`
- `scripts/logos_notify_watch.py` (Darwin `network_change` / sleep / wake)
