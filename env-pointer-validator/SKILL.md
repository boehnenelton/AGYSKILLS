---
name: env-pointer-validator
description: >-
  Audit scripts, BEJSON configurations, and application templates for strict
  adherence to Policy §4.5 pointer-only environment standards. Verifies that
  runtime configurations reference abstract pointers (ENV:<var_name>) rather than
  hardcoded paths or raw credentials, and validates pointer resolution against
  definitions.json. Use when auditing codebases for hardcoded filesystem paths,
  validating environmental pointer references before deployment, or checking
  definitions.json key resolution. Do NOT use for querying and editing
  definitions.json records (use env-definitions-manager), migrating scripts from
  legacy paths.json (use env-migration-automator), scanning raw API key leaks
  (use policy-secrets-leak-auditor), or resolving speech-to-text terminology
  aliases (use definitions-cartographer).
---

# Skill: `env-pointer-validator` (Layer 2 Policy §4.5 Pointer & Resolution Gate)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Validation & Diagnostic Engine)`
- **Policy Anchor**: `Policy §4.5 (Environment Sourcing Standards)`
- **Embedded Tool**: [`scripts/env_pointer_tool.py`](./scripts/env_pointer_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

Policy §4.5 establishes a cardinal rule: **Never hardcode environment paths in runtime logic**. Instead, applications must source configurations from abstract pointers formatted as `ENV:<var_name>`, resolving dynamically against `/storage/emulated/0/.env/user/definitions.json`.

`env-pointer-validator` audits codebases, configuration files (`config/*.json`), and BEJSON manifests to detect:
1. **Hardcoded Path Breaches**: Flagging raw `/storage/emulated/0/...` strings inside application logic.
2. **Broken Pointers**: Verifying that every `ENV:<var_name>` token maps to a registered variable in `definitions.json`.
3. **Type Mismatches**: Ensuring path variables match `Type: "Path"` declarations.

---

## 2. Three-Stage Pointer Validation Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Ingest       | --> | Stage 2: Audit For    |
| Canonical Definitions |     | Hardcoded Paths       |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Synthesize   | <-- | Stage 3: Resolve      |
| Pointer Audit Report  |     | Abstract ENV Pointers |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Definitions Ingestion)**: Ingests `definitions.json` into an O(1) field-mapped lookup dictionary.
2. **Stage 2 (Hardcode Sweep)**: Scans source code and configs for prohibited hardcoded paths.
3. **Stage 3 (Resolution Test)**: Validates that each declared `ENV:<token>` exists in `definitions.json`.
4. **Stage 4 (Report)**: Emits a validation report to `reports/audits/env_pointer_audit_${TIMESTAMP}.md`.

---

## 3. Standard Pointer Report Schema

```markdown
# Environment Pointer Validation Report

- **Target System**: `/path/to/project`
- **Validation Timestamp**: `2026-11-02T01:30:00Z`
- **Validation Status**: `POINTERS_VERIFIED` (0 hardcoded paths, 6 pointers resolved)

## Verified Pointers
- `ENV:ADMIN_LIBRARIES` -> `/storage/emulated/0/Admin/Libraries` [OK]
- `ENV:PROJECT_TYPE_LEDGER` -> `/storage/emulated/0/Admin/System/project_type_ledger.104a.bejson` [OK]
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to validate environment pointers, always mandate `--sandbox` containment and deterministic exit codes (`0` = Fully Valid, `10` = Path Failure, `20` = Env Failure, `30` = Unresolved Pointers or Hardcoded Paths):

```bash
python3 scripts/env_pointer_tool.py --target "." --report
```

---

## When NOT to Use

Do NOT use `env-pointer-validator` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Querying, inserting, or modifying definitions.json records**: Redirect immediately to `env-definitions-manager`.
- **Migrating scripts from legacy paths.json to definitions.json**: Redirect immediately to `env-migration-automator`.
- **Scanning code and transcripts for unmasked API credentials**: Redirect immediately to `policy-secrets-leak-auditor`.
- **Resolving system terminology and speech-to-text aliases**: Redirect immediately to `definitions-cartographer`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
