# IPS analysis — Logos-2026-08-20-211336.ips

Compared with:

- `Logos-2026-08-15-194851.ips`
- `Logos-2026-08-19-171802.ips`

These are the same crash, not three different ones.

## Tonight

| | |
|---|---|
| File | `live/2026-08-20/crash/Logos-2026-08-20-211336.ips` |
| App | Logos 52.2.0.0019 (`5202.0.19`), `com.logos.desktop.logos` |
| Mac | Mac17,8, ARM-64 native (`translated: false`), macOS 26.6.2 (25G83) |
| PID | 14227 |
| Launch | 2026-08-20 17:10:02 EDT |
| Crash | 2026-08-20 21:13:33 EDT (~4h 3m) |
| Role | Foreground |
| Parent | launchd |
| SIP | enabled |
| Code sign | team `G2ET27DGDP` |
| wakeTime | 17824 s (~5 h since last lid wake 16:16) |
| uptime | 33000 s |

## Wrapper vs real fault

IPS top-level:

- `exception.type`: `EXC_BAD_ACCESS`
- `exception.signal`: `SIGABRT` (because Logos then calls `abort()`)
- `exception.subtype`: `KERN_INVALID_ADDRESS at 0x01004008910043f8`
- `termination`: Abort trap: 6, `byProc: Logos`
- `asi`: `abort() called`
- `vmRegionInfo`: that address is **not in any region** (unused space)

MonoHost `our_sigsegv_signal_handler` catches SIGSEGV, AppKit reports it, `-[OurApp ReportUnhandledNativeException:]` aborts. The translated reports saying SIGSEGV are describing the root fault. The IPS listing SIGABRT is the abort after that handler.

## Crashed thread

- index 108, thread id 1163354, `triggered: true`
- **no name**
- queue: `*/client sessions` (SystemConfiguration)

Stack (symbols):

```
__pthread_kill
pthread_kill
__abort / abort
(unnamed, likely CoreCLR/Logos abort path)
-[OurApp ReportUnhandledNativeException:]
-[NSApplication reportException:]
NSApplicationUncaughtExceptionHandler
NSExceptionHandlerUncaughtExceptionHandler
our_sigsegv_signal_handler          # MonoHost
invoke_previous_action(...)         # libcoreclr
_sigtramp
_objc_msgSend_uncached              # twice — message send to a bad object
__CFCopyFormattingDescription
__CFSTRING_IS_CALLING_OUT_TO_AN_OBJECT_FORMAT_ARGUMENT_WITH_LOCALE__
__CFStringAppendFormatCore
CFStringAppendFormatAndArguments
CFStringAppendFormat
addSessionReference                 # SystemConfiguration
__CFSetApplyFunction_block_invoke
CFBasicHashApply
CFSetApplyFunction
__add_state_handler_block_invoke    # SystemConfiguration
___os_state_request_for_self_impl_block_invoke
_dispatch_...
```

So SC is walking its client-session set to produce an `os_state` dump, and `addSessionReference` tries to **format a description** of a session that is already a garbage object.

## Identical fingerprint (15 / 19 / 20 Aug)

| Crash | PID | Logos up | wakeTime | NetworkConfigWatcher | Fault address | Queue |
|---|---|---|---|---|---|---|
| 15 Aug 19:48 | 66858 | ~1h 14m | 2637 s | **23** | `0x01004008910043f8` | `*/client sessions` |
| 19 Aug 17:17 | 1639 | ~21h | 21399 s | **23** | same | same |
| 20 Aug 21:13 | 14227 | ~4h 3m | 17824 s | **23** | same | same |

Stacks match through `addSessionReference` → `CFStringAppendFormat` → `objc_msgSend` → Mono SIGSEGV handler → `ReportUnhandledNativeException` → `abort`.

The same unmapped pointer three days in a row is not random heap garbage. It looks like a poisoned / truncated / tagged pointer sitting in SC's session table.

## Other threads in tonight's dump (134 total)

Always present at crash:

- 23 × `NetworkConfigWatcher` (CEF)
- `NetworkNotificationThreadMac` (CEF)
- `.NET Network Address Change`
- `CrBrowserMain` (main thread, not the crasher)

Also CEF/V8 workers, .NET TP workers, USB hotplug. Fits Tommy's network-handoff theory: many SC clients in one process. The crash site is a **delayed** print of an already-corrupt session, not the instant the path flips.

Tonight: dual-path dock Ethernet `en7` + Wi-Fi, AC, last `network_change` at 20:59 (14 min before the crash). Native ARM, not Rosetta. Not a codesign/SIP failure. Not an obvious OOM.
