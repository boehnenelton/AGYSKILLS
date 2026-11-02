---
name: goal-contract-architect
description: >-
  Formalize, conceptualize, and author authoritative Goal Contracts
  (dev/goal_contract.104a.bejson) defining clear objective statements, hard
  negative constraint boundaries, expected filesystem deliverables, automated
  Definition of Done (DoD) verification commands, and Policy Section 1.2 user
  override protocols. Grounded in Policy Section 7.2 Goal-Driven Execution, this
  skill locks project boundaries before execution begins, preventing ambiguity
  and scope drift. Use when defining new operational goals, formalizing project
  requirements into testable acceptance criteria, specifying negative boundaries,
  or updating amended goal scopes. Do NOT use for active execution drift auditing
  or user override enforcement (use goal-drift-auditor), composing small-step
  markdown task checklists (use goal-roadmap-composer), planning backend database
  schemas (use planning-schema-planner), or designing Multi-MFDB clusters (use
  mfdb-multi-architect).
---

# Skill: `goal-contract-architect` (Layer 5 Goal Contract Architect)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (System Architecture & Goal Formalization)`
- **Policy Anchor**: `Policy §1.2 (Override Protocol) & §7.2 (Goal-Driven Execution)`
- **Canonical Schema**: `dev/goal_contract.104a.bejson`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`goal-contract-architect` is the canonical Layer 5 skill for engineering formal, machine-readable, and testable **Goal Contracts**. Before any multi-step coding task, refactor, or autonomous workflow begins, this skill establishes the strict operational boundaries required by Policy §7.2:

1. **Objective Statement**: A single, unambiguous declarative statement defining the target final state.
2. **Target File Boundaries**: Explicit array of directories and files permitted to be created or modified.
3. **Hard Negative Constraints**: Strict list of forbidden paths (e.g. `$ADMIN_LIBRARIES`), forbidden tools, and off-limits systems.
4. **Definition of Done (DoD)**: Machine-executable validation assertions (e.g. exit code `0` on test command).
5. **Policy §1.2 Override Protocol**: Codified mechanism for the user to grant ad-hoc exemptions upon confirmation.

---

## 2. Canonical Goal Contract Schema (BEJSON 104a)

Goal contracts are stored at `dev/goal_contract.104a.bejson` using the standardized schema:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["GoalContract"],
  "Fields": [
    {"name": "goal_uuid", "type": "string"},
    {"name": "objective", "type": "string"},
    {"name": "allowed_targets", "type": "string"},
    {"name": "negative_constraints", "type": "string"},
    {"name": "definition_of_done_command", "type": "string"},
    {"name": "override_allowed", "type": "boolean"},
    {"name": "created_at", "type": "string"}
  ],
  "Values": [
    [
      "a1b2c3d4-e5f6-4a1b-8c2d-3e4f5a6b7c8d",
      "Implement BKS-1 validation and rendering in publication-book-builder",
      "[\"config/skills/publication-book-builder\"]",
      "[\"/storage/emulated/0/Admin/Libraries/libraries_104\"]",
      "python3 scripts/bks_tool.py --validate --level 4",
      true,
      "2026-11-02T00:00:00Z"
    ]
  ]
}
```

---

## 3. The Five Invariant Pillars of a Valid Goal Contract

Every contract authored by this skill must fulfill five criteria:

1. **Testable Verification**: A goal cannot rely on subjective prose. The DoD must provide a deterministic script, test, or linter invocation.
2. **Negative Scoping**: If a goal does not specify what *not* to touch, it is considered incomplete. Negative constraints protect stable libraries from unintended edits.
3. **Immutability During Execution**: Once locked, the contract cannot be silently rewritten by an autonomous subagent. Scope adjustments require explicit user confirmation.
4. **Override Gateway Integration**: The contract explicitly enables Policy §1.2 exemptions so the user retains complete operational control.
5. **Atomic Workspace Anchoring**: Contracts persist relatively within the target project root (`dev/goal_contract.104a.bejson`) or global user space.

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to generate or scaffold goal contracts, always mandate `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Formalize goal contract for new payment microservice using goal-contract-architect."
```

---

## When NOT to Use

Do NOT use `goal-contract-architect` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing execution drift and enforcing user override halts**: Redirect immediately to `goal-drift-auditor`.
- **Composing sequential small-step task checklists**: Redirect immediately to `goal-roadmap-composer`.
- **Pre-planning backend database entity schemas**: Redirect immediately to `planning-schema-planner`.
- **Designing Multi-MFDB cluster topologies**: Redirect immediately to `mfdb-multi-architect`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
