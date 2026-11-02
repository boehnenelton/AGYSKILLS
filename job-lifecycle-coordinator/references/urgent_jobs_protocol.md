# Reference: Policy Urgent Jobs Protocol & Archival Routing

- **Version**: 100
- **Policy Anchor**: Policy § URGENT JOBS, Policy §2.3
- **Author**: Elton Boehnen

---

## 1. Directory Environment Mapping

Job management relies strictly on canonical environment paths:

- **`$JOBS_FOLDER`**: `/storage/emulated/0/Admin/System/Job_Management/Jobs`
- **`$COMPLETED_JOBS_FOLDER`**: `/storage/emulated/0/Admin/System/Job_Management/Completed_Jobs`
- **`$JOB_LOGS_FOLDER`**: `/storage/emulated/0/Admin/System/Job_Management/Logs`
- **`$GLOBAL_LOGS`**: `/storage/emulated/0/Admin/System/Global_Logs`

---

## 2. Policy Invariants for Urgent Jobs

1. **Top Priority**: Urgent jobs must be checked before addressing general user requests.
2. **Atomic Move**: Never leave completed jobs in `$JOBS_FOLDER`; move atomically to `$COMPLETED_JOBS_FOLDER`.
3. **Double Logging**:
   - Write Markdown summary to `$JOB_LOGS_FOLDER/daily_log-<timestamp>.md`.
   - Commit structured BEJSON record to `$GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson` via `$LOGGING_TOOL write`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
