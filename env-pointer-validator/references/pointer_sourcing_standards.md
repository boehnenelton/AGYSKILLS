# Reference: Policy §4.5 Pointer-Only Sourcing Standards

- **Version**: 100
- **Policy Anchor**: Policy §4.5, Announcement October 23, 2026
- **Author**: Elton Boehnen

---

## 1. The Canonical Environment Store

- **User Definitions**: `/storage/emulated/0/.env/user/definitions.json` (Canonical Source of Truth)
- **Deprecation**: `paths.json` is deprecated in favor of `definitions.json`.
- **Type Field**: In `definitions.json`, variables explicitly declare `Type` (e.g. `"Path"`).

---

## 2. The Abstract Pointer Standard

- Prohibited: `LOG_PATH = "/storage/emulated/0/Admin/System/Global_Logs"`
- Compliant: `LOG_PATH = resolve_env_pointer("ENV:GLOBAL_LOGS")`

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
