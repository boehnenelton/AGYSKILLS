# Reference: Canonical Negative Constraint Catalog & Breach Severity

- **Version**: 100
- **Policy Anchor**: Policy §1.2, Policy §6.1, Policy §7.3
- **Author**: Elton Boehnen

---

## 1. Canonical System Negative Constraints

In the Elton Boehnen development ecosystem, the following boundaries represent strict negative constraints:

| Code | Invariant Target | Rule Formulation | Breach Severity | Auto-Action |
| :--- | :--- | :--- | :--- | :--- |
| **NC-001** | `$ADMIN_LIBRARIES` | Never modify stable or development libraries without explicit user instruction. | CRITICAL | Git revert |
| **NC-002** | `GEMINI.md` | Never edit `~/.gemini/GEMINI.md` unless explicitly instructed or executing urgent jobs. | CRITICAL | Restore backup |
| **NC-003** | Single-Letter Vars | Single-letter (`i, j, x, d, p`) and cryptic variables are strictly prohibited in application logic. | HIGH | Code refactor |
| **NC-004** | Project_GUID | Never auto-generate or assign a global `Project_GUID` without registration tooling. | HIGH | Restore placeholder |
| **NC-005** | Raw Indexing | Never use positional `row[i]` indexing; mandatory O(1) field map caching. | HIGH | Refactor to field map |
| **NC-006** | Out-of-Scope Files | Never refactor files adjacent to the requested task (surgical scope rule). | MEDIUM | Revert unrequested |

---

## 2. Rule File Posture Standards

When evaluating `AGENTS.md` or `SKILL.md` for negative boundary integrity:
1. **Minimum Ratio**: Every ruleset must contain at least 2 explicit negative constraints ("DO NOT", "Never", "Prohibited") per 5 positive rules.
2. **Mutual Disambiguation**: Every skill manifest must contain explicit "Do NOT use for..." routing pointers.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
