---
name: code-taxonomy-architect
description: >-
  Design and standardize BEJSON entity field prefixes, snake_case column identifiers, UTC ISO-8601 <entity>_created_at timestamp conventions, and lib_bejson_<Family>_<submodule> heritage module and function signatures across Python, JavaScript, TypeScript, and Bash per Policy §6.1 and §10.2. Use when defining field names, variable identifiers, or library module signatures for 104 or 105 projects prior to template rendering. Do NOT use for assigning primary/foreign keys and Write-Owner modules (use component-taxonomy-architect), rendering 104 or 105 file templates (use template-104-template or template-105-template), or auditing existing code ASTs (use policy-bejson-auditor).
---

# Skill: `code-taxonomy-architect` (Layer 5)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5`
- **Era & Library Binding**: `Cross-Era Naming & Symbol Standardization (Policy §6.1 & §10.2)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries`
- **Target Formats**: `Naming & Symbol Taxonomy Specification (104 & 105)`
- **Reference Specification**: `references/self_describing_variable_spec.md`
- **Auditing Tool**: `scripts/verify_variable_naming.py`
- **Date Created**: `2026-10-17`
- **RELATIONAL_ID**: `c0c2d34f-b96e-5855-9946-6188e6cd3edd`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`code-taxonomy-architect` operates at **Layer 5** of the 6-Tier Layered Skill Architecture. It enforces strict separation between **Foundational Era (`libraries_104`)** and **Integrity Era (`libraries_105`)** operations as well as intra-era format variants (`104` vs. `104a` vs. `104db` and `105` vs. `105a` vs. `105db`).

### Bound Canonical Modules
- `Policy §6.1 Heritage Naming Standard (lib_bejson_<Family>_*)`
- `Policy §6.1 Long Self-Describing Variable Standard (Hierarchy-Group-Purpose Triad)`
- `Policy §10.2 Field Naming Standard (<prefix>_<field_name>)`

---

## 2. Core Structural & Policy Invariants

1. **Entity Prefix Unity**: Every entity uses exactly one snake_case prefix for all its fields (never mix prefixed and unprefixed fields).
2. **Standard Timestamps**: Timestamps follow `<entity_prefix>_created_at` in UTC ISO-8601 format.
3. **Library Family Heritage**: New library functions follow family heritage naming (e.g., `lib_bejson_Core_*`, `lib_bejson_CMS_*`).
4. **Long Self-Describing Variable Standard (HGP Triad)**: All variable identifiers in new code, templates, and scripts must follow the formula:
   $$\text{Identifier} = \langle\text{Hierarchy/Scope}\rangle\_\langle\text{Group/Domain}\rangle\_\langle\text{Purpose/Role}\rangle$$
   *Signals where it lives (Hierarchy), which subsystem it belongs to (Group), and what it does (Purpose).*
   - **Prohibited Cryptic Identifiers**: Single-letter variables (`d`, `val`, `res`, `tmp`, `arr`, `obj`, `item`, `data`) are strictly forbidden in application logic and templates.
   - **Auditor**: Enforced via [`scripts/verify_variable_naming.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/code-taxonomy-architect/scripts/verify_variable_naming.py).

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

When invoking subagents or CLI verification tools from `code-taxonomy-architect`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute code-taxonomy-architect verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `code-taxonomy-architect` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Assigning UUID primary keys, _fk foreign keys, and Write-Owner modules**: Redirect immediately to `component-taxonomy-architect`.
- **Rendering 104 or 105 BEJSON templates and owning writers**: Redirect immediately to `template-104-template`.
- **Auditing existing code ASTs for Policy §6.2 and §10.1 compliance**: Redirect immediately to `policy-bejson-auditor`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
