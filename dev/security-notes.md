# Security Notes
RELATIONAL_ID: e55a92c0-0eca-45e3-bda0-525e1b779018

Observations only; no behavior changed (surgical scope).
- `cli-ai-standardizer` references an `x-goog-api-key` header: confirm templates read keys from the secure env store, never inline.
- Several scripts use `print()` for output and absolute `/storage/emulated/0/...` defaults in SKILL.md examples; policy 2 targets application logic, so these were left as documented examples. Candidate follow-up job.
