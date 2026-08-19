# Findings (19 Aug 2026)

Review of Gmail from Martin Webster and Logos Technical Support, plus the 18 Aug freeze and 19 Aug crash packages.

## Emails

**Tommy Ball (tech@logos.com), last note 17 Aug 2026** (forwarded by Martin):

- Logs + context passed to development.
- Working theory: network handoff, not merely sleep/wake.
- Workaround: quit Logos before disconnecting the Thunderbolt dock, lid down, move, then restart Logos.

No Logos reply after that as of 19 Aug evening.

**Martin, 18 Aug 06:01** — `Crashes & Freezing` to tech@logos.com, CC Luke. “After starting Logos and using it for a few minutes I froze.” Attached `LogosLogs.mjwebster.20260818-055712.zip` and `Freezing 2026 08 18 at 05-56.docx`. Body also pasted Luke’s earlier Tommy draft (CalDigit TS5, Saturday Wi-Fi crash, stay on 01275856).

**Martin, 19 Aug 17:24** — `Crash` to tech@logos.com, CC Luke. Mac plugged ~6 hours, little use. Unsure if Logos was quit after Wi-Fi before docking. Word open. Ethernet connected, not actively using the internet. Attached `LogosLogs.mjwebster.20260819-171802.zip` and `2026 08 19 Crash at 1720.docx`.

**Logos Customer Service → Luke, 19 Aug** — Google and Apple accounts linked to **Luke Morrison’s** Logos account (VM/account setup, not a support reply).

## 19 Aug crash

From the translated report + `Logos.log`:

- Process Logos [1639], version 52.2.0.0019
- `Code Type: ARM-64 (Native)`
- Hardware Model **Mac17,8**
- Launch: 18 Aug 20:01:47; crash 19 Aug 17:17:52
- Time since wake: 21399 s (~6 h)
- Triggered by thread 106, queue `*/client sessions`
- `EXC_BAD_ACCESS (SIGABRT)` / `KERN_INVALID_ADDRESS 0x01004008910043f8`
- `abort()` after Logos native exception handler
- Stack: `SystemConfiguration addSessionReference` ← CFSet apply ← `__add_state_handler_block_invoke` ← os_state / libdispatch
- Main thread name: `CrBrowserMain`
- Related threads present: many CEF `NetworkConfigWatcher`, `NetworkNotificationThreadMac`, `.NET Network Address Change`
- Binary images include CEF, CoreCLR, MonoHost, Sinai\*, LogosWebBrowser, AGXMetalG17X

`Logos.log` line 2: `Starting application (52.2, version 52.2.0.0019) on Mac OS X 26.6.2 (Arm64 running on Apple Silicon)`. Sync still ran at 17:17:48; SIGSEGV at 17:17:52.

This is the same abort as 13 Aug 14:59 and 15 Aug 19:48.

## 18 Aug hang

Spindown (not a crash report):

- Event: hang; unresponsive 47 s before sampling; duration 49.95 s
- Time since wake: **119 s**
- PID 96105, started 05:28:36, hang ~05:54:49 (~26 min of use)
- macOS 26.6.1 (he updated to 26.6.2 before the 19 Aug crash)
- Architecture arm64; system also has a Rosetta shared cache, but Logos itself is arm64
- Heaviest stack: mouse-down → `-[MainToolbarControllerBase closeAllButtonClicked:]` → .NET `Monitor_Wait` → `psynch_cvwait` on `CrBrowserMain`
- Footprint ~1.5 GB; 94 threads; LogosCEF GPU + renderer processes donating importance
- `Logos.log` has **no** SIGSEGV; panel/sync lines continue through 05:55:00

So: UI thread blocked on a lock after Close All, shortly after wake. Different failure, same wake window.

## Intel vs ARM DMGs / QEMU

Do **not** treat the M-series DMG as a virtualization wrapper. Confirm on disk if needed:

```bash
file LogosMac.dmg LogosMac-arm.dmg
# after mount:
file /Volumes/Logos/Logos.app/Contents/MacOS/Logos
lipo -info /Volumes/Logos/Logos.app/Contents/MacOS/Logos
```

Expect `x86_64` vs `arm64`. Intel DMG on an Intel QEMU Mac is the correct installer for that VM and the wrong machine for Martin’s crash.

## Questions for Logos development (case 01275856)

1. What holds a SystemConfiguration session so `addSessionReference` runs on `*/client sessions` after wake or interface change?
2. Do CEF (`NetworkConfigWatcher` / `NetworkNotificationThreadMac`) and .NET (`Network Address Change`) both subscribe, and can they race?
3. Why the same bad pointer `0x01004008910043f8` on 13, 15, and 19 Aug?
4. Is Close All hanging on `Monitor.Wait` on the UI thread after wake the same bug or a second one?
5. Any known issue on macOS 26.6 + Mac17,8 / M5 with this CEF build?

A Gmail draft with this ask is in Luke’s Drafts, threaded on case 01275856, unsent.
