# Reference: Dual-Path Secure Logging & Daily Partition Architecture

- **Version**: 100
- **Policy Anchor**: Announcement October 31, 2026, Policy §2.3
- **Author**: Elton Boehnen

---

## 1. Dual-Path Sink Mechanics

When a log entry touches API keys, tokens, or secure environment paths:
1. The full entry with raw context is written strictly to `$GLOBAL_LOGS_SECURE/Log-<YYYY-MM-DD>-secure.bejson`.
2. An automated masked placeholder entry is inserted into `$GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson` with message `"[redacted: secure entry]"`.
3. The public log maintains sequence integrity and timing telemetry without exposing sensitive credentials.

---

## 2. Retention Invariants

- Logs under `$GLOBAL_LOGS/` remain active for **30 calendar days**.
- After 30 days, files are moved to `$GLOBAL_LOGS_ARCHIVES/` with partition naming preserved.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
