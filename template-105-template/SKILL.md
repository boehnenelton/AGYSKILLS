---
name: template-105-template
description: >-
  Generate zero-filler Integrity Era BEJSON 105, 105a, and 105db data files, UUID-fingerprinted taxonomy registries, and Policy §10.4 owning writer modules backed by $ADMIN_LIBRARIES_105 using parameterized {{VAR:-default}} templates, pre-compiled UUIDv4 field_uuid definitions, reserved record_uuid row offsets (+1 for 105/105a, +2 for 105db), and self-maintaining by_name_row field_map lookups. Use when scaffolding new Format 105, 105a, or 105db stores and 105 owning writers. Do NOT use for Foundational Era 104, 104a, or 104db templates without field_uuid and record_uuid (use template-104-template), generating bare-bones zero-filler template skeletons across arbitrary non-BEJSON formats (use template-literal-skeleton), migrating existing 104 files to 105 (use bejson-105-upgrade-automator), or executing runtime CRUD on existing 105 files (use bejson-105-core).
---

# Skill: `template-105-template` (Layer 4)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 4`
- **Era & Library Binding**: `105 (Integrity Era Templating - libraries_105, Release 301 / v3.5.3)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_105`
- **Target Formats**: `105, 105a, 105db Templates + Python/JS/TS/Bash Owning Writers (libraries_105)`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `f6505ab8-480b-5441-ada1-99672fa61654`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`template-105-template` operates at **Layer 4** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `assets/template_entity_105.bejson.tpl`
- `assets/template_config_105a.bejson.tpl`
- `assets/template_owning_writer_105.py.tpl`

---

## 2. Core Structural & Policy Invariants

1. Mints a unique UUIDv4 field_uuid for every field in Fields and uses bejson_core_define_field().
2. Pre-configures Values rows with record_uuid at index 0 (105/105a) or index 1 after Record_Type_Parent (105db).
3. Scaffolds owning writers that resolve row indices via libraries_105 self-maintaining by_name_row field_map cache.

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

When invoking subagents or CLI verification tools from `template-105-template`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute template-105-template verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `template-105-template` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Scaffolding Foundational Era 104, 104a, or 104db files and _FieldMap writers**: Redirect immediately to `template-104-template`.
- **Upgrading existing 104/104a/104db files to 105/105a/105db**: Redirect immediately to `bejson-105-upgrade-automator`.
- **Executing runtime CRUD on existing 105 files**: Redirect immediately to `bejson-105-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
