---
name: skill-architect
description: >-
  Design, scaffold, validate, and register multi-tier Antigravity CLI (agy) agent
  skills enforcing the 6-Tier Layered Skill Architecture (L1-L6), unidirectional
  downward dependencies, 3-stage progressive disclosure, O(1) BEJSON field map
  caching, and 3-level mutual negative constraint triggers. Use when authoring
  new SKILL.md bundles, defining skill directory topologies, scaffolding layer-specific
  reference shards or black-box validator scripts, or auditing skill manifests for
  routing collisions. Do NOT use for executing multi-skill DAG workflows (use
  skill-chain-coordinator), mapping or cataloging installed ecosystem routing
  topologies (use skill-ecosystem-cartographer), composing multi-skill recipe
  blueprints (use skill-chain-recipe-composer), or decomposing monolithic
  application source code (use arch-layered-refactor).
---

# skill-architect (Layer 6 Meta-Governance & Skill Scaffolder)

## Summary

`skill-architect` is the canonical Layer 6 meta-skill for engineering, scaffolding, and validating downstream skills within the Google Antigravity CLI (`agy`) 6-Tier Layered Skill Architecture. It enforces strict structural isomorphism between the Skill Ecosystem Hierarchy (`L1` to `L6`) and the Application Codebase Hierarchy (`L0` to `L5`), deterministic relational naming, pairwise disjoint negative constraint triggers, and 3-stage progressive disclosure token budgets.

## When to Use

- Designing and scaffolding a new Antigravity skill bundle (`SKILL.md`, `references/`, `scripts/`, `assets/`) at any architectural tier (`L1` through `L6`).
- Constructing Level 1 (YAML frontmatter), Level 2 (`When NOT to Use` body circuit breakers), and Level 3 (headless `agy --sandbox -p` prompt directives) negative constraint triggers.
- Embedding BEJSON 104/104a reference schemas with O(1) Field Map Caching (`field_map`) and boundary-layer sanitization into skill bundles.
- Running deterministic Layer 2 static quality gates (`scripts/skill_architect_linter.py`) to verify line budgets (`<= 500` lines), description ceilings (`<= 1024` chars), typography compliance, and sandbox containment before registering with `skill-ecosystem-cartographer`.

## When NOT to Use

- Executing dependency-ordered multi-skill DAG pipelines or managing runtime stage gates (use `skill-chain-coordinator`).
- Indexing installed skills, building pairwise trigger collision matrices, or querying the global skill topology catalog (use `skill-ecosystem-cartographer`).
- Scheduling multi-turn conversational pre-planning delays across $N = K + 1$ turns (use `planning-schema-planner`).
- Refactoring existing application persistence layers from SQLite/CSV to BEJSON (use `bejson-codebase-refactor`).
- Decomposing monolithic application codebases into `L0-L5` class hierarchies (use `arch-layered-refactor`).

---

## 1. Architectural Guardrails & Layer Boundary Laws

Every skill designed by `skill-architect` MUST declare and obey its exact position within the 6-Tier Layered Skill Architecture. Full taxonomic tables reside in [`references/layer_taxonomy_and_guardrails.md`](./references/layer_taxonomy_and_guardrails.md).

### 1.1 The 6-Tier Skill Hierarchy & Codebase Isomorphism

| Skill Tier | Codebase Layer | Core Responsibility | Allowed Downward Dependencies | Canonical Suffixes |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1 (L1)** | `L0` Substrate / `L1` Entities | Invariant data formats (`BEJSON 104/104a/104db`, `MFDB`, `BEHTML` math), O(1) `field_map` cache, atomic file I/O (`.tmp` -> `fsync` -> `replace`) | **None** (Zero external dependencies; Open Substrate) | `-core`, `-nesting-core`, `-mfdb-core` |
| **Layer 2 (L2)** | `L1` Validation / `L2` Verification | Deterministic schema validators, error code registries (`1-159`, `300-329`, `400-449`), archive/doc chunkers, policy conflict auditors | **L1 only** (Zero UI, HTTP, or CLI transport logic) | `-validator`, `-chunker`, `-auditor`, `-engine` |
| **Layer 3 (L3)** | `L2` Adapters / `L3` Services | Language script scaffolders (`python`, `javascript`, `bash`), headless `agy --sandbox` dispatchers, `fcntl.flock` daemons, ZIP delivery | **L1 - L2** (Embeds L1 schemas and L2 validators) | `-automator`, `-pipeline`, `-scaffold-<lang>`, `-manager`, `-delivery` |
| **Layer 4 (L4)** | `L4` Presentation & Transport | 8-lane X-axis grids (`x_start + x_span <= 8`), `Ry=32px` row quantization, BECSS Tri-Color (`#000000`, `#FFFFFF`, `#DE2626`), UI decomposition | **L1 - L3** (Closed layer; never mutates disk persistence directly) | `-builder`, `-diagrammer`, `-decomposer`, `-mapper`, `-template`, `-preferences` |
| **Layer 5 (L5)** | `L3` Use Cases & Blueprints | Feature menus (`1..N`), `<prefix>_<descriptor>_<unit>` taxonomies, MFDB planners, legacy-to-BEJSON refactors, multi-page manuals | **L1 - L4** (Pre-plans and transforms across L1-L4 contracts) | `-composer`, `-planner`, `-architect`, `-refactor`, `-rewriter`, `-writer`, `-analysis`, `-extraction` |
| **Layer 6 (L6)** | `L5` Composition Root | Ecosystem meta-governance, DAG coordination (`skill-chain-coordinator`), topology mapping (`skill-ecosystem-cartographer`), turn delays | **L1 - L5** (Orchestrates lifecycles; zero low-level domain logic) | `-coordinator`, `-cartographer`, `-recipe-composer`, `skill-architect`, `arch-*` |

### 1.2 Three Formal Dependency Invariants

1. **Strict Downward Dependency Law**: Let $L(S) \in \{1, 2, 3, 4, 5, 6\}$ denote the tier of skill $S$. Skill $S_a$ may depend upon, invoke, or embed templates from skill $S_b$ only if $L(S_a) > L(S_b)$, or via sequential stage handoffs governed by `skill-chain-coordinator` where upstream outputs are frozen before downstream invocation.
2. **Open Substrate vs. Closed Intermediate Layers**:
   - **Open Substrate (`L1`)**: Any upper layer (`L2-L6`) may directly embed or invoke Layer 1 primitives (`bejson_core_get_field_map`, `bejson_core_atomic_write`, error code constants).
   - **Closed Presentation & Service Layers (`L3-L4`)**: Layer 4 UI skills must never bypass Layer 3 services to mutate Layer 1/2 persistence stores directly ("The Leaky Route" anti-pattern).
3. **Contract Freezing Before Upper-Layer Execution**: All Layer 1 schemas (`Fields`, `Records_Type`, entity prefixes, UUID PKs, `_fk` foreign keys) must pass a Layer 2 validator gate before Layer 3 scaffolders or Layer 4 UI builders execute.

---

## 2. Relational Naming & Negative Constraint Trigger Engineering

### 2.1 Relational Naming Formula

Every skill identifier MUST obey the deterministic three-part formula:

$$\text{SkillIdentifier} = \texttt{[Domain]}\text{-}\texttt{[Subdomain]}\text{-}\texttt{[FunctionalSuffix]}$$

- **Regex Constraint**: `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase alphanumeric and ASCII hyphens only, 1 to 5 words, maximum 64 characters).
- **Approved Domain Prefixes**: `agy`, `arch`, `behtml`, `bejson`, `code`, `component`, `concept`, `concepts`, `file`, `ideation`, `job`, `mfdb`, `planning`, `policy`, `prompt`, `publication`, `skill`, `taxonomy`, `template`, `ui`, `web-ui`.

### 2.2 Set-Theoretic Mutual Negative Guardrails

To prevent multi-skill context pollution during Stage 1 Discovery, every skill $S_i$ defines a Positive Trigger Region $T^+(S_i)$ and a Negative Constraint Exclusion Region $T^-(S_i)$ such that pairwise effective activation regions are disjoint across sibling skills:

$$A(S_i) = T^+(S_i) \setminus T^-(S_i), \quad A(S_i) \cap A(S_j) = \emptyset \quad \forall S_j \in \text{Neighbors}(S_i)$$

Every skill authored by `skill-architect` MUST implement negative constraints at three levels:

1. **Level 1: Frontmatter Routing Guardrail (`description` <= 1024 characters)**:
   ```yaml
   description: >-
     [Imperative capability statement]. Use when [explicit positive user triggers].
     Do NOT use for [adjacent task A] (use [sibling-skill-A]), [adjacent task B]
     (use [sibling-skill-B]), or [adjacent task C] (use [sibling-skill-C]).
   ```
2. **Level 2: Body Exclusion Guardrail (`## When NOT to Use`)**:
   - Bulleted circuit breaker evaluated immediately upon Stage 2 activation, instructing the agent which exact sibling skill to hand off to if misrouted.
3. **Level 3: Headless Execution Prompt Guardrail (`agy --sandbox -p`)**:
   - Mandatory for Layer 3/Layer 6 automation skills invoking `agy`:
     ```text
     [DIRECTIVE-TAG] Target Subtree: <subfolder>. <Task instructions>.
     Negative Constraints: Zero conversational fluff, preamble, or closing remarks.
     Do NOT modify files outside <subfolder>. Output ONLY to <target_filepath>.
     ```

---

## 3. Progressive Disclosure & Bundle Directory Topology

To protect the 20,000-token rules budget and minimize active turn overhead, skills are partitioned across the 3-Stage Progressive Disclosure lifecycle:

- **Stage 1 (Discovery)**: Only YAML `name` and `description` (`<= 1024` chars) load into the startup routing catalog (~30-150 tokens/skill).
- **Stage 2 (Activation)**: Full `SKILL.md` body loads on semantic match or `/<skill-name>` invocation. **Hard Ceiling: `<= 500` lines**.
- **Stage 3 (Execution & Resource Expansion)**: Companion files in `references/`, `assets/`, and black-box CLI tools in `scripts/` are accessed strictly on demand. Never inline bulky schemas or script source code into `SKILL.md` when a relative link suffices.

### Standard Skill Bundle Layout

```text
<skill-name>/
├── SKILL.md                        # Mandatory manifest (<= 500 body lines; YAML frontmatter)
├── references/                     # On-demand Stage 3 deep domain specs and schemas
│   ├── layer_taxonomy_and_guardrails.md
│   └── reference_schemas.md
├── scripts/                        # Black-box Python 3.10+ / Bash CLI validators & scaffolders
│   ├── skill_architect_linter.py
│   └── scaffold_layered_skill.py
└── assets/                         # Zero-filler structural starter templates (.bejson, .md)
    ├── starter_skill_template.md
    └── starter_registry.104a.bejson
```

---

## 4. Reference Schemas & Mandatory Coding Standards

All schemas and scripts generated or embedded within skills MUST comply with [`references/reference_schemas.md`](./references/reference_schemas.md) and these core invariants:

1. **BEJSON 104a Compliance**:
   - Six mandatory top-level keys: `Format` (`"BEJSON"`), `Format_Version` (`"104a"`), `Format_Creator` (`"Elton Boehnen"`), `Records_Type`, `Fields`, `Values`.
   - Boundary-layer sanitization: Strip leading/trailing whitespace from all keys, field definitions, and string values before processing.
   - O(1) Field Map Cache: Always resolve column indices dynamically via `field_map = {f["name"]: idx for idx, f in enumerate(doc["Fields"])}`. Hardcoded positional indexing (`row[0]`) is strictly prohibited.
   - Atomic Disk Writes: Write to `.tmp`, flush buffer, call `os.fsync()`, and execute `os.replace()`.
2. **Script Standards (Python 3.10+ & Bash)**:
   - Include canonical file headers (`Name`, `Description`, `VERSION` integer constant, `Date Created`, `Author`, `RELATIONAL_ID` UUIDv4, `Release_Version: 300`).
   - Use the Python `logging` module exclusively; never use `print()` for runtime logging.
   - Resolve paths relatively via `SCRIPT_PATH = Path(__file__).resolve().parent`; never hardcode absolute host paths.
   - Enforce deterministic exit codes: `0` (Clean pass), `10` (Lock/path failure), `20` (Environment/config error), `30` (Schema/validation error).
3. **Typography & Formatting**:
   - Never use em-dashes or en-dashes in skill manifests or generated specifications; use standard ASCII hyphens (`-`) or double hyphens (`--`).

---

## 5. Step-by-Step Skill Authoring & Validation Workflow

Follow this exact five-step procedure whenever creating or refactoring an Antigravity skill:

### Step 1: Classify Layer & Verify Topology Boundaries
1. Consult [`references/layer_taxonomy_and_guardrails.md`](./references/layer_taxonomy_and_guardrails.md) to assign the candidate skill to its exact tier (`L1` through `L6`).
2. Select the canonical `[Domain]-[Subdomain]-[FunctionalSuffix]` identifier matching the assigned tier.
3. Identify all adjacent sibling skills in the same domain or adjacent layers to populate the mutual negative guardrail set $T^-(S_i)$.

### Step 2: Scaffold the Skill Bundle
Run the bundled black-box scaffolder script to initialize the directory tree, starter `SKILL.md`, and BEJSON 104a metadata:

```bash
python3 scripts/scaffold_layered_skill.py \
  --name "<domain>-<subdomain>-<suffix>" \
  --layer <1-6> \
  --output-dir "<target-skills-root>" \
  --positive-triggers "<comma-separated-use-cases>" \
  --negative-siblings "<sibling-skill-1>:<task-1>,<sibling-skill-2>:<task-2>"
```

### Step 3: Populate Workflow, Reference Shards, and Assets
1. Edit the generated `SKILL.md` using [`assets/starter_skill_template.md`](./assets/starter_skill_template.md) as the structural baseline.
2. Move any schema definitions, error tables, or reference manuals exceeding 80 lines into `references/<topic>.md` and link to them relatively from `SKILL.md`.
3. Place executable validators or automation drivers in `scripts/` and document their exact CLI invocation flags and exit codes (`0`, `10`, `20`, `30`).

### Step 4: Execute the Layer 2 Quality Gate Linter
Validate the skill bundle against all structural, lexical, negative-trigger, and security invariants:

```bash
python3 scripts/skill_architect_linter.py "<path-to-skill-dir>"
```

- **Gate Requirement**: The linter MUST return `Exit Code 0` (`"valid": true`, zero `E_*` errors). If `Exit Code 30` is returned, remediate all reported error codes (`401-415`) and re-run before proceeding.

### Step 5: Register with Cartographer & Reload Runtime
1. Register the validated skill entry into the ecosystem catalog (`skill_registry_catalog.104a.bejson`) via `skill-ecosystem-cartographer` to verify zero pairwise trigger collisions across the installed skill index.
2. In interactive TUI sessions, execute `/skills reload` to mount the new `/<skill-name>` slash command immediately.

---

## Credits & Attribution

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
