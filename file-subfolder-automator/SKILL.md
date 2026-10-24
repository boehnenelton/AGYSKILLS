---
name: file-subfolder-automator
description: >-
  Scaffold standardized relative subfolder architectures (lib, config, data, exports, backups, dev, docs), migrate misplaced tracking files to dev per Policy §1.3, bootstrap BEJSON 104a config, and generate technical overview signature docs. Use when scaffolding a new project directory, migrating legacy project tracking notes from docs/ to dev/, bootstrapping config/config.json defaults, or enforcing self-locating script path preambles. Do NOT use for session initialization download sweeps (use file-archive-coordinator), low-level 104 table CRUD (use bejson-104-core), or authoring SKILL.md bundles (use skill-architect).
---

# file-subfolder-automator (Layer 3 Subfolder Architecture & Tracking Migrator)

## Summary

`file-subfolder-automator` operates at Layer 3 (`L2_Adapters_L3_Services`) to enforce Policy §1.1 (Standardized Relative Subfolder Architecture), Policy §1.3 (Folder Migration & Documentation), Policy §4.1/§4.2 (Self-Locating Scripts), and Policy §4.4 (Script Configuration). It instantiates clean project roots with standardized subdirectories (`lib/`, `config/`, `data/`, `exports/`, `backups/`, `dev/`, `docs/`), migrates misplaced tracking notes from `docs/` to `dev/`, bootstraps `config/config.json` with BEJSON 104a defaults, and extracts AST signatures into `docs/technical_overview.md`.

## When to Use

- Scaffolding a clean root directory for any new Python, Bash, or web project.
- Enforcing standardized subdirectories: `lib/`, `config/`, `data/`, `exports/`, `backups/`, `dev/`, `docs/`.
- Migrating misplaced tracking files (`dead_code.md`, `variable_naming_issues.md`, `security-notes.md`) from `docs/` into `dev/` per Policy §1.3.
- Bootstrapping `config/config.json` with canonical BEJSON 104a defaults if missing.
- Generating `docs/technical_overview.md` function signature tables (`File_Name / Function_Name (var1, var2, var3)`).
- Auditing legacy codebases to ensure scripts use relative `$SCRIPT_PATH` resolution.

## When NOT to Use

- Do NOT use for session initialization maintenance sweeps across Download (use `file-archive-coordinator`).
- Do NOT use for raw BEJSON 104/104a tabular record CRUD (use `bejson-104-core`).
- Do NOT use for authoring or validating `SKILL.md` bundles (use `skill-architect`).
- Do NOT use for refactoring existing variable identifiers or AST code logic (use `code-taxonomy-architect`).

---

## 1. Architectural Invariants & Policy Grounding

- **Assigned Skill Tier**: Layer 3 (`L2_Adapters_L3_Services`).
- **Policy §1.1 Grounding**: Standard relative subfolder layout (`lib/`, `config/`, `data/`, `exports/`, `backups/`, `dev/`, `docs/`).
- **Policy §1.3 Grounding**: If tracking files exist in `docs/`, they must move to `dev/`.
- **Policy §4.1 / §4.2 Grounding**: Self-locating `get_script_path()` resolution in all executable scripts.
- **Policy §4.4 Grounding**: Script configuration embedded inside `config/config.json` adhering to BEJSON 104a format with Field Map Cache.
- **Embedded Tooling**: Driven by [`scripts/scaffold_subfolder_architecture.py`](./scripts/scaffold_subfolder_architecture.py).
- **CLI Launcher**: Globally runnable via [`~/.local/bin/project-subfolder-scaffold`](file:///data/data/com.termux/files/home/.local/bin/project-subfolder-scaffold).

---

## 2. Step-by-Step Operational Workflow

### Step 1: Directory Tree Scaffolding (Policy §1.1)
1. Verify target project directory exists.
2. Create standard relative subdirectories if absent:
   ```
   <project_root>/
   ├── lib/
   ├── config/
   ├── data/
   ├── exports/
   ├── backups/
   ├── dev/
   └── docs/
   ```

### Step 2: Policy §1.3 Tracking File Migration
1. Check `docs/` for any of the following tracking notes:
   - `dead_code.md`
   - `variable_naming_issues.md`
   - `security-notes.md`
2. If found in `docs/`: atomically move to `dev/` and continue tracking in `dev/`.
3. If absent from both `docs/` and `dev/`: instantiate initial markdown tracking table skeletons in `dev/`.

### Step 3: BEJSON 104a Configuration Bootstrapping (Policy §4.4)
1. If `config/config.json` is missing: instantiate with BEJSON 104a ScriptConfig schema containing default `local_lib_directory`, `master_lib_source`, and `log_level`.

### Step 4: Technical Overview Extraction (Policy §1.3)
1. If `docs/technical_overview.md` is missing: parse the project's root Python scripts using `ast.parse`.
2. Format extracted functions and classes into:
   ```text
   File_Name / Function_Name (var1, var2, var3)
   ```
3. Write formatted signatures to `docs/technical_overview.md`.

---

## 3. CLI Command Reference

* **Scaffold Current Directory:**
  ```bash
  project-subfolder-scaffold
  ```
* **Scaffold a Specific Target Project:**
  ```bash
  project-subfolder-scaffold --target /path/to/project
  ```
* **Simulate Scaffolding & Migration (Dry-Run):**
  ```bash
  project-subfolder-scaffold --target /path/to/project --dry-run
  ```
* **Inspect Configuration & Policy Info:**
  ```bash
  project-subfolder-scaffold --config
  ```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
