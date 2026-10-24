---
name: bejson-scaffold-javascript
description: >-
  Scaffold new standalone vanilla-JavaScript or Node.js files for Elton Boehnen's BEJSON/MFDB ecosystem using bundled starter templates embedding BEJSON Core error registry, primitives, Web Crypto AES-GCM record encryption, and validator. Use when asking to create, scaffold, or start a new plain JS file, browser script, or Node script touching BEJSON documents. Do NOT use for Python (use bejson-scaffold-python) or full HTML layouts (use behtml-layout-builder).
---
# BEJSON Vanilla-JS Script Templates

Two ready-to-run, single-file, dependency-free JS starter templates live in
`assets/`. Both are UMD-style: usable via a plain `<script>` tag in a
browser (functions land on `window`) or via `require()` in Node (functions
land on `module.exports`). They are **inert by default**  -  every function is
defined/exported but nothing runs automatically; requiring the file just
gives you the exports object, and running it directly with `node file.js`
prints an About banner.

## Templates

| File | Contains | Use when the script needs to... |
|---|---|---|
| `assets/BEJSON_Template_JS_Validator-v1.js` | Error registry (`BEJSON_ERRORS`, codes 1-29) + `bejson_validator_validate_string` / `bejson_validator_validate_file` (Node-only, uses `fs`) / `bejson_validator_get_report` / error-state accessors | only check/validate BEJSON documents |
| `assets/BEJSON_Template_JS_Full-v1.js` | Same, plus BEJSON Core under `Core` (field-map cache `bejson_core_get_field_map`/`_get_field_index`, `bejson_core_serialize`, `bejson_core_is_valid/_get_version/_get_stats`, `BEJSONEngine`, and `Core.Crypto.encryptRecord`/`decryptRecord`  -  Web Crypto AES-GCM per-record encryption with an LRU key cache) | needs field-map lookups, serialization, stats, or record-level encryption in addition to validation |

Default to **Full** unless the user explicitly wants a pure validation
utility.

## Workflow

1. Copy the matching template from `assets/` to the new script's path.
2. Update the header comment block: `Name`, `Description`, `Date Created`
   (today), and generate a **new** `RELATIONAL_ID` (fresh UUID  -  never reuse
   the template's). Keep Author/Contact/Format_Creator lines unchanged
   (Section 9.2 crediting is mandatory).
3. `BEJSON_TEMPLATE_VERSION` starts at `1` / Package_Version 100 for a first
   delivery; bump on every subsequent change per Section 3.3.
4. Add real logic below the embedded sections. In Node: `const lib =
   require('./thisfile.js'); lib.bejson_validator_validate_string(text);`  - 
   everything is namespaced under one exports object (`BEJSON_ERRORS`,
   `Core`, `bejson_validator_*`, `BEJSONValidationError`), nothing pollutes
   `module.exports` beyond that object. In the browser: include via
   `<script src="thisfile.js"></script>`, then call the same function names
   as globals (`window.BEJSON_ERRORS`, `window.BEJSON.*` for Core, top-level
   `bejson_validator_*`).
5. Always resolve fields by name through `Core.bejson_core_get_field_map` /
   `bejson_core_get_field_index`  -  never by hardcoded array index (BEJSON
   Core Mandate, non-negotiable for code dated after 2026-08-14).
6. If embedding this in an HTML page instead of a bare `.js` file, prefer
   the existing `BEJSON_Template_HTML_Validator-v1.html` /
   `BEJSON_Template_HTML_Full-v1.html` templates (separate deliverables)  - 
   those already wrap this same library code in `<script>` tags with the
   black/white/red palette and credit footer per Section 8.1/9.2. This skill
   is for a standalone `.js` file.

## Important: single-file de-duplication already applied

The original per-family source files (`lib_bejson_Core_bejson_errors.js`,
`_core.js`, `_validator.js`) each independently redeclare `const
BEJSON_ERRORS = ...` and do a clobbering `module.exports = X`  -  harmless
when they're three separate `<script>` tags (each gets its own top-level
scope in a browser) but a hard `SyntaxError` (duplicate `const`) or a
silently-overwritten `module.exports` when concatenated into one file. These
two templates already strip the redundant re-declarations and clobbering
exports and replace them with one consolidated export block at the end  - 
**do not** re-paste the original per-file boilerplate from the source libs
when hand-editing these templates, or the collision comes back.

## Error codes available

Same numbering as the Python/Bash templates: validator codes 1-16, Core ops
17-29, MFDB validator 30-49 and MFDB core 50-72 constants are declared in
`BEJSON_ERRORS` but their function bodies are not embedded here (Core family
only). Access via `BEJSON_ERRORS.E_INVALID_JSON` etc. (Node) or
`window.BEJSON_ERRORS.E_INVALID_JSON` (browser).

## Do not

- Don't alter the embedded Core/Validator function bodies when scaffolding
  (Section 7.3  -  Core family libraries are frozen); build new logic around
  them.
- Don't add a Node-only API (like raw `fs` calls) to code paths meant to run
  in the browser  -  `bejson_validator_validate_file` already guards this via
  the internal `IO_PROVIDER` and will throw a clear error in a browser
  context instead of failing silently.
- Don't ship the template unmodified  -  header placeholders must be filled in
  for the specific script being created.
