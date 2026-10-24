---
name: template-104-template
description: >-
  Generate zero-filler Foundational Era BEJSON 104, 104a, and 104db data files, lib_<family>_taxonomy.py constant registries, and Policy §10.4 owning writer modules backed by $ADMIN_LIBRARIES_104 using parameterized {{VAR:-default}} templates, _FieldMap O(1) field_map lookups, and ResilientPIDLock atomic persistence. Use when scaffolding new Release 300 .104.bejson entity stores, .104a.bejson ScriptConfig/tracker files, .104db.bejson databases, or 104 owning writers. Do NOT use for Integrity Era Format 105, 105a, or 105db templates requiring field_uuid, record_uuid, and by_name_row offset-aware writers (use template-105-template), generating bare-bones zero-filler template skeletons across arbitrary non-BEJSON formats (use template-literal-skeleton), defining initial entity prefixes (use code-taxonomy-architect), or executing runtime CRUD on existing 104 files (use bejson-104-core).
---

# Skill: `template-104-template` (Layer 4)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4`
- **Era & Library Binding**: `104 (Foundational Era Templating - libraries_104, Release 300)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_104`
- **Target Formats**: `104, 104a, 104db Templates + Python/JS/TS/Bash Owning Writers (Release 300)`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `932c3c5e-2c21-5158-a769-7a6c26df5421`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`template-104-template` operates at **Layer 4** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `assets/template_entity_104.bejson.tpl`
- `assets/template_config_104a.bejson.tpl`
- `assets/template_owning_writer_104.py.tpl`

---

## 2. Core Structural & Policy Invariants

1. Binds exclusively to $ADMIN_LIBRARIES_104 (Release 300) and maps Values rows 1:1 to Fields via field_map.
2. Preserves 'GUID_PLACEHOLDER' for Project_GUID in .bejson_project.json (Policy §4.6 / §7.3).
3. Generates a fresh UUIDv4 RELATIONAL_ID header on every scaffolded file (§9).

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

When invoking subagents or CLI verification tools from `template-104-template`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute template-104-template verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `template-104-template` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Scaffolding Format 105, 105a, or 105db files and by_name_row writers**: Redirect immediately to `template-105-template`.
- **Designing initial entity field prefixes and snake_case taxonomy**: Redirect immediately to `code-taxonomy-architect`.
- **Executing runtime CRUD on existing 104/104a/104db files**: Redirect immediately to `bejson-104-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
