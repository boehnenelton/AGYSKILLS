---
name: domain-scoped-coordinators
description: >-
  Route and orchestrate autonomous multi-agent pipelines using global_dispatcher
  and domain-scoped coordinators across Phase 1 (Goal Formulation & Gatekeeping via
  goal_setter and goal_auditor), Phase 2 (Context & Execution via global_cartography
  and domain_coordinator [domain_cartographer -> domain_generator -> domain_validator]),
  and Phase 3 (Finalization & Delivery via output_receiver [file_organization_coordinator
  -> drive_delivery]). Use when executing multi-phase autonomous agent workflows,
  domain-specific implementation pipelines, or managing iterative rework cycles.
  Do NOT use for single-skill DAG execution (use skill-chain-coordinator), authoring
  individual skill bundles (use skill-architect), or cataloging installed skill
  topologies (use skill-ecosystem-cartographer).
---

# domain-scoped-coordinators (Layer 6 Autonomous Multi-Phase Workflow Engine)

## Summary

`domain-scoped-coordinators` provides the execution engine and subagent topology for the 3-phase Antigravity Autonomous Workflow Architecture:
1. **Phase 1: Goal Formulation & Gatekeeping** (`goal_setter` -> `goal_auditor`)
2. **Phase 2: Context & Execution** (`global_cartography` -> `domain_coordinator` [`domain_cartographer` -> `domain_generator` -> `domain_validator`])
3. **Phase 3: Finalization & Delivery** (`output_receiver` [`file_organization_coordinator` -> `drive_delivery`])

`global_dispatcher` serves as the central router and state manager, managing state transitions, FAIL/PASS decision gates, and rework loops.

## When to Use

- Orchestrating complex, multi-stage software engineering tasks requiring rigorous gatekeeping upfront.
- Routing domain-specific tasks to dedicated coordinators (`bejson_coordinator`, `behtml_coordinator`, `taxonomy_coordinator`, `skills_coordinator`).
- Managing iterative rework cycles where output validation failures loop back for targeted repairs without resetting the entire session.
- Enforcing strict Phase 3 packaging and delivery standards (relative subfolder structure, integer version bumps, and project archive placement).

## When NOT to Use

- Do NOT use for basic, single-step DAG executions (use `skill-chain-coordinator`).
- Do NOT use for authoring or scaffolding a single `SKILL.md` bundle (use `skill-architect`).
- Do NOT use for indexing installed skill trigger matrices (use `skill-ecosystem-cartographer`).
- Do NOT use for low-level BEJSON CRUD operations (use `bejson-104-core` or `bejson-105-core`).

---

## 1. Architectural Topology & Subagent Roster

```
global_dispatcher (The central router and state manager)
|
| ----- [Phase 1: Goal Formulation & Gatekeeping]
| --------- goal_setter (Parses user intent into a strict, verifiable checklist)
| --------- goal_auditor (Checks: Is the goal fully defined, actionable, and scoped?)
|               └── [FAIL] -> Returns to global_dispatcher (Prompts user for clarification or resets)
|               └── [PASS] -> Locks the goal checklist and proceeds
|
| ----- [Phase 2: Context & Execution]
| --------- global_cartography (Maps existing types and definitions based on the locked goal)
|
| --------- (domain)_coordinator (Manages specific workflow)
|               | --------- (domain)_cartographer (Maps the specific project/codebase)
|               | --------- (domain)_generator (Executes the actual work)
|               | --------- (domain)_validator (Checks output against the locked goal checklist)
|                               └── [FAIL] -> Returns to global_dispatcher for a rework cycle
|                               └── [PASS] -> Proceeds to delivery
|
| ----- [Phase 3: Finalization & Delivery]
| --------- output_receiver (Formats the validated output)
|               | --------- file_organization-coordinator (Determines folder structure/names)
|               | --------- drive_delivery (Handles final file system/cloud write)
```

### Registered Subagents

- **`global_dispatcher`**: Central state machine router. Invokes phase subagents, handles failures, resets, and rework cycles.
- **`goal_setter`**: Transforms ambiguous prompt intent into numbered items with binary PASS/FAIL acceptance criteria.
- **`goal_auditor`**: Gates Phase 1. Evaluates goal completeness and scope. Emits `[FAIL]` or `[PASS]`.
- **`global_cartography`**: Maps global ecosystem types, schemas, and installed skills based on the locked checklist.
- **`domain_coordinator`**: Domain-scoped master coordinator managing `domain_cartographer`, `domain_generator`, and `domain_validator`.
  - Available domain specializations: `bejson_coordinator`, `behtml_coordinator`, `taxonomy_coordinator`, `skills_coordinator`.
- **`domain_cartographer`**: Maps codebase AST, file trees, symbols, and dependencies for the active domain.
- **`domain_generator`**: Implements solutions following Policy §6.1, §6.2, §7.1, §7.3, §8.1, and §9.1.
- **`domain_validator`**: Runs verification suites against the locked goal checklist. Emits `[FAIL]` (rework) or `[PASS]` (delivery).
- **`output_receiver`**: Formats and sanitizes validated deliverables.
- **`file_organization_coordinator`**: Enforces relative directory layout (`lib/`, `config/`, `data/`, `dev/`, `docs/`) and versioning (`Name_Case-V#-PKG#`).
- **`drive_delivery`**: Performs atomic disk writes, ZIP archiving to `$PROJECTS_ARCHIVE_ROOT`, and registration.

---

## 2. Operational Step-by-Step Procedure

### Step 1: Goal Formulation & Gatekeeping (Phase 1)
1. Send raw user request to `goal_setter` to draft a verifiable checklist.
2. Hand off draft checklist to `goal_auditor`.
3. If `goal_auditor` returns `[FAIL]`, return to `global_dispatcher`, halt, and prompt user for clarification.
4. If `goal_auditor` returns `[PASS]`, freeze the goal checklist as `locked_goal_checklist` and advance to Phase 2.

### Step 2: Context Mapping & Domain Execution (Phase 2)
1. Invoke `global_cartography` to resolve schemas, type definitions, and library dependencies.
2. Route the locked checklist and Context Dossier to the designated domain coordinator (`bejson_coordinator`, `behtml_coordinator`, etc.).
3. Domain coordinator directs `domain_cartographer` to inspect target codebase files.
4. Domain coordinator directs `domain_generator` to generate code, templates, or schemas.
5. Domain coordinator directs `domain_validator` to execute test suites and verify against `locked_goal_checklist`.
6. If `domain_validator` returns `[FAIL]`, return to `global_dispatcher` to initiate a targeted rework cycle (max 3 cycles).
7. If `domain_validator` returns `[PASS]`, advance to Phase 3.

### Step 3: Finalization & Delivery (Phase 3)
1. Route verified outputs to `output_receiver`.
2. `file_organization_coordinator` structures files into standard folders and assigns version headers with fresh `RELATIONAL_ID`.
3. `drive_delivery` executes atomic disk writes, generates archive ZIP in `$PROJECTS_ARCHIVE_ROOT`, and records completion.
4. `global_dispatcher` reports successful delivery to user.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
