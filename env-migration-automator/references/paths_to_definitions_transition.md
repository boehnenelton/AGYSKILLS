# Reference: Deprecation Transition from paths.json to definitions.json

- **Version**: 100
- **Policy Anchor**: Announcement October 23, 2026, Policy §4.5
- **Author**: Elton Boehnen

---

## 1. Sunset Timeline

- **October 23, 2026**: Announcement deprecating `paths.json` (`$PATHS_FILE`) in favor of `definitions.json` (`$DEFINITIONS_FILE`).
- **2026 - 2027**: Grace period where `paths.json` remains functional alongside `definitions.json`.
- **2027**: Hard sunset; `paths.json` will be retired entirely.

---

## 2. Invariant Differences

| Attribute | Legacy (`paths.json`) | Canonical (`definitions.json`) |
| :--- | :--- | :--- |
| **Format** | Flat JSON dictionary | BEJSON 104a tabular document |
| **Type Classification** | Absent | Mandatory (`Type: "Path"`) |
| **Description** | Optional / Absent | Mandatory field |
| **Preamble Variable** | `$PATHS_FILE` | `$DEFINITIONS_FILE` |

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
