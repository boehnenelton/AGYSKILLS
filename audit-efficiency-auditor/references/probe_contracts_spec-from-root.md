# Target Probing Contracts Specification (Layer 2)

- **Version**: `1.0.0`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Verification Gate)`
- **Binding**: `Policy §1.1, §6.1, §6.2, §12.1`
- **RELATIONAL_ID**: `497c8079-38bf-4740-a8a7-7e8799a0e631`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Scope & Execution Surfaces

The efficiency auditor accepts any target path—single script, subsystem directory, BEJSON store, or complete skill ecosystem.

### 1.1 Python Codebase Surface
- Evaluates AST nodes for:
  - Loop-nested file I/O (`EFF_04`).
  - Loop-nested subprocess execution (`EFF_05`).
  - Duplicate function bodies across distinct files (`EFF_02`).
  - Direct row index lookups on BEJSON structures (`EFF_03`).

### 1.2 Bash Script Surface
- Evaluates line tokens and pipeline structures for:
  - Utility subprocess spawning inside `while read` or `for` loops (`EFF_05`).
  - Redundant subshell evaluations (`$()`) within high-iteration loops.
  - Unbuffered file append thrashing (`>>`) inside iterative loops (`EFF_04`).

### 1.3 BEJSON & MFDB Surface
- Ingests entity stores (`.104.bejson`, `.104a.bejson`, `.105.bejson`):
  - Measures value column redundancy frequency across records (`EFF_08`).
  - Flags unnormalized repetitive data payloads suitable for entity splitting.

### 1.4 Skill Bundle & Prompt Surface
- Audits `.agents/skills/` and `~/.gemini/config/skills/`:
  - Enforces `SKILL.md` line ceiling `<= 500` lines (`EFF_06`).
  - Enforces frontmatter `description` ceiling `<= 1024` chars.
  - Checks for lingering zero-filler violations or verbose fluff copy.

### 1.5 Binary & Asset Deduplication Surface
- Hashes binary assets across target directory tree:
  - SHA-256 byte digest matching detects redundant duplicate files (`EFF_07`).

---

## 2. Mandatory Deliverable Contract

Every execution of `probe_efficiency.py` against a target path automatically writes the canonical findings report to:

```text
<target_root>/efficiency_report.md
```

- When target is a directory: `<target_dir>/efficiency_report.md`
- When target is a file: `<target_file_parent>/efficiency_report.md`
- The file contains high-density tabular Markdown telemetry with finding codes, severities, affected line numbers, and actionable remediation steps.
- Excluded from self-scanning to prevent recursive duplicate asset warnings.
