# Contradiction Audit Worksheet Template

Use this structured worksheet when executing the six-pass policy audit.

## Pass 1: Extraction Table

| Rule ID | Verbatim Policy Text | Candidate Scope | Operational Condition | Raw Priority |
| :--- | :--- | :--- | :--- | :--- |
| POL-001 | | | | |
| POL-002 | | | | |
| POL-003 | | | | |

## Pass 2: Normalization Registry

Format: `IF [Condition] AND [Scope] THEN [Requirement] UNLESS [Exception]`

- **POL-001**: `IF [default] AND [all scripts] THEN [MUST resolve path dynamically] UNLESS [none]`
- **POL-002**: `IF [default] AND [configuration files] THEN [MUST store beside script] UNLESS [production]`
- **POL-003**: `IF [production deployment] AND [configuration files] THEN [MUST store in /etc/app] UNLESS [none]`

## Pass 3: Pairwise Collision Matrix

| Rule ID | POL-001 | POL-002 | POL-003 | POL-004 | Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **POL-001** | - | ✓ | ✓ | ? | |
| **POL-002** | ✓ | - | ✓ (Cond) | X | |
| **POL-003** | ✓ | ✓ (Cond) | - | ✓ | |
| **POL-004** | ? | X | ✓ | - | Requires investigation |

Legend:
- `-` : Self-comparison
- `✓` : Compatible or conditionally disjoint
- `?` : Ambiguous relationship or undefined precedence
- `X` : Definite conflict requiring resolution

## Pass 4: Redundancy and Subsumption Log

| Candidate Rule ID | Subsumed By / Duplicate Of | Overlap Details | Action (Merge / Retain / Prune) |
| :--- | :--- | :--- | :--- |
| | | | |

## Pass 5: Scenario Testing Probes

### Probe Scenario A: [Title]
- **Operational Context**: [Concrete state and input]
- **Activated Rules**: [List IDs, e.g. POL-002, POL-003]
- **Evaluated Outcome**: [Deterministic result or collision point]
- **Resolution Verdict**: [Deterministic / Ambiguous]

### Probe Scenario B: [Title]
- **Operational Context**:
- **Activated Rules**:
- **Evaluated Outcome**:
- **Resolution Verdict**:

## Pass 6: Exception Registry and Precedence Map

### Centralized Exception Registry

| Exception ID | General Rule ID | Overriding Rule ID | Applied Condition | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| EX-001 | POL-010 | POL-042 | Assignment report generation | Specialized storage path |
| EX-002 | POL-014 | POL-028 | Production deployment | Security hardening |

### Authority Precedence Hierarchy

1. Safety and platform non-negotiable boundaries (Tier 100)
2. Current explicit user instruction (Tier 90)
3. Policy exception registry entries (Tier 80)
4. Specific domain rules (Tier 70)
5. General baseline rules (Tier 50)
6. Preferences and stylistic defaults (Tier 30)
7. Illustrative examples and non-normative commentary (Tier 10)
