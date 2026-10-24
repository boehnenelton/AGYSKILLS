# Standardized Twelve-Section Policy Template

When rewriting or restructuring a policy to guarantee deterministic execution, adhere to this structure:

```markdown
# [POLICY TITLE]

## 01. Policy Identity
- **Policy ID**: POL-[DOMAIN]-001
- **Version**: 1.0.0
- **Effective Date**: YYYY-MM-DD
- **Scope / Applicability**: Systems, services, and codebases covered.

## 02. Definitions
- **Normative Keywords**: MUST (mandatory), MUST NOT (forbidden), SHOULD (strongly recommended), MAY (discretionary).
- **Domain Terminology**: Exact definitions of core entities.

## 03. Authority and Precedence
- **Precedence Hierarchy**:
  1. Safety and platform constraints (Tier 100)
  2. Explicit user instructions (Tier 90)
  3. Documented policy exceptions (Tier 80)
  4. Specific domain rules (Tier 70)
  5. General baseline rules (Tier 50)
  6. Preferences and defaults (Tier 30)
  7. Examples and commentary (Tier 10)
- **Conflict Resolution Law**: Narrower specific rules override broader general rules at equal tiers. Document position is non-semantic.

## 04. Non-Negotiable Hard Constraints
- Hard boundaries, security restrictions, and environment limits.

## 05. General Baseline Rules
- Broad defaults and standard operational practices across the entire domain.

## 06. Specific Domain Rules
- Granular, conditional rules for specific sub-systems, file types, or environments.

## 07. Centralized Exception Registry
| Exception ID | General Rule ID | Overriding Rule ID | Applied Condition | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| EX-001 | POL-010 | POL-042 | Under condition X | Rationale |

## 08. Workflows and Procedures
- Step-by-step sequential processes.

## 09. Validation and Verification Protocols
- Pre-execution criteria and post-execution audit commands.

## 10. Failure and Ambiguity Protocol
- Required behavior when undefined conditions or unresolved collisions occur (halt and request clarification).

## 11. Illustrative Examples
- Non-normative examples demonstrating correct implementation.

## 12. Changelog
- Version history detailing affected rule IDs and modification rationale.
```
