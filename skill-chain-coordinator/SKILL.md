---
name: skill-chain-coordinator
description: >-
  Orchestrate multi-skill Directed Acyclic Graph (DAG) execution flows, manage
  stage state transitions, delegate isolated subagent handoffs, and enforce
  deterministic Layer 2 stage gates across Layers 1 through 5 using verified
  topologies from skill-ecosystem-cartographer. Use when executing multi-stage
  skill pipelines, coordinating cross-layer schema-to-code-to-UI workflows, or
  running verified Recipe Blueprints. Do NOT use for scaffolding individual skill
  manifests (use skill-architect), cataloging installed skill registries or
  auditing trigger collisions (use skill-ecosystem-cartographer), authoring static
  recipe markdown blueprints without execution (use skill-chain-recipe-composer),
  scheduling N=K+1 conversational turn delays (use planning-schema-planner), or
  running sequential JobMaker task files (use job-workflow-manager).
---

# skill-chain-coordinator (Layer 6 Multi-Skill DAG & Subagent Orchestrator)

## Summary

`skill-chain-coordinator` is the runtime execution engine of Layer 6. It consumes the collision-free skill catalog produced by `skill-ecosystem-cartographer` (`data/skill_registry_catalog.104a.bejson`) and executes dependency-ordered multi-skill DAGs with cryptographic contract freezing, isolated subagent delegation, and deterministic stage gate verification recorded in `data/dag_pipeline_ledger.104a.bejson`.

## When to Use

- Executing end-to-end multi-skill pipelines spanning Layers 1 through 5 (e.g., `code-taxonomy-architect` -> `bejson-104-core` -> `bejson-104-validator` -> `bejson-scaffold-python`).
- Managing subagent handoffs (`invoke_subagent` / `send_message`) across read-only planning waves (`--mode=plan`) and sandboxed mutation waves (`--mode=accept-edits`).
- Enforcing Stage Gate validation checks between upstream artifact producers and downstream consumers.
- Resuming interrupted multi-stage pipelines from the last `VERIFIED` checkpoint in `data/dag_pipeline_ledger.104a.bejson`.

## When NOT to Use

- Do NOT use for authoring, scaffolding, or linting a single `SKILL.md` bundle (use `skill-architect`).
- Do NOT use for scanning skill directories or building pairwise trigger collision matrices (use `skill-ecosystem-cartographer`).
- Do NOT use for drafting a Markdown Recipe Blueprint prior to execution approval (use `skill-chain-recipe-composer`).
- Do NOT use for enforcing $N = K + 1$ multi-turn conversational pre-planning withholding before schemas/wireframes are approved (use `planning-schema-planner`).
- Do NOT use for running sequential JobMaker task files (use `job-workflow-manager`).

---

## 1. Layer Boundary & Dependency Contract

- **Assigned Skill Tier**: Layer 6 (`L6: Root Orchestration & Meta-Governance`)
- **Codebase Layer Mapping**: `L5_Composition_Root`
- **Exclusive Write-Owner Of**: `data/dag_pipeline_ledger.104a.bejson` (`DagStageExecution` entity)
- **Foreign Key Integrity**: `dag_skill_entry_fk` -> `SkillCatalogEntry.skill_entry_uuid` (`on_delete: restrict`)
- **Sandbox Policy**: All `agy` CLI invocations MUST include `--sandbox`.
- **BEJSON Access Policy**: All `.bejson` reads and mutations MUST resolve column indices dynamically via `field_map`.

---

## 2. Step-by-Step DAG Execution & Stage Gate Workflow

### Step 1: Verify Catalog & Pre-Planning Readiness
1. Load `data/skill_registry_catalog.104a.bejson` via `field_map` and verify that every stage skill has `skill_linter_verified_flag == true`.
2. If the requested workflow requires $K \ge 1$ unfrozen conversational pre-planning turns (`planning-schema`, `planning-template`), hand off to `planning-schema-planner` first.

### Step 2: Execute Topological DAG Pipeline & Stage Gates
Invoke `scripts/coordinator_dag_runner.py` to validate acyclicity (`Code 435`), execute each stage's gate validator command, compute SHA-256 handoff digests, and persist state transitions (`PENDING` -> `PREFLIGHT_CHECK` -> `DISPATCHED` -> `GATE_VALIDATING` -> `VERIFIED`) to `data/dag_pipeline_ledger.104a.bejson`:

```bash
python3 scripts/coordinator_dag_runner.py \
  --catalog "/storage/emulated/0/Documents/AGY/data/skill_registry_catalog.104a.bejson" \
  --ledger "/storage/emulated/0/Documents/AGY/data/dag_pipeline_ledger.104a.bejson" \
  --pipeline-skills "skill-architect,skill-ecosystem-cartographer"
```

### Step 3: Verify Completion Ledger
Confirm `Exit Code 0` and verify that all rows in `data/dag_pipeline_ledger.104a.bejson` report `dag_stage_lifecycle_state == "VERIFIED"` and `dag_contract_frozen_flag == true`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
