---
name: goal-drift-auditor
description: >-
  Continuous adversarial blocker and verification auditor that monitors code
  modifications, tool calls, and file operations to prevent goal drift, scope
  creep, and counteracting actions. Enforces immediate execution halts upon
  discovering contradictions against the active goal contract, presenting a
  structured discrepancy report with an explicit User Override Gateway (Halt
  and Revert, Confirm Override and Proceed per Policy Section 1.2, or Amend
  Goal Contract). Use when auditing active agent execution against goal
  contracts, checking git diffs for scope creep, intercepting counter-productive
  file edits, or confirming user override requests. Do NOT use for formalizing
  initial goal contracts (use goal-contract-architect), breaking goals down into
  task checklists (use goal-roadmap-composer), final pre-delivery release audits
  (use audit-hostile-finalizer), or static AST policy auditing (use
  policy-bejson-auditor).
---

# Skill: `goal-drift-auditor` (Layer 2 Execution Blocker & Override Gateway)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Validation & Blocker Engine)`
- **Policy Anchor**: `Policy §1.2 (Override Protocol) & §7.2 (Goal-Driven Execution)`
- **Embedded Tool**: [`scripts/goal_drift_auditor.py`](./scripts/goal_drift_auditor.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`goal-drift-auditor` is the continuous runtime gatekeeper for goal-driven execution. It actively monitors agent trajectories, modified file lists, and pending tool invocations against the authoritative **Goal Contract** (`dev/goal_contract.104a.bejson` or `dev/active_goal.md`).

When an agent operation counteracts the set goal (e.g. modifying out-of-scope files, breaking previously established passing criteria, or introducing unauthorized architectural refactors), this skill triggers an **Immediate Execution Halt**.

---

## 2. The User Override Confirmation Protocol (Policy §1.2)

Per Policy §1.2, a clear, plain-English user instruction authored by the policy creator overrides constraints upon explicit confirmation. When `goal-drift-auditor` halts execution, it NEVER silently fails or blindly continues; it presents the **Tri-Option User Override Gateway**:

```text
+-----------------------------------------------------------------------------+
|                     GOAL DRIFT DETECTED: EXECUTION HALTED                   |
+-----------------------------------------------------------------------------+
Active Goal:      Implement BKS-1 validation in publication-book-builder
Trigger Action:   Modified /storage/emulated/0/Admin/Libraries/libraries_104/...
Violation Code:   DRIFT_OUT_OF_SCOPE_MODIFICATION
Severity:         CRITICAL BLOCKER
-------------------------------------------------------------------------------
The pending action modifies an authoritative library outside the declared goal scope.
Please select an operational path to continue:

[1] HALT & REVERT (Recommended)
    Revert the pending file modification and resume the planned roadmap.

[2] CONFIRM OVERRIDE & PROCEED (Policy §1.2)
    Explicitly grant an ad-hoc override. The exemption will be logged to
    'dev/goal_overrides.md' and execution will resume immediately.

[3] AMEND GOAL CONTRACT
    Halt execution and invoke 'goal-contract-architect' to officially expand
    the project goal contract to include library modifications.
+-----------------------------------------------------------------------------+
```

### Protocol Invariants:
1. **Explicit Prompting**: If interactive, present the options via interactive choice. If headless, halt execution with exit code `30` and write the discrepancy report to `reports/audits/goal_drift_halt.md`.
2. **Override Logging**: When Option 2 is confirmed, the auditor appends an immutable record to `dev/goal_overrides.md`:
   ```markdown
   ## Override Confirmed: [TIMESTAMP]
   - **Action**: Modified libraries_104/Lib_PY/...
   - **Reason**: User confirmed ad-hoc exemption per Policy §1.2
   - **Authorized By**: User Explicit Confirmation
   ```
3. **Resumption**: Once confirmed, the auditor suppresses the alert for that specific action signature and releases the execution lock.

---

## 3. Discrepancy Detection Taxonomy

| Drift Code | Failure Category | Trigger Condition |
| :--- | :--- | :--- |
| **`DRIFT_SCOPE_EXPANSION`** | Scope Creep | Modifying files outside the declared `target_directories` or `target_files` list. |
| **`DRIFT_CONSTRAINT_BREACH`** | Hard Negative | Violating an explicit negative constraint declared in the goal contract. |
| **`DRIFT_PREMATURE_COMPLETION`**| False Finish | Claiming task completion without executing the automated test suite in the Definition of Done. |
| **`DRIFT_REGRESSION`** | Regression | Reverting or breaking a checklist step marked completed in the active roadmap. |

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When executing automated drift auditing, always enforce `--sandbox` containment and deterministic exit codes (`0` = Clean Pass, `10` = Path Failure, `20` = Env Failure, `30` = Drift Contradiction / Halt):

```bash
python3 scripts/goal_drift_auditor.py --contract "dev/goal_contract.104a.bejson" --check-diff
```

---

## When NOT to Use

Do NOT use `goal-drift-auditor` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Formalizing initial goal contracts and acceptance criteria**: Redirect immediately to `goal-contract-architect`.
- **Composing small-step checklist roadmaps**: Redirect immediately to `goal-roadmap-composer`.
- **Conducting hostile pre-release quality audits at session wrap-up**: Redirect immediately to `audit-hostile-finalizer`.
- **Auditing source code AST for BEJSON field map caching**: Redirect immediately to `policy-bejson-auditor`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
