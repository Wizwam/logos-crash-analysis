# Ready-to-send follow-up (case 01275856)

To: tech@logos.com
CC: martinjwebster@gmail.com
Subject: Re: Crash - 2026 08 15 at 19:50 Using WI-FI only & Using NOTES in Logos & Apple Notes was open & Safari was open to listen to a talk
Attachments: none

---

Hi Tommy,

One extra observation from tonight's .ips (already on this thread) and the 15 Aug / 19 Aug reports, in case it helps development.

The IPS lists SIGABRT / abort() called. That is Logos aborting after Mono catches the real fault: EXC_BAD_ACCESS (KERN_INVALID_ADDRESS) at 0x01004008910043f8. That exact address is in the 15 Aug, 19 Aug, and 20 Aug dumps.

The dying thread is SystemConfiguration's "*/client sessions" queue, not the UI thread. The stack is:

  os_state_request_for_self
    → addSessionReference
      → CFStringAppendFormat
        → objc_msgSend on a bad/unmapped object
          → SIGSEGV
            → our_sigsegv_signal_handler
              → ReportUnhandledNativeException
                → abort()

So a client session in that table is already corrupt; the crash happens later, when SystemConfiguration tries to describe it. Tonight that was about 4 hours after launch and about 5 hours after lid wake, on dock Ethernet (en7 / CalDigit TS5) with Wi-Fi also connected — not an immediate undock.

All three dumps also show exactly 23 Chromium NetworkConfigWatcher threads, plus .NET Network Address Change and NetworkNotificationThreadMac. Native ARM-64, not Rosetta.

No new files attached; you already have tonight's .ips, Logos.log, and LogosError.log. Happy to send anything else development wants.

Thank you,
Luke Morrison (with Martin Webster)
Case 01275856
