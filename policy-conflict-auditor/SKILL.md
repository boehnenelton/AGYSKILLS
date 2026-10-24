---
name: policy-conflict-auditor
description: >-
  Audit technical policies, guidelines, directives, and system prompts by treating them as deterministic rule systems. Extracts atomic rules, normalizes conditions, maps pairwise conflict matrices, detects direct and indirect contradictions, eliminates redundant constraints, and establishes explicit precedence hierarchies. Use when auditing long policies, hunting contradictions or ambiguities, reviewing specifications, resolving competing rules, or establishing exception registries. Do NOT use for BEJSON validation (use bejson-104-validator), BEHTML validation (use behtml-schema-validator), multi-layer code refactoring (use arch-layered-refactor), prompt placeholder templating (use prompt-placeholder-composer), or authoring skills (use skill-architect).
---

# Policy Conflict Auditor

Systematic auditing framework for analyzing technical policies, system instructions, specifications, and operational directives as deterministic rule systems. Extracts atomic constraints, builds pairwise conflict matrices, exposes hidden or indirect contradictions, prunes redundant rules, and establishes explicit precedence hierarchies and centralized exception registries.

## Summary

Translates complex, ambiguous, or overlapping technical policies and operational directives into deterministic rule systems. Decomposes unstructured prose into atomic rule models, builds collision matrices, surfaces hidden contradictions, eliminates redundancies, and generates clear precedence hierarchies and exception registries to ensure deterministic execution.

## When to Use

- Auditing complex policies, engineering standards, or architectural guidelines for internal consistency.
- Hunting down hidden contradictions, circular overrides, or undefined priority conflicts in instruction sets.
- Identifying and eliminating redundant, duplicate, or subsumed policy statements.
- Normalizing loose policy prose into structured IF-AND-THEN-UNLESS conditional logic.
- Building explicit conflict matrices and centralized exception registries for AI-facing directives.
- Resolving multi-constraint ambiguities through scenario testing before execution.

## When NOT to Use

- Validating BEJSON data structures or files (use `bejson-104-validator`).
- Validating spatial BEHTML layouts, grids, or DOM coordinates (use `behtml-schema-validator`).
- Decomposing monolithic codebases into 6-tier architectures (use `arch-layered-refactor`).
- Composing dynamic prompt templates with placeholder variables (use `prompt-placeholder-composer`).
- Designing or authoring new Gemini Spark skills (use `skill-architect`).
- Managing linear job tasks and task state machines (use `job-workflow-manager`).

## Core Architecture and Rule Model

### 1. The Four-Attribute Atomic Rule Model

Every policy requirement must be decomposed into an atomic tuple:

- **ID**: Stable unique identifier (`POL-001`, `POL-002`, `R-001`).
- **Scope**: The target entity, artifact, or domain where the rule applies (e.g. all scripts, assignment reports, API endpoints).
- **Trigger / Condition**: Specific operational state or prerequisite under which the rule activates (e.g. always, default, production deployments).
- **Requirement**: Mandatory normative action or state demanded (MUST / MUST NOT).
- **Priority**: Hierarchical tier of authority (Safety, Instruction, Exception, Specific, General, Preference).

A formal contradiction exists if and only if two rules share the same scope and same active conditions while demanding incompatible required outcomes:

`Conflict = Same Scope + Same Active Conditions + Incompatible Outcomes`

### 2. Normative vs Explanatory Language

Enforce strict RFC 2119 keyword semantics:

- `MUST` / `REQUIRED`: Absolute mandatory requirement.
- `MUST NOT` / `FORBIDDEN`: Absolute prohibition.
- `SHOULD` / `RECOMMENDED`: Required unless a documented exception exists.
- `SHOULD NOT`: Prohibited unless a documented exception exists.
- `MAY` / `OPTIONAL`: Permitted discretion; non-binding.
- `RATIONALE` / `EXAMPLE`: Explanatory commentary. Never interpret rationale as normative obligation.

### 3. Absolute Language Watchlist

Flags all occurrences of absolute terms for elevated scrutiny: `always`, `never`, `must`, `must not`, `only`, `exactly`, `all`, `none`, `required`, `forbidden`, `except`, `unless`, `regardless`, `under no circumstances`.

### 4. Seven-Tier Hierarchy of Authority

When two applicable rules collide, resolve priority by strict authority tier (higher rank overrides lower rank):

1. **Tier 1 (Priority 100) - Safety and Platform Constraints**: Hard sandbox, security, non-negotiable boundaries. Cannot be overridden.
2. **Tier 2 (Priority 90) - Explicit Current User Instruction**: Real-time direct request from user for current task.
3. **Tier 3 (Priority 80) - Explicit Policy Exceptions**: Deliberate, documented exemptions in the policy exception registry.
4. **Tier 4 (Priority 70) - Specific Domain Rules**: Narrow scope, detailed domain-specific requirements.
5. **Tier 5 (Priority 50) - General Baseline Rules**: Broad system defaults and overarching principles.
6. **Tier 6 (Priority 30) - Preferences and Recommendations**: Desired style or default suggestions (`SHOULD`).
7. **Tier 7 (Priority 10) - Illustrative Examples and Commentary**: Non-normative demonstrations.

Precedence Rule: Specificity Rule. If two colliding rules occupy the exact same authority tier, the rule with the narrower, more specific scope overrides the rule with the broader general scope. Document order is non-semantic.

## The Six-Pass Contradiction Audit Workflow

### Pass 1: Extraction

Scan the document linearly. Isolate every normative requirement from surrounding explanatory prose. Assign a stable ID (`POL-xxx`) and record:

- Original verbatim text
- Assigned ID
- Candidate scope
- Initial condition and priority level

### Pass 2: Normalization

Convert every extracted rule into standard conditional logic:

`IF [Condition] AND [Scope] THEN [Requirement] UNLESS [Exception]`

Normalize terms so identical scopes and actions use identical keywords across all rules.

### Pass 3: Relationship Classification and Collision Matrix

Compare extracted rules pairwise. Classify each pair into one of five relationship types:

- **Type A (Compatible)**: Both rules can be satisfied simultaneously without mutual interference.
- **Type B (Conditional)**: Rules demand differing outcomes but activate under disjoint conditions. No conflict.
- **Type C (Overlapping / Specific)**: Both apply, but one specifies additive constraints or narrower specialization.
- **Type D (Direct Contradiction)**: Both rules apply under identical scope and conditions, but demand mutually impossible outcomes.
- **Type E (Priority Conflict)**: Both rules apply, but the policy fails to establish which one takes precedence.

Construct an NxN pairwise Conflict Matrix for all intersecting rules:

- `-` : Self-comparison
- `✓` : Compatible or conditionally disjoint
- `?` : Ambiguous or priority-unresolved
- `X` : Definite contradiction or collision

Focus deep inspection exclusively on `X` and `?` intersections.

### Pass 4: Redundancy and Subsumption Pruning

Inspect all `✓` and Type C pairs for unnecessary bloat:

- **Exact Redundancy**: Identical requirements stated across multiple sections under the same conditions.
- **Subsumption**: A broader rule completely encompasses a weaker rule with zero additional constraint value.
- Consolidate duplicates into a single canonical rule ID and record cross-references.

### Pass 5: Scenario Testing

Stress-test identified ambiguities and rules with concrete operational probe scenarios:

- Construct 3 to 5 realistic edge-case scenarios where multiple rules activate simultaneously.
- Verify whether the policy produces an unambiguous, deterministic outcome for every scenario.
- Identify indirect contradictions (e.g. file retention vs immediate deletion, required metadata on unversioned temporary files).

### Pass 6: Resolution, Exception Registry, and Restructuring

Resolve every detected conflict using one of seven deterministic remedies:

- **Remedy 1: Merge**: Combine overlapping rules into a single unified specification.
- **Remedy 2: Narrow Scope**: Restrict one rule to eliminate the intersection.
- **Remedy 3: Add Explicit Condition**: Clarify the exact operational trigger for each rule.
- **Remedy 4: Create Exception**: Log an explicit entry in the Centralized Exception Registry.
- **Remedy 5: Establish Precedence**: Explicitly declare which rule overrides the other.
- **Remedy 6: Deprecate / Remove**: Eliminate obsolete, superseded, or contradictory legacy rules.
- **Remedy 7: Escalate Decision**: If semantic ambiguity remains, surface the exact conflict to the policy author.

Assemble the Centralized Exception Registry:

`| Exception ID | General Rule ID | Overriding Rule ID | Applied Condition | Rationale |`

Restructure the policy following the 12-section architecture:

1. Policy Identity
2. Definitions
3. Authority and Precedence
4. Non-Negotiable Hard Constraints
5. General Rules
6. Specific Rules
7. Exception Registry
8. Workflows
9. Validation
10. Failure/Ambiguity Protocols
11. Non-Normative Examples
12. Changelog

## Runtime Precedence Algorithm

For autonomous execution when evaluating conflicting instructions:

1. Identify all candidate rules applicable to the target action.
2. Filter out rules whose conditions or triggers are not met.
3. Classify remaining active rules across the 7-tier authority hierarchy.
4. Detect incompatible requirements among active rules.
5. If no incompatibility exists: execute all active rules.
6. If conflict exists: select the highest-tier authority rule.
7. If authority tiers are tied: apply the more specific rule over the general rule.
8. If specificity is tied: check for an explicit exception or override declaration.
9. If ambiguity remains unresolved: halt immediately without guessing; report conflicting rule IDs and request clarification.
10. Pre-execution audit: confirm the proposed action violates no higher-priority constraint.

## Gotchas and Anti-Patterns

- **Linear Prose Trap**: Do not attempt to spot contradictions by reading prose front to back. Always extract and normalize into atomic rules first.
- **False Positive Exceptions**: Do not mark conditional differences as contradictions. Differentiate between conflicting conditions versus conflicting requirements.
- **Document Order Fallacy**: Never infer precedence from document order (e.g. later rule overrides earlier rule). Paragraph rearrangements silently corrupt logic.
- **Buried Exceptions**: Never scatter exceptions across narrative paragraphs. Always centralize exceptions in the dedicated Exception Registry.
- **Hidden Lifecycle Collisions**: Always verify temporal dependencies across create, update, archive, and delete lifecycles.
- **Silent Guessing**: An AI must never guess between equal-priority conflicting rules. Report the collision explicitly.
