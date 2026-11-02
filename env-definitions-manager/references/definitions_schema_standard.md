# Reference: Canonical definitions.json Schema Standard

- **Version**: 100
- **Policy Anchor**: Announcement October 23, 2026, Policy §4.5
- **Author**: Elton Boehnen

---

## 1. Schema Structure

`definitions.json` adheres to BEJSON 104a tabular layout:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["EnvironmentDefinition"],
  "Fields": [
    {"name": "name", "type": "string"},
    {"name": "value", "type": "string"},
    {"name": "description", "type": "string"},
    {"name": "Type", "type": "string"}
  ],
  "Values": [
    ["GLOBAL_LOGS", "/storage/emulated/0/Admin/System/Global_Logs", "Authoritative daily logs sink", "Path"]
  ]
}
```

---

## 2. Standard Type Classifications

- `Path`: Filesystem path to directory or file.
- `String`: General text constant.
- `Config`: Configuration parameter token.
- `Port`: Network port number.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
