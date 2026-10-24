---
name: agy-skill-refactor
description: Audit, refactor, modernize, and harmonize Antigravity CLI (agy) skills, prompt presets, and headless automation daemons. Enforces the 2026 Anti-Collision Constraint Protocol, mandatory --sandbox container isolation, two-phase --mode=plan and --mode=accept-edits workflows, standardizes output routing to reports/ and target/, converts presets to BEJSON 104a with field map caching, and parameterizes minute-based scheduling. Use when auditing or refactoring agy skills, prompt templates, daemons, or CLI automation pipelines. Do NOT use for Gemini Spark skills (use spark-skill-refactor) or general application source code (use bejson-codebase-refactor).
---
# agy-skill-refactor

Systematic refactoring and optimization framework for Google Antigravity CLI (`agy`) skills, prompt templates, and background automation daemons. Enforces container sandboxing, plan-first inspection modes, deterministic output routing, BEJSON 104a data contracts, and the 2026 Anti-Collision Constraint Protocol.

## Summary

Audits and transforms Antigravity CLI (`agy`) skills, prompt catalogs, and execution runners. Strips conversational preamble, enforces mandatory container sandboxing (`--sandbox`), splits workflows into plan and accept-edits phases, routes artifacts to canonical directories, standardizes daemon timing variables into minute-based intervals, and audits skill triggers against the 2026 Anti-Collision Constraint Protocol.

## When to Use

- Refactoring Antigravity CLI (`agy`) prompt templates to eliminate conversational fluff and ensure zero-preamble execution.
- Enforcing mandatory `--sandbox` isolation across headless scripts, daemons, and shell pipelines.
- Restructuring mutative prompts into two-phase execution: `--mode=plan` (inspection) followed by `--mode=accept-edits` (mutation).
- Converting hardcoded prompt strings into structured BEJSON 104a preset registries with runtime field map caching.
- Standardizing output artifact paths to canonical project directories (`reports/`, `reports/audits/`, `dev/`, `target/ideas/`, `target/schemas/`).
- Refactoring background runners and daemons on Linux, macOS, or Android Termux to use minute-based scheduling and wake-lock controls.
- Hardening skill frontmatter descriptions against router trigger collisions using the Tri-Partite Description Contract.

## When NOT to Use

- Refactoring general application source code or modules (use `bejson-codebase-refactor`).
- Architecting new greenfield skills from scratch across the 6 layers (use `skill-architect`).
- Updating visual templates or UI wireframes (use `template-architect` or `behtml-layout-builder`).
- Executing interactive CLI prompts manually without automated refactoring goals.

## Core Antigravity CLI Refactoring Standards

1. **Mandatory Sandboxing**: Every `agy` invocation in scripts or automated pipelines must pass `--sandbox` to isolate tool execution within project boundaries.
2. **Two-Phase Operational Modes**:
   - Inspection and Auditing: Must use `--mode=plan` for read-only AST inspection, diff generation, and report generation.
   - Code Mutation: Must use `--mode=accept-edits` inside a sandboxed workspace. Never run uncontrolled auto-accept without prior planning.
3. **Model Tier Optimization**:
   - Use `"Gemini 3.5 Flash"` or `"Gemini 3.7 Flash"` for heartbeat daemons, high-frequency triage, and 25 to 50 point list generation.
   - Reserve `"Gemini 3.1 Pro"` or deep reasoning tiers for multi-file code refactoring, complex AST transformations, and hostile security audits.
4. **Zero-Fluff Directives**: Prompts must start with an explicit directive tag (`[HOSTILE-AUDIT]`, `[DEAD-CODE-PURGE]`, `[BEJSON-104]`, `[BEJSON-104A]`, `[BECSS-BEM]`, `[SURGICAL]`, `[PLAN]`) and mandate zero conversational filler.
5. **Minute-Based Scheduling**: Background loops must parameterize intervals in integer minutes (e.g., `MIN_MINUTES=5`, `MAX_MINUTES=15`) with randomized jitter to prevent execution collisions.
6. **2026 Anti-Collision Trigger Hardening**:
   - Enforce the Tri-Partite Description Contract: (1) Capability Statement, (2) Positive Activation Triggers (`Use when...`), (3) Symmetrical Negative Guardrails (`Do NOT use for X, use Y instead`).
   - Purge generic buzzwords (`handle`, `process`, `manage`, `utilities`) from skill descriptions.
   - Enforce 3-stage progressive disclosure (Discovery metadata -> Activation markdown -> Execution assets) and a 500-line ceiling on `SKILL.md`.

Refer to `references/agy_prompt_contracts.md` for directive tag mappings and directory routing specifications.

## Architectural Workflow Layers

Multi-skill and multi-tool `agy` systems operate across four symbiotic layers:

- **Layer 1 (Audit)**: Read-only inspection tools running with `--mode=plan`. Emits findings to `reports/audits/` and appends entries to `dev/dead_code.md` and `dev/security-notes.md`. Suffix: `-auditor`.
- **Layer 2 (Ideation)**: Generative tools synthesizing 25 to 50 point feature menus and CLI flag universes in `target/ideas/`. Suffix: `-ideation-feature-composer`.
- **Layer 3 (Specification)**: Schema tools building BEJSON 104/104a registries and prompt templates in `target/schemas/`. Suffix: `-schematizer`.
- **Layer 4 (Refactor)**: Surgical code modification engines operating under `--mode=plan` followed by `--mode=accept-edits`. Suffix: `-refactor`.

## Individual agy Skill & Prompt Refactoring Workflow

When refactoring an individual `agy` skill or prompt template, follow this four-step sequence:

### Step 1: Baseline Inspection
Scan the target skill or script for compliance using the bundled linter:

```bash
python3 skills/agy-skill-refactor/scripts/agy_skill_linter.py skills/<skill-name>
```

### Step 2: Prompt Hardening and Anti-Collision Formatting
Transform loose conversational requests into structured, directive-backed prompt templates:
- Add the appropriate directive tag at the start of the prompt.
- Explicitly define target scope (e.g., `Target Scope: src/`).
- Specify required output format and exact destination filepath using timestamp tokens (`${TIMESTAMP}`).
- Include the negative constraint: "Zero conversational fluff, preamble, pleasantries, or closing remarks. Output only the structured deliverable."
- Format the frontmatter `description` into the Tri-Partite Contract (Capability, Triggers, Negative Guardrails).

### Step 3: Flag and Mode Verification
Audit all CLI command strings in bundled scripts:
- Verify that `--sandbox` is present in every call.
- Verify that read-only workflows pass `--mode=plan`.
- Verify that mutative workflows explicitly specify `--mode=accept-edits` and target the project root via `--dir`.
- Replace hardcoded model strings with appropriate tier selections.

### Step 4: BEJSON 104a Registry Conversion
If the skill manages multiple prompts or presets, convert them from raw strings to a BEJSON 104a registry:
- Include the 6 mandatory keys: `Format`, `Format_Version`, `Format_Creator`, `Records_Type`, `Fields`, `Values`.
- Set `Format_Creator: "Elton Boehnen"`.
- Implement dynamic field map caching (`bejson_get_field_map(doc)`) instead of hardcoded column numbers.

## Group & Ecosystem Workflow Harmonization

When refactoring a cluster of interconnected `agy` automation tools:

### Step 1: Directory Tree Partitioning
Enforce exclusive output directory boundaries across tools to eliminate race conditions:
- Auditors write only to `reports/audits/` and append to `dev/`.
- Idea generators write only to `target/ideas/`.
- Schema builders write only to `target/schemas/`.
- Refactorers touch only approved source files.

### Step 2: Timestamp Salting and Advisory Locks
- Ensure every generated report includes a timestamp suffix (`_${TIMESTAMP}.md`) so parallel runs do not overwrite files.
- For shared files (such as `dev/security-notes.md`), implement file locking using `fcntl.flock` (Python) or `flock` (Bash) around append operations.

### Step 3: Script Path Portability
Eliminate hardcoded absolute paths across all scripts and daemons:
- In Python: Use `SCRIPT_PATH = Path(__file__).resolve().parent`.
- In Bash: Use `SCRIPT_PATH="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"`.

### Step 4: Daemon Telemetry and Exit Code Standardization
Standardize return codes across all runner scripts:
- `0`: Clean execution and valid deliverable produced.
- `10`: Process lock contention or skipped cycle.
- `20`: Sandbox boundary violation or permission denial.
- `30`: Upstream timeout or API failure.

## Gotchas & Anti-Patterns

- Never omit `--sandbox` when invoking `agy` from scripts or background loops. Unsandboxed executions risk host filesystem contamination.
- Avoid passing raw, unstructured prompts to `agy`. Always prepend an operational directive tag.
- Never write vague skill descriptions lacking negative guardrails; this causes trigger collisions in multi-skill agents.
- Never use hardcoded column indices (`row[1]`) when accessing BEJSON data. Schema evolution will cause silent data corruption.
- On Android Termux, never launch long-running daemons without acquiring `termux-wake-lock` and setting termination traps (`termux-wake-unlock`).
