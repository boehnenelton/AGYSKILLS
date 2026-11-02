---
name: job-template-composer
description: >-
  Compose, structure, and parameterize reusable JobMaker BEJSON 104a job templates
  and execution task sequences from natural language goals, project roadmaps, and
  refactoring plans. Enforces contextualization flags (Contextualize_Plan,
  Contextualize_Last), 11-field task schemas, synthetic UUIDs, and sequential
  task ordering ready for execution. Use when generating new JobMaker job schemas,
  authoring reusable task templates in templates/*.bejson, breaking down complex
  development missions into structured task DAGs, or parameterizing multi-step
  workflows. Do NOT use for autonomous multi-job lifecycle orchestration (use
  job-lifecycle-coordinator), validating job schema conformity (use
  job-conformance-validator), executing tasks sequentially (use
  job-workflow-manager), or composing raw feature menus (use
  ideation-feature-composer).
---

# Skill: `job-template-composer` (Layer 5 JobMaker 104a Template & DAG Composition Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (Composition, Planning & Refactoring)`
- **Policy Anchor**: `Policy §7.2 (Goal-Driven Execution), Policy §6.2 (BEJSON Core Mandate)`
- **Embedded Tool**: [`scripts/job_template_tool.py`](./scripts/job_template_tool.py)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Core Mission

`job-template-composer` translates abstract technical goals, project specifications, and multi-turn refactoring roadmaps into deterministic, machine-executable **JobMaker BEJSON 104a** documents. Rather than writing ad-hoc, unstructured markdown checklists, this skill composes structured task DAGs with explicit file reference pointers, synthetic UUIDs, contextualization flags, and audit criteria.

---

## 2. Four-Stage Job Composition Pipeline

```text
+-----------------------+     +-----------------------+
| Stage 1: Decompose    | --> | Stage 2: Sequence &   |
| Goal & Scope          |     | Dependency Assignment |
+-----------------------+     +-----------------------+
                                          |
                                          v
+-----------------------+     +-----------------------+
| Stage 4: Serialize    | <-- | Stage 3: Inject Audit |
| BEJSON 104a Schema    |     | Criteria & Context    |
+-----------------------+     +-----------------------+
```

1. **Stage 1 (Goal Decomposition)**: Analyzes project requirements into discrete, atomic tasks adhering to the **1-Action-per-Task Law**.
2. **Stage 2 (Sequencing)**: Assigns 1-indexed contiguous `task_order` integers, synthetic UUIDv4 `task_id` strings, and mandatory designations.
3. **Stage 3 (Context & Audit Formulation)**: Configures `Contextualize_Plan` and `Contextualize_Last` headers, declares `task_reference` file targets, and defines clear pass/fail audit expectations.
4. **Stage 4 (Serialization)**: Emits a strictly conforming BEJSON 104a document to `jobs/<slug>.bejson` or `templates/<slug>.bejson`.

---

## 3. Exemplar Composed JobMaker Document

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Schema_Name": "Job Schema",
  "Schema_Version": "1.0",
  "Records_Type": ["JobTask"],
  "Job_Goal": "Refactor authentication middleware to use pointer-only credentials",
  "Job_Type": "coding",
  "Job_Subtype": "refactor",
  "Contextualize_Plan": true,
  "Contextualize_Last": true,
  "Job_Complete": false,
  "Creation_Date": "2026-11-02",
  "Completion_Date": "",
  "Fields": [
    {"name": "task_id", "type": "string"},
    {"name": "task_order", "type": "integer"},
    {"name": "task_title", "type": "string"},
    {"name": "task_description", "type": "string"},
    {"name": "task_context", "type": "string"},
    {"name": "task_reference", "type": "string"},
    {"name": "task_mandatory", "type": "boolean"},
    {"name": "is_completed", "type": "boolean"},
    {"name": "audit_enabled", "type": "boolean"},
    {"name": "audit_passed", "type": "boolean"},
    {"name": "audit_fail_reason", "type": "string"}
  ],
  "Values": [
    ["task_auth_001", 1, "Audit Current Auth Endpoints", "Scan src/auth.py for hardcoded tokens", "", "src/auth.py", true, false, true, null, ""],
    ["task_auth_002", 2, "Implement Pointer Resolution", "Update auth logic to source ENV:<var_name>", "", "src/auth.py", true, false, true, null, ""]
  ]
}
```

---

## 4. Execution & Containment Contract (Level 3 Guardrail)

When invoking subagents to compose job templates, always mandate `--sandbox` containment and deterministic exit codes (`0` = Clean Composition, `10` = Path Failure, `20` = Env Failure, `30` = Composition Error):

```bash
python3 scripts/job_template_tool.py --goal "Migrate database" --tasks "Audit schema,Scaffold tables,Run migration" --output "jobs/migrate.bejson"
```

---

## When NOT to Use

Do NOT use `job-template-composer` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Autonomous multi-job lifecycle orchestration and folder sweeps**: Redirect immediately to `job-lifecycle-coordinator`.
- **Validating job schema conformity and invariant gates**: Redirect immediately to `job-conformance-validator`.
- **Executing tasks sequentially one task at a time**: Redirect immediately to `job-workflow-manager`.
- **Generating 25-50 point brainstorming feature menus**: Redirect immediately to `ideation-feature-composer`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
