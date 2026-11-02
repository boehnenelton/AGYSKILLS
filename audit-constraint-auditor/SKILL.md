---
name: audit-constraint-auditor
description: >-
  Audit systems, repositories, and prompt rule files against negative constraints
  and architectural boundaries. Verifies that agents have not modified frozen
  libraries ($ADMIN_LIBRARIES), altered core policy files (GEMINI.md), or used
  banned single-letter variable names, and audits rule manifests (AGENTS.md,
  SKILL.md) to ensure explicit 'DO NOT' constraints are securely locked in place.
  Use when conducting negative boundary reviews, verifying policy compliance
  against off-limits files, auditing rules for defensive negative constraints,
  or preventing architectural violations. Do NOT use for auditing positive goal
  task completion (use audit-deviation-auditor), pre-flight dependency readiness
  checks (use audit-readiness-auditor), real-time tool execution blocking (use
  goal-drift-auditor), scanning API token leaks (use policy-secrets-leak-auditor),
  or multi-audit orchestration (use audit-domain-coordinator).
---

# Skill: `audit-constraint-auditor` (Layer 2 Negative Constraint & Boundary Defense Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Validation & Diagnostic Engine)`
- **Policy Anchor**: `Policy §1.2 (Override Protocol & Negative Constraints), Policy §7.3 (Negative Constraints)`
- **Embedded Tool**: [`scripts/audit_constraint_tool.py`](./scripts/audit_constraint_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

While positive goal auditing tracks what an agent *should* accomplish, `audit-constraint-auditor` provides adversarial verification of what the agent was **strictly forbidden from doing**. In complex, multi-turn coding sessions, models often overreach - refactoring adjacent files, modifying immutable core libraries, altering master environment definitions, or adopting banned shortcuts like single-letter variables.

Furthermore, `audit-constraint-auditor` performs **Defense-in-Depth Rule Audits**, inspecting `AGENTS.md`, `GEMINI.md`, and `SKILL.md` manifests to ensure that explicit, unambiguous negative constraints are actively established before work commences.

---

## 2. Dual Audit Verification Pipeline

```text
+-----------------------+     +-----------------------+
| Mode A: Post-Run      |     | Mode B: Pre-Run       |
| Boundary Breach Audit |     | Rule Posture Audit    |
+-----------------------+     +-----------------------+
           |                             |
           v                             v
+-----------------------+     +-----------------------+
| Inspect Git Diffs &   |     | Verify Active 'DO NOT'|
| Forbidden Path Touches|     | Constraints in Rules  |
+-----------------------+     +-----------------------+
           |                             |
           +--------------+--------------+
                          |
                          v
               +-----------------------+
               | Synthesize Constraint |
               | Breach Dossier        |
               +-----------------------+
```

### Mode A: Boundary Breach Audit (Physical Inspection)
1. **Forbidden Path Sweep**: Scans `git status` and changed file paths against immutable directories:
   - `$ADMIN_LIBRARIES` / `$ADMIN_LIBRARIES_104` / `$ADMIN_LIBRARIES_105`
   - Master configuration stores (`~/.gemini/GEMINI.md`, `paths.json`)
   - Unspecified root project files outside requested scope.
2. **Code Style Negative Constraints**: Scans new/modified source code for single-letter loop/variable variables (`i`, `j`, `x`, `d`, `p`, `tmp`, `val`) prohibited by Policy §6.1.
3. **GUID Governance Compliance**: Verifies that no automated `Project_GUID` generation occurred (Policy §4.6).

### Mode B: Rule Posture Audit (Manifest Inspection)
1. Scans `AGENTS.md`, `GEMINI.md`, or active `.agents/rules/` files.
2. Verifies the presence of negative boundary statements ("DO NOT", "must never", "prohibited").
3. Flags rule files that lack negative constraints as **HIGH_RISK_UNBOUNDED**.

---

## 3. Standard Constraint Audit Report Schema

```markdown
# Negative Constraint Audit Report

- **Target System**: `/path/to/project`
- **Audit Timestamp**: `2026-11-02T01:30:00Z`
- **Audit Status**: `BREACH_DETECTED` (1 breach, 1 rule warning)

## Discovered Violations
1. **[FORBIDDEN_PATH_TOUCH]**: Modified `/storage/emulated/0/Admin/Libraries/lib_core.py` without explicit authorization.
2. **[RULE_POSTURE_WARNING]**: Active `AGENTS.md` contains 0 negative constraint clauses.

## Mandatory Containment Actions
- [ ] Action 1: Immediately revert `/storage/emulated/0/Admin/Libraries/lib_core.py` to baseline.
- [ ] Action 2: Inject defensive boundary clauses into `AGENTS.md`.
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to execute negative constraint audits, always mandate `--sandbox` containment and deterministic exit codes (`0` = Clean / Full Compliance, `10` = Path Failure, `20` = Env Failure, `30` = Violations Detected):

```bash
python3 scripts/audit_constraint_tool.py --target "." --report
```

---

## When NOT to Use

Do NOT use `audit-constraint-auditor` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing positive deliverables against declared session goals**: Redirect immediately to `audit-deviation-auditor`.
- **Pre-flight dependency and environment readiness verification**: Redirect immediately to `audit-readiness-auditor`.
- **Real-time execution blocking with interactive override gateways**: Redirect immediately to `goal-drift-auditor`.
- **Scanning files and transcripts for leaked API tokens**: Redirect immediately to `policy-secrets-leak-auditor`.
- **Multi-phase audit workflow orchestration**: Redirect immediately to `audit-domain-coordinator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
