---
name: audit-redundancy-planner
description: >-
  Audit systems, repositories, skill suites, and data models for code duplication,
  redundant functions, overlapping skill triggers, and unnormalized storage bloat.
  Calculates exact Jaccard similarity indices across agent triggers and hashes AST
  code chunks to synthesize a structured, phased consolidation blueprint in
  reports/audits/. Use when identifying duplicate routines, auditing skill suites
  for routing collisions and overlap, consolidating duplicate data stores, or
  refactoring copy-pasted implementations into unified shared libraries. Do NOT
  use for identifying structural coverage blind spots or missing ports (use
  audit-gap-planner), auditing deviations against stated goal contracts (use
  audit-deviation-auditor), real-time execution blocking with user override
  gateways (use goal-drift-auditor), or loop I/O efficiency audits (use
  audit-efficiency-auditor).
---

# Skill: `audit-redundancy-planner` (Layer 5 Redundancy & Consolidation Planning Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (Composition, Planning & Refactoring)`
- **Policy Anchor**: `Policy §1.3 (Code Cleanup, Discretion & Project Documentation)`
- **Embedded Tool**: [`scripts/audit_redundancy_tool.py`](./scripts/audit_redundancy_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`audit-redundancy-planner` provides automated detection and phased consolidation planning for duplicate logic, redundant data representations, and overlapping skill triggers. In evolving ecosystems, multiple modules frequently solve the same operational problem with slight variations, leading to maintenance debt and routing ambiguity.

Key analysis scopes:
1. **Source Code Duplication**: Identifies identical and near-identical AST function blocks, classes, and utility scripts across repositories.
2. **Skill Trigger Collisions**: Calculates lexical and token-level Jaccard similarity between skill positive triggers, detecting routing ambiguity.
3. **Storage & Schema Redundancy**: Identifies duplicate column definitions, unnormalized redundant stores, and unindexed tabular bloat.
4. **Consolidation Blueprints**: Emits surgical, phased migration plans that unify duplicates into shared libraries without breaking backward compatibility.

---

## 2. Four-Stage Redundancy & Consolidation Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Ingest       | --> | Stage 2: Calculate    |
| Code & Manifests      |     | Similarity & Overlap  |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Synthesize   | <-- | Stage 3: Classify     |
| Consolidation Plan    |     | Redundancy Archetypes |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Ingestion)**: Scans Python/Bash/JS source files or skill `SKILL.md` manifests.
2. **Stage 2 (Similarity Computation)**:
   - *Code Hash Match*: Exact normalized AST hash comparison for code duplicates.
   - *Jaccard Index*: Token n-gram overlap calculation across triggers ($J(A, B) = \frac{|A \cap B|}{|A \cup B|}$).
3. **Stage 3 (Archetype Classification)**:
   - *Identical Clone*: Identical logic duplicated across multiple paths.
   - *Functional Variant*: Equivalent logic with minor parameterization differences.
   - *Trigger Collision*: Skills competing for the same user intent ($J \ge 0.55$).
4. **Stage 4 (Plan Synthesis)**: Generates a phased consolidation plan output to `reports/audits/redundancy_audit_${TIMESTAMP}.md`.

---

## 3. Standard Redundancy Audit Report Schema

```markdown
# Redundancy Audit & Consolidation Blueprint

- **Target System**: `/path/to/project`
- **Audit Timestamp**: `2026-11-02T01:00:00Z`
- **Redundancy Status**: `REDUNDANCIES_DETECTED` (4 overlaps identified)

## Discovered Overlaps & Collisions
1. **[CODE_DUPLICATION]**: Function `sanitize_input()` duplicated across `src/parser.py` and `tools/util.py`.
2. **[TRIGGER_COLLISION]**: Skills `bejson-104-core` and `bejson-core` have 0.72 Jaccard trigger overlap.
3. **[STORAGE_BLOAT]**: Unnormalized user session data duplicated in both `session.json` and `cache.db`.

## Phased Consolidation Blueprint
### Phase 1: Shared Library Extraction
- [ ] Task 1.1: Extract `sanitize_input()` to shared module `lib/sanitize.py`.
- [ ] Task 1.2: Refactor `src/parser.py` and `tools/util.py` to import shared module.

### Phase 2: Skill Trigger Disambiguation
- [ ] Task 2.1: Add explicit negative constraint triggers to disambiguate routing.
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to execute redundancy audits, always mandate `--sandbox` containment and deterministic exit codes (`0` = Clean Pass / No Redundancy, `10` = Path Failure, `20` = Env Failure, `30` = Redundancies Identified):

```bash
python3 scripts/audit_redundancy_tool.py --target "." --report
```

---

## When NOT to Use

Do NOT use `audit-redundancy-planner` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Auditing structural coverage blind spots and missing ports**: Redirect immediately to `audit-gap-planner`.
- **Auditing execution deviations against declared session goal contracts**: Redirect immediately to `audit-deviation-auditor`.
- **Real-time execution blocking during active tool calls**: Redirect immediately to `goal-drift-auditor`.
- **Measuring CPU, memory, and loop I/O efficiency**: Redirect immediately to `audit-efficiency-auditor`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
