---
name: job-workflow-manager
description: >-
  Create, template, manage, and sequentially execute jobs 1 task at a time adhering to Elton Boehnen's JobMaker BEJSON 104a Job Schema and 104db Registry standards. Use when creating jobs or templates, instantiating templates into fresh job schemas, tracking job states, running jobs one task at a time, injecting contextualized plans or last-task outputs, or auditing task completion. Do NOT use for general shell script scaffolding (use bejson-scaffold-bash) or full codebase layered refactoring (use arch-layered-refactor).
allowed-tools: vm_shell drive
---
# Job Workflow Manager

Authoritative framework for authoring, templating, managing, and sequentially executing multi-task jobs one task at a time based on Elton Boehnen's JobMaker BEJSON 104a Job Schema and 104db Job Registry specifications.

## Summary

Provides the complete lifecycle for jobs and templates: authoring job schemas in `jobs/*.bejson`, managing reusable recipes in `templates/*.bejson`, indexing entries via `registry.bejson` (104db), and executing jobs sequentially one task at a time. Enforces per-task embedded chunked context (`task_context`), file path references (`task_reference`), mandatory step designations (`task_mandatory`), header-level plan contextualization (`Contextualize_Plan`), sequential output pipelining (`Contextualize_Last`), and deterministic task audits.

## When to Use

- Authoring new BEJSON 104a Job Schemas or Template documents.
- Instantiating a reusable Template into a fresh Job Schema ("Save As Job Schema") with fresh task UUIDs and reset completion states.
- Maintaining the 104db `registry.bejson` entry catalog (classifying entries as `schema` vs. `template`).
- Running a job sequentially, executing exactly one task at a time in `task_order` sequence.
- Injecting global plan context into task execution via `Contextualize_Plan`.
- Pipelining prior task output into subsequent steps via `Contextualize_Last`.
- Auditing individual task deliverables (`audit_enabled`, `audit_passed`, `audit_fail_reason`).
- Inspecting or updating task completion states atomically with O(1) Field Map Caching.

## When NOT to Use

- General shell script scaffolding (use `bejson-scaffold-bash`).
- High-level code architecture pre-planning (use `planning-schema-planner` or `component-taxonomy-architect`).
- System-wide multi-layer codebase refactoring (use `arch-layered-refactor`).
- Validating raw BEJSON files against base formats (use `bejson-104-validator`).
- Generating 25-50 point feature menus from vague concepts (use `ideation-feature-composer`).

## Core Specifications & Schema Standards

### 1. The BEJSON 104a Job Schema

Every job document lives in `jobs/<slug>.bejson` (or `templates/<slug>.bejson`) and adheres strictly to BEJSON 104a:

- **Format**: `BEJSON`
- **Format_Version**: `104a`
- **Format_Creator**: `Elton Boehnen`
- **Schema_Name**: `Job Schema`
- **Schema_Version**: `1.0`
- **Records_Type**: `["JobTask"]`

#### Job Header Fields

- `Job_Goal` (string): High-level mission or deliverable description.
- `Job_Type` (string): Primary domain classification (e.g. `writing`, `coding`, `audit`, `media`).
- `Job_Subtype` (string): Sub-classification (e.g. `book`, `refactor`, `cli`, `slideshow`).
- `Contextualize_Plan` (boolean): When true, every task is injected with the overall plan scope and all task titles.
- `Contextualize_Last` (boolean): When true, every task receives the prior task's output as context.
- `Job_Complete` (boolean): Evaluates to true only when all tasks are complete.
- `Creation_Date` (string, `YYYY-MM-DD`): Date the job was created.
- `Completion_Date` (string, `YYYY-MM-DD`): Date all tasks finished (empty string while in progress).

#### The 11 Canonical Task Fields (`_JOB_FIELDS`)
1. `task_id` (string): Synthetic UUID string identifying the task.
2. `task_order` (integer): Sequential 1-indexed execution sequence.
3. `task_name` (string): Concise descriptive title of the task.
4. `task_description` (string): Detailed instructions for task execution.
5. `task_completed` (boolean): Execution status flag.
6. `audit_enabled` (boolean): Flag requiring explicit verification of task output.
7. `audit_passed` (boolean): Result of audit verification.
8. `audit_fail_reason` (string): Explanatory reason if audit failed, or empty string.
9. `task_context` (array): Embedded file chunk objects formatted Doc_Chunker-style (`{ref, text_based, chunks: [{chunk_id, chunk_label, chunk_content, chunk_index_pos, chunk_status}]}`).
10. `task_reference` (array): List of file path strings to consult during execution.
11. `task_mandatory` (boolean): Marks task as a required built-in step for that `Job_Type`/`Job_Subtype`.

### 2. The 104db Job Registry Schema (`registry.bejson`)

Tracks every saved entry and classifies it as a Job Schema or Template:

- **Format**: `BEJSON`
- **Format_Version**: `104db`
- **Format_Creator**: `Elton Boehnen`
- **Schema_Name**: `Job Registry Schema`
- **Records_Type**: `["JobRegistryEntry"]`
- **Fields**:
  1. `entry_id` (string): Synthetic UUID string.
  2. `entry_name` (string): Display name.
  3. `entry_slug` (string): Filesystem-safe snake_case name.
  4. `entry_type` (string): Strictly `"schema"` or `"template"`.
  5. `file_path` (string): Relative path from project root (`jobs/<slug>.bejson` or `templates/<slug>.bejson`).
  6. `created_date` (string): `YYYY-MM-DD`.
  7. `modified_date` (string): `YYYY-MM-DD`.

## Job Creation & Templating Lifecycle

### 1. Authoring a Fresh Job
1. Define the job header: `Job_Goal`, `Job_Type`, `Job_Subtype`, `Contextualize_Plan`, and `Contextualize_Last`.
2. Construct task rows with sequential `task_order` (1, 2, 3...).
3. Attach file path strings to `task_reference`.
4. Attach Doc_Chunker paragraph-split chunk arrays to `task_context` for text assets.
5. Save to `jobs/<slug>.bejson` and upsert a `"schema"` row in `registry.bejson`.

### 2. Authoring a Reusable Template
1. Follow the exact same document structure as a Job Schema.
2. Flag required structural steps as `task_mandatory = true`.
3. Save to `templates/<slug>.bejson` and record an entry with `entry_type = "template"` in `registry.bejson`.

### 3. Template Instantiation ("Save As Job Schema")
When generating an actionable job from a template:
1. Load the template document from `templates/<slug>.bejson`.
2. Clear `task_id` on each task (generate fresh synthetic UUIDs).
3. Reset `task_completed = false` and `audit_passed = false` on every task.
4. Preserve `task_context`, `task_reference`, and `task_mandatory` untouched.
5. Assign a new job name and save to `jobs/<new_slug>.bejson`.
6. Register the new job in `registry.bejson` with `entry_type = "schema"`.

## Running Jobs 1 Task at a Time (Execution Protocol)

When executing a job, always proceed sequentially through this strict five-step loop:

```
Load Job Doc -> Identify Next Uncompleted Task -> Assemble Context -> Execute Task -> Audit & Atomic State Save
```

### Step 1: Identify the Active Task
1. Load the target job document using `bejson_core_load_file()`.
2. Resolve columns dynamically via Field Map Cache (`bejson_core_get_field_map()`).
3. Sort tasks by `task_order`.
4. Find the first task where `task_completed == false`. This is the **active task**.
5. If all tasks are completed, verify `Job_Complete == true`, set `Completion_Date`, and exit.

### Step 2: Assemble Multi-Source Task Context
Before dispatching or executing the active task, synthesize its execution context:
1. **Task Core Instructions**: Extract `task_name` and `task_description`.
2. **Task Context Chunks**: Read embedded chunks in `task_context` and present verbatim contents.
3. **Task References**: Verify and read files referenced in `task_reference`.
4. **Plan Contextualization (`Contextualize_Plan`)**: If `Contextualize_Plan == true` on the job header:
   - Inject the overall `Job_Goal`.
   - Inject the full enumerated list of all task names and descriptions so the executor understands the global scope.
5. **Sequential Output Pipelining (`Contextualize_Last`)**: If `Contextualize_Last == true` on the job header:
   - If `task_order > 1`, retrieve the execution output, deliverable text, or audit report of task ($task\_order - 1$) and inject it as context.

### Step 3: Execute Single Task Isolated
1. Focus exclusively on the active task's scope.
2. Do NOT execute subsequent tasks in the same step.
3. Produce the required deliverable, code change, or report.

### Step 4: Audit Verification Gate
1. Check `audit_enabled`:
   - If `audit_enabled == false`: Proceed directly to completion marking.
   - If `audit_enabled == true`: Inspect deliverable against task acceptance criteria.
2. If audit checks pass:
   - Set `audit_passed = true`.
   - Set `audit_fail_reason = ""`.
   - Set `task_completed = true`.
3. If audit checks fail:
   - Set `audit_passed = false`.
   - Record specific failure details in `audit_fail_reason`.
   - Keep `task_completed = false`.
   - Report failure and halt sequential progression until remediated.

### Step 5: Atomic State Persistence & Manifest Update
1. Update the row values in `doc["Values"]` through the cached field map.
2. Check if all tasks in the job are now complete:
   - If complete: set `Job_Complete = true` and `Completion_Date = "<today>"`.
3. Write the updated document to disk atomically (`.bejson_<pid>.tmp` -> `flush` -> `fsync` -> `os.replace`).
4. Update `modified_date` in `registry.bejson`.
5. Report task completion to the user and prompt to advance to task ($task\_order + 1$).

## Standalone CLI Runner (`scripts/job_runner.py`)

The skill bundles a self-contained execution driver in `scripts/job_runner.py`:

```bash
# List all registered jobs and templates
python3 scripts/job_runner.py --list

# Inspect next pending task for a job
python3 scripts/job_runner.py --inspect "jobs/refactor_cli.bejson"

# Step and execute exactly 1 task
python3 scripts/job_runner.py --step "jobs/refactor_cli.bejson"

# Instantiate a template into a fresh job
python3 scripts/job_runner.py --instantiate "templates/doc_pipeline.bejson" --name "Book Release Job"
```

## Gotchas & Anti-Patterns to Avoid

- **Batch Task Leaping**: Never execute multiple tasks in a single turn. Always run 1 task at a time to allow verification and proper sequential contextualization.
- **Context Loss on Instantiation**: When instantiating a template into a job, never discard `task_context` or `task_reference`. Only clear `task_id`, `task_completed`, and `audit_passed`.
- **Hardcoding Column Offsets**: Never read or write task fields using literal indices (e.g. `row[4]`). Always resolve offsets dynamically through `bejson_core_get_field_map()`.
- **Ignoring Contextualize Flags**: If `Contextualize_Last` is enabled, the executor must receive the previous task's output. Bypassing this causes downstream tasks to lose continuity.
- **Direct File Mutation**: Never overwrite `.bejson` files directly. Always stage changes in a `.tmp` file and perform an atomic swap with fsync fallback.
