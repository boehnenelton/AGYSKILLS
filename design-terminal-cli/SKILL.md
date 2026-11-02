---
name: design-terminal-cli
description: >-
  Establish authoritative design principles, architectural patterns, and ergonomic
  standards for headless and interactive terminal Command-Line Interfaces (CLIs).
  Governs the Loaded Chamber stateful target pattern, multi-mode entry routing,
  decoupled target acquisition and execution, deterministic exit codes, atomic state
  persistence, and Policy §4.5 pointer-only environmental compliance. Houses canonical
  exemplars including the Stateful Multi-Mode CLI and the Loaded Chamber context
  engine. Use when designing, auditing, or refactoring terminal CLI tools, subcommand
  trees, or headless automation scripts. Do NOT use for interactive visual menus
  or terminal dashboard displays (use design-terminal-menu), 57-column BEJSON terminal menus
  (use bejson-tui-menu-builder), bare zero-filler template skeletons (use template-literal-skeleton),
  or non-file CLI utility bootstrapping (use auto-processing-standardizer).
---

# design-terminal-cli (Layer 4 Presentation & Design)

## Summary

`design-terminal-cli` defines the canonical design principles, human-computer interaction standards, and execution architecture for terminal command-line interfaces. Part of the **Design Domain** (`design-*`), it is strictly separated from the **Template Domain** (`template-*`): design skills establish the *axioms, ergonomic laws, and behavioral mechanics*, while template skills stamp out mechanical skeletons.

`design-terminal-cli` eliminates parameter typing fatigue, conflicting subcommand flag sprawl, and brittle one-shot argument pipelines. It standardizes the **Loaded Chamber Target Architecture**, where operational context (target, category, session, subsystem, flags) is locked once into persistent state, allowing subsequent actions and queries to execute with zero argument friction.

---

## When to Use

- Designing or refactoring command-line interfaces (CLIs), CLI routers, and headless terminal utilities.
- Implementing the Loaded Chamber pattern to decouple target acquisition from repetitive action execution.
- Structuring multi-mode CLI entry points (e.g. Mode 1 Logging, Mode 2 Reports Indexing & Sync) to prevent argument collision.
- Standardizing deterministic POSIX exit codes (0 = Success, 1 = Missing Target, 2 = Syntax Error, etc.).
- Enforcing Policy §4.5 pointer-only persistence (abstract `ENV:<var>` pointers) and atomic state serialization (`.tmp` -> replace).
- Separating machine-readable JSON payloads on `stdout` from human diagnostic alerts on `stderr`.

## When NOT to Use

- Designing visual terminal user interface (TUI) menus or status dashboards (use `design-terminal-menu`).
- Generating bare zero-filler structural skeletons without design opinions (use `template-literal-skeleton`).
- Scaffolding basic Python CLI scripts with embedded validators (use `auto-processing-standardizer`).
- Mutating or validating underlying BEJSON data files on disk (use `bejson-104-core`).

---

## 1. The Core Principles of Terminal CLI Design

Every terminal CLI designed under this skill MUST adhere to the five core principles detailed in [`references/terminal_cli_design_spec.md`](./references/terminal_cli_design_spec.md):

1. **Decoupled Target Acquisition (Loaded Chamber)**:
   - Separate setting context from executing operations.
   - Command pattern:
     ```bash
     # 1. Lock chamber context once:
     cli context --set-target "BEJSON_Standards" --set-category "core"
     # 2. Fire actions repeatedly with zero repetitive flags:
     cli exec compile
     cli exec verify
     # 3. Inspect or nullify when complete:
     cli context --clear
     ```
2. **Multi-Mode Routing**:
   - Complex tools group workflows into distinct operational modes (e.g. Mode 1 Logging vs. Mode 2 Asset Indexing) to maintain clean subcommand trees.
3. **Deterministic POSIX Exit Codes**:
   - Exit `0` strictly for clean execution; distinct non-zero integers for target resolution failure (`1`), syntax errors (`2`), or I/O faults (`3`).
4. **Fail-Safe Ad-Hoc Overrides**:
   - Always allow `--target <name>` to override the loaded chamber for a single command without mutating persistent state.
5. **Pointer-Only Atomic Persistence**:
   - State files must never contain plain-text secrets or personal absolute paths; save atomically via temporary swap files.
6. **Dynamic Status Feedback Discipline**:
   - Dynamic command responses strictly enforce:
     - **Positive Feedback**: Bold White, **ALL CAPS** with `[✓]`.
     - **Bad Feedback (Non-option character / error)**: Bold Red, **lowercase with `[X]`**.
     - **Neutral Feedback**: Normal standard rules with `[*]`.

---

## 2. Canonical Showcase Exemplars

1. **Standalone Stateful Context Engine**:
   - Reference implementation: [`scripts/showcase_stateful_cli.py`](./scripts/showcase_stateful_cli.py)
   - Demonstrates context locking (`context --set-target ...`), status inspection (`context --json`), target execution (`exec <verb>`), and chamber clearing (`context --clear`).
2. **Unified Management Tool Router**:
   - Production exemplar located at `$ADMIN_SYSTEM_TOOLS/management_tool/management_tool.py`.
   - Routes between Mode 1 (Stateful Standards Logging) and Mode 2 (Research Reports Tracking & Indexing) with shared context injection.

---

## 3. Verification & Testing

To test the showcase stateful CLI exemplar:

```bash
# 1. Lock target into chamber
python3 ~/.gemini/config/skills/design-terminal-cli/scripts/showcase_stateful_cli.py context --set-target "My_Project" --set-category "tools"

# 2. Fire action against loaded target
python3 ~/.gemini/config/skills/design-terminal-cli/scripts/showcase_stateful_cli.py exec "audit"

# 3. Clear chamber state
python3 ~/.gemini/config/skills/design-terminal-cli/scripts/showcase_stateful_cli.py context --clear
```
