# IPS analysis — Logos-2026-08-30-143710.ips

Same fingerprint as 15 / 19 / 20 Aug, now on **Logos 53.1.0.0002**. Upgrading did not fix it.

## Crash

| | |
|---|---|
| When | 30 Aug 2026 14:37:05 EDT |
| App | Logos **53.1.0.0002** (`5301.0.2`), native ARM-64 |
| Mac | Mac17,8, macOS 26.6.2 (25G83) |
| PID | 9879, launched 28 Aug 21:20:10, up ~41 h |
| Fault | `EXC_BAD_ACCESS` / `KERN_INVALID_ADDRESS at 0x01004008910043f8` |
| Wrapper | `SIGABRT` / `abort()` after Mono `our_sigsegv_signal_handler` |
| Queue | `*/client sessions` |
| NetworkConfigWatcher | **23** |
| wakeTime | 3060 s (~51 min after 13:46 wake) |

At crash the live watch had **Wi-Fi only** (`en0` 10.0.0.110), battery, no dock Ethernet. ~5 min earlier: Navigating Mt 26, then CEF `Function 0 not found` / `runProxiedFunction`.

Stack matches the earlier dumps: `os_state_request_for_self` → `addSessionReference` → `CFStringAppendFormat` → `objc_msgSend` on a bad object → SIGSEGV → Logos abort.

So this is not dock-Ethernet-only. Same poisoned pointer after the 53.1 upgrade, on Wi-Fi, after a long-running process.
