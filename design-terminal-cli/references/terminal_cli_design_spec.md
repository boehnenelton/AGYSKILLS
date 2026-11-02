# Terminal CLI Design Specification & Interaction Principles

- **Domain**: Design (`design-*`)
- **Author**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **Status**: Authoritative Canonical Specification
- **Version**: 1.0.0

---

## 1. Executive Summary & Philosophy

The **Design Domain** (`design-*`) governs the foundational human-computer ergonomics, interaction principles, and behavioral models of software interfaces, completely separated from the mechanical code generation and slot-binding of the **Template Domain** (`template-*`).

`design-terminal-cli` defines the authoritative design principles for non-interactive, headless, and scriptable Command-Line Interfaces (CLIs). In mobile portrait terminal environments (e.g. Android Termux) and high-throughput POSIX automation pipelines, standard CLIs suffer from severe ergonomic flaws:
- Repetitive, error-prone parameter typing (`--subsystem=x --category=y --session=z --target=w` repeated on every single invocation).
- Monolithic subcommands with conflicting, sprawling argument flags.
- Stale target drift and non-deterministic error codes.
- Failure to cleanly separate machine-readable stdout from human-facing diagnostic telemetry.

`design-terminal-cli` resolves these failure modes through the **Loaded Chamber Target Architecture** and strict multi-mode routing.

---

## 2. The Core Principles of Terminal CLI Design

### Principle 1: Decoupled Target Acquisition (The Loaded Chamber Pattern)
Instead of forcing the user or calling agent to re-declare the operational target, category, and session context on every execution, the CLI decouples target configuration from action execution:
1. **Load the Chamber**: Lock target state once per session or workflow (`cli context --set-target <item>`).
2. **Fire Actions Repeatedly**: Execute verbs directly against the loaded target without repeating arguments (`cli exec <verb>`).
3. **Inspect the Chamber**: Query currently loaded target metadata on demand (`cli context --show` or `--json`).
4. **Explicit Nullification**: Clear state deliberately when workflows conclude (`cli context --clear`).

### Principle 2: Multi-Mode Subsystem Routing
Complex CLI tools must not merge disparate functional domains into a single flat namespace. CLIs should route through distinct top-level operational modes:
- **Mode 1 (Operational / Stateful Logging)**: Minimal friction telemetry emission using the loaded chamber.
- **Mode 2 (Management / Asset Indexing & Sync)**: Batch operations, directory tree inspections, and registry maintenance.
- Each mode maintains its own focused subcommands, options, and help pages.

### Principle 3: Deterministic Exit Codes & Machine-Parseable Contracts
- `0`: Success.
- `1`: Target resolution failure (empty chamber and no override provided).
- `2`: Invalid argument or syntax error.
- `3`: Filesystem / I/O or permissions failure.
- `4`: Network / remote dispatch timeout.
- Machine-readable payloads route strictly to `stdout` (e.g. `--json`), while status, telemetry, and error alerts route to `stderr`.

### Principle 4: Fail-Safe Target Overrides
While the loaded chamber eliminates routine repetition, the CLI must always support immediate, ad-hoc overrides:
- `cli exec <verb> --target <override>` fires against the specified target without mutating the persistent chamber state.

### Principle 5: Policy §4.5 Pointer-Only Environmental Persistence
State files must never store unmasked API keys, secrets, or hardcoded personal absolute paths:
- All paths resolve dynamically relative to `$SCRIPT_PATH` or reference abstract pointers (`ENV:<var_name>`) sourced from `definitions.json`.
- State files are saved atomically using POSIX atomic rename (`.tmp` -> `replace`) to prevent file corruption during concurrent operations.

### Principle 6: Dynamic Status Feedback Discipline
Dynamic command responses and diagnostic alerts strictly enforce the feedback triad:
- **Positive Status Feedback**: Bold White, **ALL CAPS** with `[✓]` (e.g. `[✓] ACTION 'COMPILE' COMPLETED SUCCESSFULLY.`).
- **Bad / Error Feedback** (e.g. invalid arguments, missing target, non-option character): Bold Red, **lowercase with `[X]`** (e.g. `[X] no active target in chamber. set via 'context --set-target <name>' or specify --target.`).
- **Neutral Status Feedback**: Normal standard rules with `[*]` (e.g. `[*] Chamber context updated.`).
