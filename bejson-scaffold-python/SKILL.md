---
name: bejson-scaffold-python
description: >-
  Scaffold new standalone Python scripts/tools for Elton Boehnen's BEJSON/MFDB ecosystem using bundled starter templates that embed the BEJSON Core error registry, primitives, and validator self-contained. Use when asking to create, scaffold, or start a new Python script, tool, CLI, or Component app that touches BEJSON documents. Do NOT use for JavaScript (use bejson-scaffold-javascript), Bash (use bejson-scaffold-bash), or codebase refactoring (use bejson-codebase-refactor).
---
# BEJSON Python Script Templates

Two ready-to-run, single-file Python starter templates live in `assets/`. Both
are self-contained (stdlib only, no external `lib_bejson_*` imports) and
**inert by default**  -  every function/class is defined and exported but
nothing is called automatically. Running either file with `python3 file.py`
just prints an About banner.

## Templates

| File | Contains | Use when the script needs to... |
|---|---|---|
| `assets/BEJSON_Template_PY_Validator-v1.py` | Error registry (codes 1-16) + `validate_bejson()` / `bejson_validator_validate_file()` / `bejson_validator_get_report()` | only check/validate BEJSON documents, not read or mutate them |
| `assets/BEJSON_Template_PY_Full-v1.py` | Same, plus BEJSON Core (`bejson_core_load_file`, `bejson_core_atomic_write`, field-map cache `bejson_core_get_field_map`/`bejson_core_get_field_index`, `bejson_core_create_104/104a/104db`, record CRUD, filter/sort) | needs to load, create, mutate, or atomically write BEJSON documents, in addition to validating them |

Default to **Full** unless the user is explicitly asking for a pure validator
utility  -  most real scripts end up needing at least `bejson_core_load_file`
or the field-map cache.

## Workflow

1. Copy the matching template from `assets/` to the new script's path.
2. Update the header docstring: `Name`, `Description`, `Date Created` (today),
   and generate a **new** `RELATIONAL_ID` (fresh UUID  -  never reuse the
   template's). Keep the Author/Contact/Format_Creator lines unchanged
   (Section 9.2 crediting is mandatory on every deliverable).
3. Bump `VERSION = 1` only if this is a re-delivery of an existing project
   file, per Package_Version rules (Section 3.3)  -  a first delivery starts
   at 1 / Package_Version 100.
4. Build the actual script logic *below* the embedded library code (or in a
   new module that imports this file) and call into `validate_bejson()`,
   `bejson_core_load_file()`, `bejson_core_get_field_map()`, etc. as needed  - 
   always via the field-map cache, never hardcoded positional indices
   (Section "BEJSON Core Mandate"  -  non-negotiable for all code dated after
   2026-08-14).
5. If the script is a root-level executable for a project, add the
   self-locating `SCRIPT_PATH` snippet (Policy 4.1) and the `config.json`
   bootstrap (Policy 4.4) on top  -  these are intentionally NOT baked into
   the template since not every script is a project root launcher.
6. Leave the `if __name__ == "__main__":` block as a thin entry point that
   only prints `about()` unless the user asks for real CLI behavior  -  don't
   wire the template into calling the validator/core against real data
   unless that's the actual point of the script being built.

## Error codes available

`E_INVALID_JSON`, `E_MISSING_MANDATORY_KEY`, `E_INVALID_FORMAT`,
`E_INVALID_VERSION`, `E_INVALID_RECORDS_TYPE`, `E_INVALID_FIELDS`,
`E_TYPE_MISMATCH`, `E_RECORD_LENGTH_MISMATCH`, `E_RESERVED_KEY_COLLISION`,
`E_INVALID_RECORD_TYPE_PARENT`, `E_FILE_NOT_FOUND`, `E_PERMISSION_DENIED`,
`E_ATOMIC_WRITE_FAILED`, `E_INVALID_FORMAT_CREATOR` (Full template adds
`E_CORE_*` 17-29: parse/serialization/index/field/backup/write/query/
encryption errors). Raise `BEJSONValidationError(message, code)` for any new
validation failure path so callers get a consistent code, not a bare string.

## Do not

- Don't reintroduce a `lib_bejson_Core_bejson_env` / `resolve_path` external
  import  -  the Full template already inlines a minimal `resolve_path()`
  stand-in so the file stays single-file portable.
- Don't alter the embedded Core/Validator function bodies themselves when
  scaffolding a new script (Section 7.3  -  Core family libraries are frozen);
  build new logic around them instead.
- Don't ship the template unmodified as the "finished" deliverable  -  the
  header placeholders (RELATIONAL_ID, date, description) must be filled in
  for the specific script being created.
