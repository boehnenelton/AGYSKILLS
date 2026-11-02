---
name: env-migration-automator
description: >-
  Automate the deprecation migration from legacy paths.json ($PATHS_FILE) to
  canonical definitions.json ($DEFINITIONS_FILE) across repositories, scripts,
  and configurations per Policy §4.5. Scans codebase files for references to
  paths.json, updates sourcing preambles to definitions.json, injects mandatory
  Type classifications (Type: 'Path'), and verifies backward compatibility with
  dry-run backups. Use when migrating legacy scripts to definitions.json, retiring
  deprecated paths.json references before the 2027 sunset deadline, or updating
  environment preambles. Do NOT use for auditing hardcoded paths or verifying
  pointer resolution (use env-pointer-validator), routine CRUD on definitions.json
  (use env-definitions-manager), 104-to-105 data table upgrades (use
  bejson-105-upgrade-automator), or MFDB database upgrades (use
  mfdb-105-upgrade-coordinator).
---

# Skill: `env-migration-automator` (Layer 3 Environment Store Deprecation Migration Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 3 (Infrastructure Automation & Staging Engines)`
- **Policy Anchor**: `Policy §4.5 (Environment Sourcing Standards), Announcement October 23, 2026`
- **Embedded Tool**: [`scripts/env_migration_tool.py`](./scripts/env_migration_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

Under Policy §4.5 and the October 23, 2026 directive:
> *"`paths.json` (`$PATHS_FILE`) is deprecated in favor of `definitions.json` (`$DEFINITIONS_FILE`). `paths.json` remains functional until 2027, but immediate transition to `definitions.json` is required. The `Type` field in `definitions.json` explicitly categorizes variable types (e.g. 'Path')."*

`env-migration-automator` scans repositories, scripts (Python, Bash), and configuration stores to locate references to `paths.json` and automatically transforms them to `definitions.json` with verbatim backup safety (`<filename>.bak`) and dry-run validation.

---

## 2. Four-Stage Deprecation Migration Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Scan Target  | --> | Stage 2: Dry-Run Diff |
| For paths.json Tokens |     | Generation            |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Verify Syntax| <-- | Stage 3: Atomic Edit &|
| & Sourcing Execution  |     | Verbatim Backup (.bak)|
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Scan)**: Finds all files referencing `paths.json` or `$PATHS_FILE`.
2. **Stage 2 (Dry-Run)**: Displays side-by-side unified diffs of proposed changes without touching files.
3. **Stage 3 (Atomic Transformation)**: Preserves original file as `.bak` and replaces sourcing calls with `definitions.json`.
4. **Stage 4 (Verification)**: Runs Python/Bash syntax checks to ensure execution integrity.

---

## 3. Standard Migration Transformations

### Python Preamble Migration:
```python
# Legacy
with open("/storage/emulated/0/.env/user/paths.json", "r") as f:
    paths = json.load(f)

# Migrated (Canonical Policy §4.5)
with open("/storage/emulated/0/.env/user/definitions.json", "r") as f:
    definitions = json.load(f)
```

### Bash Sourcing Migration:
```bash
# Legacy
PATHS_FILE="/storage/emulated/0/.env/user/paths.json"

# Migrated
DEFINITIONS_FILE="/storage/emulated/0/.env/user/definitions.json"
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to run environment deprecation migrations, always mandate `--sandbox` containment and deterministic exit codes (`0` = Clean Migration, `10` = Path Failure, `20` = Env Failure, `30` = Migration Error):

```bash
python3 scripts/env_migration_tool.py --target "." --dry-run
python3 scripts/env_migration_tool.py --target "." --apply
```

---

## When NOT to Use

Do NOT use `env-migration-automator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing hardcoded paths and verifying ENV: pointer resolution**: Redirect immediately to `env-pointer-validator`.
- **Querying and updating variables inside definitions.json**: Redirect immediately to `env-definitions-manager`.
- **Upgrading BEJSON 104 data tables to 105 UUID tables**: Redirect immediately to `bejson-105-upgrade-automator`.
- **Coordinating multi-file MFDB v1.31 to v1.40 upgrades**: Redirect immediately to `mfdb-105-upgrade-coordinator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
