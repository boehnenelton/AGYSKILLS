---
name: agy-prompt-automator
description: >-
  Author, structure, and execute Antigravity CLI (agy) prompts, headless tasks, targeted project audits, and BEJSON 104a workflows with user-directed sandboxing and minute-based scheduling. Use when creating agy prompt templates, structuring targeted subfolder audits with explicit user approval, generating 25-50 point feature menus or schemas, and running sandboxed CLI workflows across projects in Termux, Linux, or macOS. Do NOT use for general shell script scaffolding (use bejson-scaffold-bash).
---
# agy-prompt-automator

Developer framework for authoring, structuring, and dispatching Google Antigravity CLI (`agy`) tasks, prompt templates, project audits, and BEJSON 104a-backed workflows under user-directed sandbox control.

## Summary

Provides structured templates and utilities for constructing headless `agy` prompts, targeted project audits, and data schemas. Enforces safe execution through container sandboxing (`--sandbox`), plan-first review modes (`--mode=plan`), and BEJSON 104a Field Map Caching standards.

## When to Use

- Authoring structured prompts for Antigravity CLI (`agy`) tasks.
- Running user-approved headless prompts with `--sandbox` isolation.
- Auditing a target project by selecting an internal subfolder and applying specialized audit disciplines.
- Generating structured, sequentially numbered lists (e.g. 25-50 point feature menus, function catalogs, edge-case inventories).
- Managing developer automation workflows across Termux (Android), Linux, or macOS.
- Structuring prompt presets in BEJSON 104a with runtime Field Map Caching.

## Core Antigravity CLI Command Baseline

Execute prompts with sandboxing and appropriate operational modes:

```bash
# Standard sandboxed headless execution
agy --sandbox -p "<prompt>"

# Model override targeting specific reasoning or speed tiers
agy --sandbox --model="Gemini 3.5 Flash" -p "<prompt>"

# Scoped execution targeting a user-specified project directory
agy --sandbox --dir="/path/to/project" -p "<prompt>"

# Execution mode selection
agy --sandbox --mode=plan -p "<prompt>"         # Plan only (safe inspection)
agy --sandbox --mode=accept-edits -p "<prompt>" # Auto-apply file edits in sandbox
```

### Supported Models
- Default / Fast: `"Gemini 3.5 Flash"`, `"Gemini 3.5 Flash (High)"`, `"Gemini 3.5 Flash (Low)"`, `"Gemini 3.7 Flash"`
- Deep Reasoning: `"Gemini 3.1 Pro"`, `"Claude Sonnet 4.6 (Thinking)"`, `"Claude Opus 4.6 (Thinking)"`
- Open-Source: `"GPT-OSS 120B"`

## Standard Subdirectory Routing

Organize all generated outputs into dedicated subdirectories within the target project root:

- `reports/`: Architecture overviews, dependency graphs, and health summaries.
- `reports/audits/` and `dev/`: Security reviews, dead code listings, and schema integrity audits.
- `target/ideas/`: 25-50 point feature menus, CLI flag brainstorms, and subagent roadmaps.
- `target/schemas/`: BEJSON 104/104a schemas, registries, and agent system instructions.
- `dev/security-notes.md`: Security vulnerability log.
- `dev/dead_code.md`: Verified dead and uncalled code candidates.

## Targeted Subfolder Audit Workflows

When auditing a project, select a concrete subfolder with user consent and pair it with a specialized audit discipline:

1. **Security Audit**:
   Scan for hardcoded secrets, shell injections, path traversal, and unsanitized subprocess calls.
   Directive: `[HOSTILE-AUDIT]` | Target: `<project>/reports/audits/security_audit_<subfolder>_<timestamp>.md`.

2. **Dead Code Purge**:
   Detect uncalled functions, unused imports, and dead variables across caller files.
   Directive: `[DEAD-CODE-PURGE]` | Log findings to `<project>/dev/dead_code.md`.

3. **BEJSON Schema Integrity**:
   Verify the 6 mandatory keys, `Format_Creator='Elton Boehnen'`, positional integrity, and field map caching.
   Directive: `[BEJSON-104]` | Target: `<project>/reports/audits/bejson_audit_<subfolder>_<timestamp>.md`.

4. **BECSS UI & Tri-Color Conformance**:
   Enforce the Tri-Color Law (`#000000`, `#FFFFFF`, `#DE2626`) and `becss-` BEM class syntax (`block__element--modifier`).
   Directive: `[BECSS-BEM]` | Target: `<project>/reports/audits/becss_audit_<subfolder>_<timestamp>.md`.

5. **Path Portability Audit**:
   Verify dynamic location via `SCRIPT_PATH = Path(__file__).resolve().parent` and ban hardcoded absolute paths.
   Directive: `[SURGICAL]` | Target: `<project>/reports/audits/path_audit_<subfolder>_<timestamp>.md`.

6. **Error Handling & Logging**:
   Enforce Python `logging` module (ban `print()`) and deterministic exit codes (0, 10, 20, 30).
   Directive: `[SURGICAL]` | Target: `<project>/reports/audits/error_audit_<subfolder>_<timestamp>.md`.

## Minute-Based Scheduling & Heartbeat Daemons

Parameterize execution intervals in minutes to maintain predictable, user-monitored cadences:

```bash
#!/usr/bin/env bash
MIN_MINUTES=5
MAX_MINUTES=15

while true; do
  DELAY_MINS=$(( MIN_MINUTES + RANDOM % (MAX_MINUTES - MIN_MINUTES + 1) ))
  
  # Execute user-approved sandboxed task
  agy --sandbox --dir="$TARGET_PROJECT" -p "$PROMPT"
  
  # Pause for randomized minute delay
  sleep "${DELAY_MINS}m"
done
```

### Termux Background Execution
On Android Termux, manage background tasks with user notifications and wake-lock controls:

```bash
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
trap 'termux-wake-unlock; exit 0' SIGINT SIGTERM

while true; do
  python3 scripts/agy_random_auditor.py --project "$HOME/projects/MyApp" --once
  sleep "15m"
done
```

## BEJSON 104a Configuration & Field Map Caching

All preset registries must implement the 6 mandatory top-level keys and primitive types:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["AgyPreset"],
  "Fields": [
    {"name": "preset_id", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "default_subject", "type": "string"},
    {"name": "prompt_template", "type": "string"}
  ],
  "Values": [
    ["preset_audit", "Security Audit", "API Routing", "[HOSTILE-AUDIT] Scan @src/ for leaks."]
  ]
}
```

### Runtime Field Map Resolution
Always resolve row values through `field_map` rather than hardcoded column numbers:

```python
def bejson_get_field_map(doc: dict) -> dict[str, int]:
    return {f["name"]: i for i, f in enumerate(doc.get("Fields", []))}

fmap = bejson_get_field_map(doc)
prompt = row[fmap["prompt_template"]]
```

## Bundled Automation Scripts

The skill provides safe, user-directed automation drivers located in `scripts/`:

1. `scripts/agy_random_auditor.py`:
   Audits a chosen project directory by inspecting internal subfolders and applying specialized audit types with sandbox isolation.
   Usage: `python3 scripts/agy_random_auditor.py --project "/path/to/project" --dry-run`

2. `scripts/agy_project_randomizer.py`:
   Selects a project directory with user authorization and executes a workflow on a monitored timer.
   Usage: `python3 scripts/agy_project_randomizer.py --root-dir="$HOME/projects" --once`

3. `scripts/agy_subject_list_automator.py`:
   Minute-based domain automator generating modular library functions, 50-point feature menus, and schemas.
   Usage: `python3 scripts/agy_subject_list_automator.py --subject bejson_data_architecture --once`

## Gotchas & Pitfalls

- **Safe Sandboxing**: Always include `--sandbox` to ensure generated commands and subprocesses execute within an isolated container.
- **Directory Exclusions**: Always exclude `.git`, `__pycache__`, `.pytest_cache`, and `reports` when discovering project folders or subfolders.
- **Positional Integrity**: When appending presets to a BEJSON 104a document, ensure the appended row matches the `Fields` length exactly and pads missing fields with `null`.
- **String Variable Expansion**: In Bash, avoid using `${var//pattern/replacement}` directly when the replacement contains `&` characters, as Bash expands `&` to the matched pattern. Use Python one-liners or safe replacement utilities instead.
- **Path Resolution**: Never hardcode paths in scripts. Use `Path(__file__).resolve().parent` in Python and standard `BASH_SOURCE` resolution in Bash.
