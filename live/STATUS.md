# CRASH — 20 Aug 2026 21:13:33 EDT

Martin's Mac17,8, Logos **52.2.0.0019** ARM64.

**CRASH:** PID **14227** (up ~4h03m since 17:10) **GONE** at **21:13:35**. **SIGSEGV** in native code: `our_sigsegv_signal_handler` (MonoHost) → **`addSessionReference`** (SystemConfiguration). New `.ips`: `Logos-2026-08-20-211336.ips` (now in `~/Library/Logs/DiagnosticReports/Retired/`).

**At crash:** dual-path **dock Ethernet** `en7` 10.0.0.163 + Wi-Fi 10.0.0.43, **AC**, last wake **16:16:29**. Last heartbeat 21:13:24 still running rss=1381MB cef=13. Last `network_change` was **20:59** (14 min earlier), not at the crash instant.

**Now:** Logos not running. Watchers still up. Dual-path Ethernet+Wi-Fi, AC.

## Grabs around crash (`~/Documents/LogosLiveWatch-screens/`)

Not pushed (too large). Last-before / at / after:

- `2026-08-20T21-12-14-D1.jpg` `…-D2.jpg` `…-D3.jpg`
- `2026-08-20T21-13-15-D1.jpg` `…-D2.jpg` `…-D3.jpg` (~18s before SIGSEGV)
- `2026-08-20T21-14-15-D1.jpg` `…-D2.jpg` `…-D3.jpg` (after GONE)

Also 21:10 / 21:11 / 21:15.

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

Also immediately before SIGSEGV: Logos.log `WebBrowser.WebBrowserInteropController` / `logos.hybrid-ui.runProxiedFunction`: Function not found.

## Last EVENTS

```
21:02:10  SCAN  pid 14227 rss=1545MB cpu=18.0% threads=109  ifaces=en7 en0
21:07:10  SCAN  pid 14227 rss=1399MB cpu=33.7% threads=97  ifaces=en7 en0
21:12:10  SCAN  pid 14227 rss=1433MB cpu=3.4% threads=111  ifaces=en7 en0
21:13:35  ALERT  logos process GONE (was pid 14227)
21:13:35  CRASH  NativeSignalException: Got a SIGSEGV while executing native code.
21:13:35  CRASH  0 our_sigsegv_signal_handler [MonoHost]
21:13:35  CRASH  10 addSessionReference [SystemConfiguration]
21:13:45  ALERT  new crash report Logos-2026-08-20-211336.ips
21:17:10  SCAN  logos=not-running  ifaces=en7 en0
```

## Case

01275856 (Tommy Ball). Live catch of the `addSessionReference` SIGSEGV.
