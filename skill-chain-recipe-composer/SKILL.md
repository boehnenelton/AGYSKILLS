---
name: skill-chain-recipe-composer
description: Conceptualize, structure, and compose end-to-end skill chain recipes across the 6-tier architecture to reach desired outcomes. Evaluates target objectives against user preference for either utilizing existing installed skills or conceptualizing missing greenfield skills needed for the pipeline. When new skills are needed, defines their functional boundaries, architectural layers, and input-output contracts. Formulates standardized markdown recipe blueprints complete with skill dependency ledgers, pipeline DAG topologies, stage-by-stage handoff contracts, and execution directives for skill-chain-coordinator. Use when designing multi-skill workflows, creating skill chain recipes, ideating missing pipeline skills, or structuring end-to-end process blueprints. Do NOT use for executing recipes (use skill-chain-coordinator), multi-turn pre-planning delays (use planning-schema-planner), or authoring raw skill files (use skill-creator or skill-architect).
---

# Skill Chain Recipe Composer

A systematic architectural engine for conceptualizing, designing, and structuring multi-task skill chain recipes to achieve complex end outcomes across the 6-tier architecture. Evaluates incoming project goals against user preference to either assemble recipes from existing installed skills or conceptualize missing greenfield skills needed to complete the pipeline.

## Summary

`skill-chain-recipe-composer` operates as the recipe designer and pipeline architect for the ecosystem. While `skill-chain-coordinator` executes established multi-skill workflows, `skill-chain-recipe-composer` creates the blueprint recipes that guide execution. It evaluates the user's desired outcome, conducts a capability gap analysis against installed skills, and either stitches together existing capabilities or conceptualizes new specialized skills with defined layer positions and input-output contracts. Every recipe is produced using the standard Markdown Recipe Blueprint template, ensuring complete predictability and verifiable handoffs across stages.

## When to Use

- Designing or conceptualizing a new multi-task skill chain recipe to achieve a specific target deliverable.
- Evaluating a complex goal to determine whether existing installed skills can fulfill it or if greenfield skills must be invented.
- Conceptualizing new candidate skills needed for a pipeline, defining their naming, layer tier, and handoff contracts.
- Formatting standardized markdown recipe blueprints for execution by `skill-chain-coordinator`.
- Creating reproducible workflows for recurring processes like UI refactoring, documentation publishing, or database migration.

## When NOT to Use

- Executing an established recipe or orchestrating active runtime handoffs (use `skill-chain-coordinator`).
- Managing multi-turn conversational pre-planning turn delays (use `planning-schema-planner`).
- Authoring, linting, or saving the actual executable `SKILL.md` code files for new skills (use `skill-creator` or `skill-architect`).
- Decomposing monolithic codebases across class hierarchies (use `arch-layered-refactor`).
- Executing single tasks sequentially in JobMaker BEJSON registries (use `job-workflow-manager`).

## Core Invariants: The Recipe Composition Laws

Every composed recipe must adhere to five foundational laws:

1. **Explicit Preference Adherence**:
   - The composer must strictly honor the user's preference mode:
     - **Mode A (Ecosystem-Restricted)**: Assemble the recipe exclusively using currently installed skills. If a gap exists, adapt existing skills or alert the user.
     - **Mode B (Greenfield-Expansion)**: When existing skills are insufficient or when requested by the user, conceptualize the missing candidate skills, specify their roles, and schedule them for creation.
2. **Deterministic Stage Gates**:
   - Every stage in the recipe must define an explicit input artifact, a discrete transformation, a concrete output artifact, and a verifiable validation criteria before handoff.
3. **Layer Directionality (6-Tier Hierarchy)**:
   - Pipeline stages must respect architectural boundaries. Dependencies flow forward from foundational substrates (Layer 1) through engines (Layer 2), scaffolds (Layer 3), and UI (Layer 4) up to system architects (Layer 5) and coordinators (Layer 6).
4. **Context-Window Preservation**:
   - Intermediate handoff artifacts must be self-contained semantic packages, never ambiguous snippets requiring human guesswork.
5. **Standardized Blueprint Output**:
   - All recipes must be generated matching the authoritative Markdown Recipe Template format.

## Recipe Conceptualization Modes

### Mode 1: Existing Skills Assembly
Use when the user wants to accomplish a goal with their current skill inventory.
- Inspects installed skills across Layers 1 through 6.
- Chains matching skills into a logical Directed Acyclic Graph (DAG).
- Ensures data emitted by Skill S_i matches the expected input schema of Skill S_{i+1}.

### Mode 2: Greenfield Skill Conceptualization
Use when the user wants an optimal pipeline and invites new skill ideation.
- Identifies missing capabilities in the chain (e.g. specialized parsers, custom exporters, or visualizers).
- For each missing skill, conceptualizes:
  1. Canonical Name: Following the `[Domain]-[Subdomain]-[FunctionalSuffix]` standard.
  2. Architectural Tier: Assigning Layer 1 through Layer 6.
  3. Input/Output Contract: Defining exact input artifacts and output schemas.
  4. Core Responsibility: Summarizing the specific job of the skill.
  5. Sibling Negative Guardrails: Defining what the skill should NOT do.
- Prepares the conceptualized skills for creation via `skill-architect` or `skill-creator`.

## Step-by-Step Recipe Formulation Workflow

Follow this 5-step workflow when composing a skill recipe:

### Step 1: Goal Deconstruction and Target Deliverable

Clarify the target outcome, required file types, and quality criteria (e.g. production static site, refactored data taxonomy, compiled documentation suite).

### Step 2: Capability Gap Analysis

Evaluate available tools and installed skills against the requirements:
- Identify steps directly supported by existing skills.
- Flag missing capabilities and determine if Mode A (adapt existing) or Mode B (conceptualize greenfield) applies based on user guidance.

### Step 3: Pipeline Topology Design

Construct the sequential execution pipeline:
- Determine if the flow is linear (Stage 1 -> Stage 2 -> Stage 3) or branching (parallel data extraction merging into a single compiler).
- Assign an existing or conceptualized skill to every stage.

### Step 4: Handoff Contract Specification

For each stage boundary (S_i -> S_{i+1}), define:
- Artifact format and path (e.g. `.bejson`, `.md`, `.html`, `.zip`).
- Invariant schema requirements (e.g. zero backend keys, column 0 primary key).
- Verifiable gate check criteria (e.g. linter pass, 100% field coverage).

### Step 5: Recipe Blueprint Generation

Compile the complete plan into the standard Markdown Recipe Template.

## Standard Markdown Recipe Template

All composed recipes must output matching this structure:

```markdown
# Skill Chain Recipe: [Recipe Title]
**Standard**: BEJSON / BEHTML Ecosystem Pipeline Contract  
**Architect**: Elton Boehnen Ecosystem Standards  
**Release**: Release_Version 300  
**Status**: ACTIVE // SPECIFICATION  

---

## 1. Executive Summary & Objective

- **Target Outcome**: [Concise description of the final deliverable and goal.]
- **Strategy & Methodology**: [Explanation of how chaining skills achieves the outcome.]
- **Execution Mode**: [Single-turn pipeline execution via skill-chain-coordinator.]
- **Total Stages**: [N Stages]

---

## 2. Skill Inventory & Dependency Ledger

| Stage # | Skill Identifier | Architectural Layer | Status | Input Artifact | Output Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Stage 1** | `[skill-name-1]` | Layer [1-6] | [Installed / Greenfield] | `[initial_input]` | `[artifact_1]` |
| **Stage 2** | `[skill-name-2]` | Layer [1-6] | [Installed / Greenfield] | `[artifact_1]` | `[artifact_2]` |
| **Stage N** | `[skill-name-n]` | Layer [1-6] | [Installed / Greenfield] | `[artifact_n-1]` | `[final_deliverable]` |

---

## 3. Pipeline Topology & Data Flow Graph

```text
[Initial User Input]
  │
  ▼
1. [skill-name-1] (Layer [X])
  │  └─ Output: [artifact_1]
  ▼
2. [skill-name-2] (Layer [X])
  │  └─ Output: [artifact_2]
  ▼
N. [skill-name-n] (Layer [X])
  │  └─ Output: [final_deliverable]
  ▼
[Verified Final Outcome]
```

---

## 4. Stage-by-Stage Handoff Specifications

### Stage 1: [Stage Name]
- **Executing Skill**: `[skill-name-1]`
- **Input Contract**: [Required source files, parameters, or prompt]
- **Core Transformation**: [Operations performed by this skill]
- **Handoff Artifact**: `[Path / filename / format]`
- **Stage Gate Check**: [Validation rule before advancing]

### Stage 2: [Stage Name]
- **Executing Skill**: `[skill-name-2]`
- **Input Contract**: Consumes `[artifact_1]` from Stage 1
- **Core Transformation**: [Operations performed by this skill]
- **Handoff Artifact**: `[Path / filename / format]`
- **Stage Gate Check**: [Validation rule before advancing]

---

## 5. Execution Directive for `skill-chain-coordinator`

To execute this recipe, trigger `skill-chain-coordinator` with:

```text
"Use skill-chain-coordinator to execute the [Recipe Title] recipe:
 1. Stage 1: Execute [skill-name-1] on [initial_input] to produce [artifact_1].
 2. Stage 2: Execute [skill-name-2] on [artifact_1] to produce [artifact_2].
 ...
 Assert zero contract drift at each stage gate before advancing."
```

---

## 6. Failure Modes & Remediation

| Failure Point | Root Cause Indicator | Remediation Action |
| :--- | :--- | :--- |
| **Stage Gate Break** | [Format mismatch / invalid schema] | Halt pipeline; repair upstream output before continuing. |
| **Missing Dependency** | [Greenfield skill not yet created] | Invoke skill-creator or skill-architect to draft the skill. |
```

## Gotchas and Anti-Patterns

- **Unbounded Greenfield Sprawl**: Do not invent new skills when an existing installed skill already handles 90% of the job. Only conceptualize greenfield skills when there is a genuine functional void.
- **Vague Handoff Contracts**: Never define a handoff as simply "data" or "info". Always specify the file path, serialization format, and schema expectations.
- **Skipping the Preference Check**: Always verify whether the user wants to stick to existing skills or expand into newly conceptualized skills.
- **Neglecting Layer Directionality**: Never design a pipeline where a presentation skill feeds raw input directly into a low-level substrate without an architectural or validation bridge.
