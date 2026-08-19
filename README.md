# Logos crash analysis (case 01275856)

Scratch workspace for **Martin Webster**’s Logos Bible Software crashes on a **Mac17,8 (M5 MacBook Pro)**. Not a product codebase.

Logos Technical Support: Tommy Ball, **case 01275856**. Keep follow-ups on that case.

## Hardware / environment

| | |
|---|---|
| Machine | Mac17,8 (M5 MacBook Pro), 24 GB, 18 cores |
| OS at freeze (18 Aug) | macOS 26.6.1 (25G76) |
| OS at crash (19 Aug) | macOS 26.6.2 (25G83) |
| App | Logos **52.2.0.0019**, **ARM-64 Native** (`Arm64 running on Apple Silicon`) |
| Desk dock | CalDigit TS5 (Thunderbolt 5). All three displays through that one dock (two native Thunderbolt, one Thunderbolt-to-HDMI dongle). Dock 2.5GbE is Ethernet to the house router. |
| Other | Malwarebytes present (exclusion requested). iCloud Private Relay was turned off for testing. |

`LogosCrash.txt` inside every zip is a **stale 25 Jun 2026 / version 51.1 / MacBookPro18,1** file. Ignore it. Use `Logos.log` plus the translated macOS `.docx` reports.

## What is actually crashing

Logos on Mac is **not** a VM wrapper. It is a native ARM64 desktop app:

- Stub: `/Applications/Logos.app/Contents/MacOS/Logos`
- Host: `FaithlifeDesktop.framework` → `MonoHost` launching **.NET CoreCLR** (`libcoreclr.dylib`)
- HTML / login / resource UI: **Chromium Embedded Framework** (`org.cef.framework`, `LogosCEF` GPU + renderer processes)
- Layout / library: Sinai\* + SQLite under `~/Library/Application Support/Logos4/`

Two installers exist because Intel and Apple Silicon are different CPUs:

- `LogosMac.dmg` → Intel (`x86_64`)
- `LogosMac-arm.dmg` → Apple Silicon (`arm64`)

Crash reports say `Code Type: ARM-64 (Native)`. Rosetta would say **Translated**. The M-series DMG does **not** virtualize the Intel app.

An Intel QEMU macOS VM can install the Intel DMG and test **login** (CEF). That will **not** reproduce Martin’s crash (ARM + SystemConfiguration + CalDigit/wake). Dumps start with `Has valid credentials = True`; he is already signed in.

## Crash signature (13, 15, 19 Aug)

Repeated native abort:

- `NativeSignalException: SIGSEGV`
- Thread on dispatch queue `*/client sessions`
- `SystemConfiguration` `addSessionReference`
- `KERN_INVALID_ADDRESS at 0x01004008910043f8`
- Then Logos’s own handler `-[OurApp ReportUnhandledNativeException:]` → `abort()`

Logos support’s working theory (Tommy, 17 Aug): **network path change** (Ethernet ↔ Wi-Fi / dock), not merely sleep/wake. Workaround they gave: **quit Logos before undocking**.

That is necessary but not sufficient: the 15 Aug crash was on **Wi-Fi**, and the 19 Aug crash was at the **desk on Ethernet** ~6 hours after wake, with Logos left running overnight.

## 18 Aug freeze (different symptom)

Hang, not SIGSEGV. About **2 minutes after wake**, UI unresponsive ~47s. Heaviest stack: **Close All** on `CrBrowserMain` blocked in `.NET Monitor.Wait` / `psynch_cvwait`. Background logs (layout + sync) kept writing. Process alive, window stuck.

## Dump index

Incoming packages are `LogosLogs.mjwebster.<timestamp>.zip` plus optional translated crash/hang `.docx`. Unzip under `extracted/<dump-id>/`.

| Dump | What Martin reported | What the files show |
|---|---|---|
| `20260731-062249` / `062619` | Early crashes | Logos 52.1, macOS 26.5.2, ARM64 |
| `20260810-163402` | After update | Logos 52.2.0.0019, macOS 26.6.1 |
| `20260813-145947` | Crash after leaving desk | SIGSEGV `addSessionReference`; Wi-Fi in later analysis |
| `20260813-165405` | Crash almost immediately after quitting, on Wi-Fi | Same app version; no SIGSEGV in that `Logos.log` tail |
| `20260815-194900` | Wi-Fi only, Notes in Logos, Apple Notes + Safari open | Same SIGSEGV, ~44 min after wake |
| `20260818-055712` | Froze after a few minutes | **Hang** after wake; Close All / Monitor.Wait |
| `20260819-171802` | Desk, Ethernet, Word open, ~6 h plugged | Same SIGSEGV as 13/15 Aug; macOS 26.6.2; launched overnight |

## Layout

```
LogosLogs.mjwebster.*.zip     original packages sent to Logos
*Translated Report*.docx      macOS translated crash / hang reports
crashphoto*.jpeg              screenshots
extracted/<id>/               unpacked working copies (logs; maps/PBB omitted from git)
scripts/logos_network_watch.py  macOS helper: log Ethernet vs Wi-Fi path changes
docs/FINDINGS.md              longer notes from 19 Aug 2026 review
```

## Support thread

- Last Logos engineering update: 17 Aug 2026 (Tommy passed logs to development as network handoff).
- Martin CC’d Luke on 18 Aug freeze + 19 Aug crash packages.
- Draft follow-up to Tommy is in Gmail Drafts (not sent from this repo). Stay on case **01275856**.
