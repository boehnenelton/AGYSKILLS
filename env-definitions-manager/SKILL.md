---
name: env-definitions-manager
description: >-
  Manage, query, insert, and update canonical environment definitions in
  definitions.json ($DEFINITIONS_FILE) with schema validation and type classification
  (Type: 'Path'). Provides CLI operations to safely add new directory pointers,
  inspect registered environment variables, and project definitions to shell/python
  stores per Policy §4.5. Use when adding new directory paths to definitions.json,
  querying ecosystem environment variables, updating canonical paths, or inspecting
  environment store integrity. Do NOT use for scanning hardcoded paths or verifying
  pointer resolution in code (use env-pointer-validator), migrating legacy paths.json
  scripts (use env-migration-automator), managing secure API keys (use
  policy-secrets-leak-auditor), or mapping conceptual terminology (use
  definitions-cartographer).
---

# Skill: `env-definitions-manager` (Layer 3 Canonical Definitions Store Manager)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 3 (Infrastructure Automation & Staging Engines)`
- **Policy Anchor**: `Policy §4.5 (Environment Sourcing Standards), Announcement October 23, 2026`
- **Embedded Tool**: [`scripts/env_definitions_tool.py`](./scripts/env_definitions_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

Under the **October 23, 2026 Standards Update**, `paths.json` is deprecated in favor of `definitions.json` (`/storage/emulated/0/.env/user/definitions.json`). In `definitions.json`, variables explicitly declare their `Type` (e.g. `"Path"` for directories and files).

`env-definitions-manager` is the operational CLI tool for:
1. **Querying**: Look up definitions by key, substring, or Type.
2. **Inserting**: Safely adding new paths and configuration variables with schema validation and atomic file replacement.
3. **Integrity Verification**: Ensuring that any declared `Type: "Path"` entry points to a real physical directory or file before committing.

---

## 2. Four-Stage Definition Management Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Load         | --> | Stage 2: Validate     |
| definitions.json      |     | Key & Type Constraints|
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Atomic POSIX | <-- | Stage 3: Verify       |
| Replacement & Backup  |     | Physical Path On Disk |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Load & Map)**: Ingests `definitions.json` with O(1) field map caching.
2. **Stage 2 (Validation)**: Validates variable name syntax and mandatory `Type` classification.
3. **Stage 3 (Path Verification)**: If `Type="Path"`, verifies target directory existence.
4. **Stage 4 (Atomic Commit)**: Writes atomically via temporary file with automatic timestamped backup.

---

## 3. CLI Command Workflows

```bash
# Query a variable
python3 scripts/env_definitions_tool.py get GLOBAL_LOGS

# List all Path variables
python3 scripts/env_definitions_tool.py list --type Path

# Safely set or update a definition
python3 scripts/env_definitions_tool.py set NEW_TOOL_DIR "/storage/emulated/0/Admin/Tools/NewTool" --type Path --desc "Directory for new tool"
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to modify definitions, always mandate `--sandbox` containment and deterministic exit codes (`0` = Success, `10` = Path Failure, `20` = Env Failure, `30` = Mutation Rejected):

```bash
python3 scripts/env_definitions_tool.py list --json
```

---

## When NOT to Use

Do NOT use `env-definitions-manager` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing code for hardcoded paths and verifying ENV: pointers**: Redirect immediately to `env-pointer-validator`.
- **Migrating scripts from legacy paths.json to definitions.json**: Redirect immediately to `env-migration-automator`.
- **Auditing unmasked credentials and API keys in code**: Redirect immediately to `policy-secrets-leak-auditor`.
- **Resolving system terminology and concept definitions**: Redirect immediately to `definitions-cartographer`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
