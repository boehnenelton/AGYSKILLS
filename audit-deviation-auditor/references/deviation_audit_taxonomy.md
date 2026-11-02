# Reference: Goal Deviation Audit Taxonomy & Recovery Matrix

- **Version**: 100
- **Policy Anchor**: Policy §7.2 (Goal-Driven Execution), Policy §1.2 (Override Protocol)
- **Author**: Elton Boehnen

---

## 1. Deviation Classification Taxonomy

When an autonomous agent or developer executes tasks across multi-turn sessions, deviations are categorized into four canonical classes:

| Class Code | Category Token | Severity | Definition | Remediation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **DEV-001** | `OMISSION` | HIGH | A deliverable explicitly declared in the Goal Contract or instructions was never created on the physical filesystem. | Stage an immediate scaffolding task to build the missing artifact. |
| **DEV-002** | `CONSTRAINT_BREACH` | CRITICAL | An explicit negative constraint was violated (e.g., editing frozen libraries, modifying untouched directories, using banned single-letter variables). | Halt, revert the unauthorized modifications, and restore untouched baseline. |
| **DEV-003** | `FALSE_COMPLETION` | HIGH | A task or deliverable was marked complete in logs or tracking files, but verification tests fail or verification commands exit non-zero. | Reopen task status to in-progress, isolate test failure, and resolve syntax/logic bugs. |
| **DEV-004** | `SCOPE_CREEP` | MEDIUM | Files were created or refactored that were not part of the stated goal, inflating diff surface and risk. | Audit added files; prune or quarantine unrequested code if not required by core functionality. |

---

## 2. Recovery Matrix & Priority Queue

When deviations are detected during an audit pass:

1. **Phase 1 (Containment)**:
   - Identify all `CONSTRAINT_BREACH` instances.
   - If negative constraints were breached without explicit user override, trigger immediate revert of affected paths.
2. **Phase 2 (Gap Closure)**:
   - Process `OMISSION` items in order of dependency (data schemas -> core engines -> CLI tools -> tests -> documentation).
3. **Phase 3 (Verification Re-Check)**:
   - Re-run verification commands (test suites, linters, syntax checks).
   - Only transition task status to complete once exit code 0 is attained.
4. **Phase 4 (Course-Correction Report)**:
   - Persist Markdown audit summary to `reports/audits/goal_deviation_audit_<timestamp>.md`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
