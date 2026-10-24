---
name: component-taxonomy-architect
description: >-
  Architect canonical schema_registry.104a.bejson specifications defining immutable UUIDv4 primary keys, _fk foreign-key relationships with explicit on_delete behaviors (cascade, null, default, restrict), and single Write-Owner module assignments per entity across BEJSON 104 and 105 projects per Policy §10.1, §10.3, and §10.4. Use when modeling relational entity graphs and write-ownership boundaries before scaffolding. Do NOT use for field-level snake_case prefix naming (use code-taxonomy-architect), turn-gated Era selection between 104 and 105 (use planning-schema-planner), or rendering 104/105 templates (use template-104-template or template-105-template).
---

# Skill: `component-taxonomy-architect` (Layer 5)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5`
- **Era & Library Binding**: `Cross-Era Relational & Write-Owner Standardization (Policy §10.1, §10.3, §10.4)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries`
- **Target Formats**: `schema_registry.104a.bejson / MFDB Entity Graph`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `4a1d74be-c134-54a2-b674-22c8aea7e026`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`component-taxonomy-architect` operates at **Layer 5** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Policy §10.1 Schema Registry Standard`
- `Policy §10.3 Keys & Foreign Keys Standard`
- `Policy §10.4 Write Ownership Standard`

---

## 2. Core Structural & Policy Invariants

1. Exactly one immutable UUIDv4 primary key per entity.
2. All foreign keys reference parent UUID PKs, end in _fk, and declare on_delete (cascade | null | default | restrict).
3. Exactly one owning write module is assigned per entity; hand-rolled inserts outside the owning writer are forbidden.

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

When invoking subagents or CLI verification tools from `component-taxonomy-architect`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute component-taxonomy-architect verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `component-taxonomy-architect` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Standardizing snake_case field prefixes and function names**: Redirect immediately to `code-taxonomy-architect`.
- **Turn-gated Era selection between libraries_104 and libraries_105**: Redirect immediately to `planning-schema-planner`.
- **Rendering 104 or 105 templates from frozen schemas**: Redirect immediately to `template-104-template`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
