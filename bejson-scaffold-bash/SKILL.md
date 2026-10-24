---
name: bejson-scaffold-bash
description: >-
  Scaffold new standalone Bash scripts/tools for Elton Boehnen's BEJSON/MFDB ecosystem (Termux/Android-ready) using bundled starter templates embedding the BEJSON Core error registry, jq-backed primitives, and validator. Use when asking to create, scaffold, or start a new bash/shell script, Termux tool, or CLI touching BEJSON documents. Do NOT use for Python (use bejson-scaffold-python) or JavaScript (use bejson-scaffold-javascript).
---
# BEJSON Bash Script Templates

Two ready-to-run, single-file Bash starter templates live in `assets/`.
Both require `jq >= 1.6` (the validator/core functions shell out to it) and
are **inert by default**  -  every function is `export -f`'d but nothing is
called automatically. Running or `source`-ing either file just prints an
About banner (the About-only behavior is gated by
`[[ "${BASH_SOURCE[0]}" == "${0}" ]]`, so sourcing does NOT print the banner
and just makes the functions available).

## Templates

| File | Contains | Use when the script needs to... |
|---|---|---|
| `assets/BEJSON_Template_SH_Validator-v1.sh` | Error registry (codes 1-29) + `bejson_validator_check_dependencies` / `bejson_validator_validate_file` | only check/validate BEJSON documents, not read or mutate them |
| `assets/BEJSON_Template_SH_Full-v1.sh` | Same, plus BEJSON Core (`bejson_core_load_file`, `bejson_core_atomic_write` with automatic timestamped backup, `bejson_core_get_field_index`, record add/remove/update, filter/sort by field) and the resilient PID-aware mutex lock (`resilient_lock_acquire`/`resilient_lock_release`) | needs to load, create, mutate, or atomically write BEJSON documents, or needs locking around concurrent writes |

Default to **Full** unless the user explicitly wants a pure validation
utility (e.g. a pre-commit hook that just checks files are well-formed).

## Workflow

1. Copy the matching template from `assets/` to the new script's path.
2. Update the header comment block: `Name`, `Description`, `Date Created`
   (today), and generate a **new** `RELATIONAL_ID` (fresh UUID  -  never reuse
   the template's). Keep Author/Contact/Format_Creator lines unchanged
   (Section 9.2 crediting is mandatory).
3. `BEJSON_TEMPLATE_VERSION` starts at `1` / Package_Version 100 for a first
   delivery; bump on every subsequent change per Section 3.3.
4. Add the script's real logic below the embedded library sections, calling
   `bejson_validator_validate_file`, `bejson_core_load_file`,
   `bejson_core_get_field_index`, etc.  -  always resolve fields by name via
   `bejson_core_get_field_index` (jq-backed), never by hardcoded array
   position (BEJSON Core Mandate, non-negotiable for code dated after
   2026-08-14).
5. This template already includes the self-locating `SCRIPT_PATH` /
   `get_script_path()` block (Policy 4.2) at the top  -  reuse `$SCRIPT_PATH`
   for any relative lib/data paths instead of hardcoding.
6. Wrap concurrent read-modify-write sequences against the same file in
   `resilient_lock_acquire "$target_path"` / `resilient_lock_release` (Full
   template only)  -  do not write your own ad hoc lockfile scheme.
7. Leave the trailing `if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then ... fi`
   guard as the only auto-executing code unless the user asks for real CLI
   behavior when the script is run directly.

## Error codes available

Validator: `E_INVALID_JSON`(1) `E_MISSING_MANDATORY_KEY`(2)
`E_INVALID_FORMAT`(3) `E_INVALID_VERSION`(4) `E_INVALID_RECORDS_TYPE`(5)
`E_INVALID_FIELDS`(6) `E_INVALID_VALUES`(7) `E_TYPE_MISMATCH`(8)
`E_RECORD_LENGTH_MISMATCH`(9) `E_RESERVED_KEY_COLLISION`(10)
`E_INVALID_RECORD_TYPE_PARENT`(11) `E_NULL_VIOLATION`(12)
`E_FILE_NOT_FOUND`(13) `E_PERMISSION_DENIED`(14) `E_ATOMIC_WRITE_FAILED`(15)
`E_INVALID_FORMAT_CREATOR`(16). Core: `E_CORE_*`(20-29). MFDB ranges
(30-79) are also declared (guarded with `[[ -v ... ]] ||` so re-sourcing
never errors) but MFDB core/validator function bodies are NOT embedded in
either template  -  only the Core family. Say so if the user needs MFDB
functions and offer to pull those sections from
`bejson_core_compiled.sh` on request.

## Do not

- Don't alter the embedded Core/Validator function bodies when scaffolding
  (Section 7.3  -  Core family libraries are frozen); build new logic around
  them.
- Don't add `set -o nounset` inside the embedded sections  -  intentionally
  omitted upstream so sourcing this file never breaks a host script's shell
  options (see the SAFETY & ERROR HANDLING note in the Core section).
- Don't ship the template unmodified  -  header placeholders must be filled in
  for the specific script being created.
