---
name: planning-schema-planner
description: >-
  Execute Turn 1 schema and Era allocation planning to partition project data artifacts cleanly between Foundational Era libraries_104 (104, 104a, 104db, Nested 104, MFDB v1.31/v1.32) and Integrity Era libraries_105 (105, 105a, 105db, MFDB v1.40) before Turn 2 code or template generation. Use when planning new BEJSON databases, deciding between 104, 104a, 104db, and 105 variants, or scheduling 104-to-105 migrations. Do NOT use for executing multi-skill runtime DAGs (use skill-chain-coordinator), rendering 104 templates (use template-104-template), rendering 105 templates (use template-105-template), or running atomic 104-to-105 upgrades (use bejson-105-upgrade-automator).
---

# Skill: `planning-schema-planner` (Layer 5)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5`
- **Era & Library Binding**: `Cross-Era Turn-Gated Architecture Planner (104 vs. 105)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries`
- **Target Formats**: `Turn-Gated Schema & Era Allocation Blueprint`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `f68d5e10-0cd3-5b96-bda2-c82a624fa081`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`planning-schema-planner` operates at **Layer 5** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Policy Announcement (Aug 15, 2026): libraries_104 Default vs. libraries_105 Explicit Opt-In`
- `Policy §10 Data Schema & Integrity Mandate`

---

## 2. Core Structural & Policy Invariants

1. Defaults all standard production configs (config/config.json) and project trackers (.bejson_project.json) to 104a in libraries_104.
2. Assigns 104 for single-entity tables with array/object fields, 104a for primitive-only metadata/configs, and 104db for multi-entity single-file tables.
3. Assigns 105/105a/105db when strict field_uuid/record_uuid fingerprinting or MFDB v1.40 FK cascade verification is required.

### Mandatory Field Map Cache & Boundary Sanitization Pattern
All record reads and writes must strip boundary whitespace (Policy §10.9) and resolve column indices through a dynamic `field_map` (Policy §6.2):

```python
def bejson_read_column(doc: dict, field_map: dict[str, int], row: list, col_name: str):
    clean_col = col_name.strip()
    col_idx = field_map[clean_col]
    val = row[col_idx]
    return val.strip() if isinstance(val, str) else val
```

---

## 3. Execution & Subagent Containment Contract (Level 3 Guardrail)

When invoking subagents or CLI verification tools from `planning-schema-planner`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute planning-schema-planner verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `planning-schema-planner` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Executing runtime multi-skill DAG workflows**: Redirect immediately to `skill-chain-coordinator`.
- **Scaffolding 104/104a/104db files from a frozen plan**: Redirect immediately to `template-104-template`.
- **Scaffolding 105/105a/105db files from a frozen plan**: Redirect immediately to `template-105-template`.
- **Executing atomic 104-to-105 file upgrades**: Redirect immediately to `bejson-105-upgrade-automator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
