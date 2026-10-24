---
name: prompt-placeholder-composer
description: >-
  Compose deterministic {{VAR:-default}} placeholder slot schemas for BEJSON 104 and 105 file templates, owning writer skeletons, and agy_presets.104a.bejson prompt registries, guaranteeing zero unresolved tokens or forbidden TODO/TBD markers prior to Layer 4 template binding. Use when parameterizing reusable templates or prompt presets for 104 or 105 workflows. Do NOT use for binding 104 dialect schemas (use template-104-template), binding 105 UUID-fingerprinted schemas (use template-105-template), or defining entity relational graphs (use component-taxonomy-architect).
---

# Skill: `prompt-placeholder-composer` (Layer 5)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5`
- **Era & Library Binding**: `Cross-Era Slot Parameterization ({{VAR:-default}})`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries`
- **Target Formats**: `{{VAR:-default}} Slot Schema + agy_presets.104a.bejson`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `17d0e2bd-d4bb-5c9f-a330-4008466fc222`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`prompt-placeholder-composer` operates at **Layer 5** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Template Slot Compiler ({{SLOT_NAME:-default_value}})`

---

## 2. Core Structural & Policy Invariants

1. Every placeholder slot must follow {{UPPER_SNAKE_NAME:-deterministic_default}}.
2. Zero tolerance for unparameterized filler markers ('TODO', 'TBD', 'FIXME', '...').
3. Separates 104 slot sets from 105 UUID-injected slot sets ({{FIELD_UUID_*}}, {{RECORD_UUID_*}}).

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

When invoking subagents or CLI verification tools from `prompt-placeholder-composer`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute prompt-placeholder-composer verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `prompt-placeholder-composer` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Binding slots to Foundational Era 104/104a/104db files**: Redirect immediately to `template-104-template`.
- **Binding slots to Integrity Era 105/105a/105db files**: Redirect immediately to `template-105-template`.
- **Designing entity PK/FK relational graphs and Write-Owners**: Redirect immediately to `component-taxonomy-architect`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
