# HIRO: SEND TO TOMMY

Reply on case **01275856** (existing thread, no new case, no attachments).

Paste from [`live/HIRO-SEND-TO-TOMMY.md`](HIRO-SEND-TO-TOMMY.md) or [`live/2026-08-20/crash/TOMMY-FOLLOWUP.md`](2026-08-20/crash/TOMMY-FOLLOWUP.md).

IPS write-up: [`live/2026-08-20/crash/IPS-ANALYSIS.md`](2026-08-20/crash/IPS-ANALYSIS.md). Tonight's `.ips` / `Logos.log` / `LogosError.log` are in `live/2026-08-20/crash/`.

---

# CRASH — 20 Aug 2026 21:13:33 EDT (still down as of 21:47)

Martin's Mac17,8, Logos **52.2.0.0019** ARM64.

**CRASH:** PID **14227** (up ~4h03m since 17:10) **GONE** at **21:13:35**. **SIGSEGV** in native code: `our_sigsegv_signal_handler` (MonoHost) → **`addSessionReference`** (SystemConfiguration). `.ips`: `Logos-2026-08-20-211336.ips` (in `~/Library/Logs/DiagnosticReports/Retired/`). No new ips/hang since.

**At crash:** dual-path **dock Ethernet** `en7` 10.0.0.163 + Wi-Fi 10.0.0.43, **AC**, last wake **16:16:29**. Last heartbeat 21:13:24 still running rss=1381MB cef=13. Last `network_change` was **20:59** (14 min earlier), not at the crash instant.

**Now (21:47):** Logos **still not running** (~33 min). pid=none rss=n/a cef=0. Dual-path Ethernet `en7` 10.0.0.163 + Wi-Fi 10.0.0.43, **AC** (battery 85% not charging), last wake **16:16:29**. No relaunch. Watchers still up (watch pid 5278, grab pid 7664).

## Grabs around crash (`~/Documents/LogosLiveWatch-screens/`)

Not pushed (too large). Last-before / at / after:

- `2026-08-20T21-12-14-D1.jpg` `…-D2.jpg` `…-D3.jpg`
- `2026-08-20T21-13-15-D1.jpg` `…-D2.jpg` `…-D3.jpg` (~18s before SIGSEGV)
- `2026-08-20T21-14-15-D1.jpg` `…-D2.jpg` `…-D3.jpg` (after GONE)

Also 21:10 / 21:11 / 21:15. Latest grab 21:46-28 (Logos still down).

## Timeline today

| Time | What |
|---|---|
| 17:10:04 | Relaunch PID 14227 on dock Ethernet + Wi-Fi, AC |
| 20:16–20:17 | RSS ~389→1582 MB, active use |
| 20:43:15 | 2× `network_change`. Survived. RSS dropping |
| 20:59:01 | 2× `network_change`. Survived at ~467 MB |
| 21:01–21:07 | RSS climbed again ~1528–1545 MB, cpu 18–34%, threads ~109 |
| 21:12:10 | SCAN still up: rss=1433MB threads=111 ifaces=en7 en0 |
| 21:13:24 | Heartbeat still up: rss=1381MB cef=13 dual-path AC |
| **21:13:33** | **SIGSEGV NativeSignalException / addSessionReference** |
| 21:13:35 | ALERT GONE pid 14227 |
| 21:13:45 | ALERT new ips `Logos-2026-08-20-211336.ips` |
| 21:17–21:42 | SCAN logos=not-running ifaces=en7 en0 |
| **21:47** | Still not running. Dual-path, AC. Watchers up |

Also immediately before SIGSEGV: Logos.log `WebBrowser.WebBrowserInteropController` / `logos.hybrid-ui.runProxiedFunction`: Function not found.

## Last EVENTS

```
21:12:10  SCAN  pid 14227 rss=1433MB cpu=3.4% threads=111  ifaces=en7 en0
21:13:35  ALERT  logos process GONE (was pid 14227)
21:13:35  CRASH  NativeSignalException: Got a SIGSEGV while executing native code.
21:13:35  CRASH  0 our_sigsegv_signal_handler [MonoHost]
21:13:35  CRASH  10 addSessionReference [SystemConfiguration]
21:13:45  ALERT  new crash report Logos-2026-08-20-211336.ips
21:17:10  SCAN  logos=not-running  ifaces=en7 en0
21:22:10  SCAN  logos=not-running  ifaces=en7 en0
21:27:10  SCAN  logos=not-running  ifaces=en7 en0
21:32:10  SCAN  logos=not-running  ifaces=en7 en0
21:37:11  SCAN  logos=not-running  ifaces=en7 en0
21:42:11  SCAN  logos=not-running  ifaces=en7 en0
```

## Case

01275856 (Tommy Ball). Live catch of the `addSessionReference` SIGSEGV.
