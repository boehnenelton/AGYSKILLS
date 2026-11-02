# Reference: Policy §2.3 Global Standardized Logging Protocol

- **Version**: 100
- **Policy Anchor**: Policy §2.3, Announcement October 31, 2026
- **Author**: Elton Boehnen

---

## 1. Authoritative Log Sink Topology

Authoritative global logs are partitioned strictly under `$GLOBAL_LOGS/`:
- **Daily Sink**: `$GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson`
- **Secure Sink**: `$GLOBAL_LOGS_SECURE/Log-<YYYY-MM-DD>-secure.bejson`
- **Archives**: `$GLOBAL_LOGS_ARCHIVES/`

---

## 2. Mandatory Write Payload Schema

Every log entry must be written via `$LOGGING_TOOL write` with the following parameters:
- `-m "<message>"`: Concise task summary.
- `-l "<level>"`: Standard level (`INFO`, `WARN`, `ERROR`, `CRITICAL`).
- `-k "<key>"`: Subsystem action dot-path (`skills.audit`, `job.complete`, etc.).
- `-s "<subsystem>"`: Canonical subsystem name.
- `--category "<category>"`: Domain token (`SKILL_ECOSYSTEM`, `MIGRATION`, etc.).
- `--flag "<flag>"`: Architectural flag (`RELEASE_300`, `FOUNDATIONAL_104`, etc.).
- `--context '<json>'`: Context dictionary with `task`, `status`, and `files_modified`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
