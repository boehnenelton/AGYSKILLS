# 6-Tier Layered Skill Taxonomy, Guardrails, and Error Registries

> **Parent Skill:** `skill-architect` (Layer 6)  
> **Version:** 102 | **Release_Version:** 300 | **RELATIONAL_ID:** `f19c3d82-4a7e-4b01-8c64-3e5d9a2b7f10`  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Dual Hierarchy Isomorphism: Skill Tiers (L1-L6) vs. Codebase Layers (L0-L5)

Every skill in the ecosystem maps deterministically to an application codebase layer, enforcing strict separation of concerns and unidirectional downward dependencies:

| Skill Tier | Codebase Layer | Architectural Invariants & Boundary Rules | Allowed Downward Dependencies | Approved Functional Suffixes |
| :--- | :--- | :--- | :--- | :--- |
| **Layer 1 (L1): Core Substrate & Data Format** | **L0 (Substrate) & L1 (Domain Entities)** | Invariant data structures (`BEJSON 104`, `104a`, `104db`, `Nested 104`, `MFDB`, `BEHTML` 18-field math), O(1) `field_map` caching, boundary whitespace sanitization, atomic file I/O (`.tmp` -> `fsync` -> `replace`), global error registries | **None** (Zero external dependencies; Open Substrate accessible to all upper tiers) | `-core`, `-nesting-core`, `-mfdb-core` |
| **Layer 2 (L2): Domain Engines, Validation & Processing** | **L1 (Domain Validation) & L2 (Persistence Verification)** | Deterministic validation algorithms, error code diagnostics (`1-159`, `300-329`, `400-449`), schema drift detection, self-healing, archive/document chunkers, policy conflict matrices | **L1 only** (Operates strictly on L1 contracts; zero UI, HTTP, or CLI orchestration logic) | `-validator`, `-chunker`, `-auditor`, `-engine` |
| **Layer 3 (L3): Automation Pipelines, CLI & Scaffolding** | **L2 (Persistence Adapters) & L3 (Application Services)** | Self-contained script scaffolders (`Python`, `JS`, `Bash`) embedding L1/L2 primitives, headless `agy --sandbox` dispatchers, `fcntl.flock` daemons, FFmpeg media pipelines, ZIP packaging | **L1 - L2** (Generates executable artifacts embedding L1 schemas and L2 validators) | `-automator`, `-pipeline`, `-scaffold-python`, `-scaffold-javascript`, `-scaffold-bash`, `-manager`, `-delivery` |
| **Layer 4 (L4): UI, Spatial Layout & Visual Presentation** | **L4 (Presentation & Transport Adapters)** | 8-lane / 16-sublane horizontal grids (`x_start + x_span <= 8`), `Ry=32px` row quantization, `z_layer * 32` stacking, BECSS Tri-Color (`#000000`, `#FFFFFF`, `#DE2626`), zero-filler wireframes, sitemaps, component trees | **L1 - L3** (Closed presentation layer; never queries databases or mutates disk persistence directly) | `-builder`, `-diagrammer`, `-decomposer`, `-mapper`, `-template`, `-preferences` |
| **Layer 5 (L5): Ideation, System Architecture & Refactoring** | **L3 (Use Case Design) & Cross-Layer Blueprinting** | Numbered feature menus (`1..N`), concept nuance analysis, idea pattern extraction, `<prefix>_<descriptor>_<unit>` naming taxonomies, language-specific MFDB planners, SQLite/JSON-to-BEJSON codebase refactoring, documentation portals | **L1 - L4** (Pre-plans systems and orchestrates transformations across L1-L4 contracts) | `-composer`, `-planner`, `-architect`, `-refactor`, `-rewriter`, `-writer`, `-analysis`, `-extraction` |
| **Layer 6 (L6): Root Orchestration & Meta-Governance** | **L5 (Composition Root & Runtime Bootstrap)** | Ecosystem skill scaffolding (`skill-architect`), topology mapping & collision prevention (`skill-ecosystem-cartographer`), multi-skill DAG execution (`skill-chain-coordinator`), `N = K + 1` turn delays (`planning-coordinator`), monolithic decomposition (`arch-layered-refactor`) | **L1 - L5** (Coordinates entire ecosystem lifecycles without implementing low-level domain logic) | `-coordinator`, `-cartographer`, `-recipe-composer`, `skill-architect`, `arch-*`, `agy-skill-refactor` |

---

## 2. Canonical Domain Prefix & Functional Suffix Registry

### 2.1 Approved Domain Tokens (`[Domain]`)

| Domain Token | Architectural Scope | Primary Target Artifacts |
| :--- | :--- | :--- |
| `agy` | Antigravity CLI headless automation, presets, and daemon orchestration | `agy_presets.104a.bejson`, `reports/audits/*.md` |
| `arch` | Root 6-layer codebase decomposition and boundary enforcement | Layered migration plans, module interface contracts |
| `behtml` | 8-lane / `Ry=32px` spatial HTML coordinate math, validation, and layout | `.behtml`, `18-field BEHTMLElement` datasets, `.html` |
| `bejson` | Tabular JSON (`104`, `104a`, `104db`, `Nested 104`) persistence and tools | `.bejson`, `.104a.bejson`, `.104db.bejson` |
| `code` | Identifier naming taxonomies (`<prefix>_<descriptor>_<unit>`) and manuals | Prefix registries, multi-page HTML code portals |
| `component` | UI component tree to backend BEJSON schema derivation | Entity schemas, foreign key (`_fk`) registries |
| `concept` / `concepts` | Concept nuance pattern analysis and concept/idea pattern extraction | `target/ideas/*.md`, `data/concept_*.104a.bejson` |
| `file` | Clean project packaging, `.beignore` filtering, and ZIP archive delivery | `<Project_Name>-V#-PKG#.zip` |
| `ideation` | Numbered feature menus (`1..200+`), macro treatises, and user interviews | Feature menus, builder prompts |
| `job` | Sequential single-task JobMaker BEJSON 104a workflow execution | Job state ledgers (`.104a.bejson`) |
| `mfdb` | Multi-File Database (`104a.mfdb.bejson`) architecture and language planners | `104a.mfdb.bejson`, Master-Slave sync blueprints |
| `planning` | Turn-delayed (`N = K + 1`) conversational schema and template pre-planning | Frozen schema/wireframe phase blueprints |
| `policy` | Atomic rule extraction (`POL-xxx`) and $N \times N$ contradiction matrices | Conflict matrices, exception registries |
| `prompt` | Parameterized system prompt composition with `{{VAR:-default}}` slots | Dynamic prompt templates (`.md`) |
| `publication` | Standalone editorial HTML formatting (`#DE2626`, drop-caps, dotted TOC) | Publication `.html` |
| `skill` | Ecosystem skill authoring, DAG coordination, recipe design, and cartography | `SKILL.md` bundles, `skill_registry_catalog.104a.bejson` |
| `taxonomy` | Backend BEJSON schema projection into 100%-coverage UI component trees | UI component hierarchy maps (`.md`) |
| `template` | Bare-bones Release 300 structural wireframe scaffolding | Structural `.html` / `.py` wireframes |
| `ui` / `web-ui` | Sitemap route decomposition and abstract UI component mapping | Navigation trees, ASCII component trees |

---

## 3. Formal Set-Theoretic Negative Constraint Trigger Model

### 3.1 Disjoint Activation Condition

Let $\mathcal{P}$ denote the universe of user prompts and $\mathcal{S} = \{S_1, S_2, \dots, S_n\}$ denote the set of installed skills. Each skill $S_i$ defines:
- **Positive Trigger Region** $T^+(S_i) \subset \mathcal{P}$: Explicit capability verbs and `"Use when..."` clauses.
- **Negative Exclusion Region** $T^-(S_i) \subset \mathcal{P}$: Explicit `"Do NOT use for..."` clauses with sibling redirections `(use <sibling-skill>)`.
- **Effective Activation Region**: $A(S_i) = T^+(S_i) \setminus T^-(S_i)$.

To guarantee zero multi-skill context collisions during Stage 1 Discovery, every pair of sibling skills $(S_i, S_j)$ sharing domain vocabulary must satisfy **Reciprocal Negative Partitioning**:

$$T^+(S_j) \subseteq T^-(S_i) \quad \text{and} \quad T^+(S_i) \subseteq T^-(S_j) \implies A(S_i) \cap A(S_j) = \emptyset$$

### 3.2 Six-Pass Contradiction Audit Classification (`policy-conflict-auditor` & `skill-ecosystem-cartographer`)

Every skill routing rule is normalized into the Four-Attribute Atomic Tuple:

$$\text{Rule} = (\texttt{ID}, \texttt{DomainBoundary}, \texttt{Condition}, \texttt{Requirement}, \texttt{Priority})$$

$$\text{Normalized Form: } \texttt{IF } [\text{Condition}] \texttt{ AND } [\text{DomainBoundary}] \texttt{ THEN } [\text{Requirement}] \texttt{ UNLESS } [\text{Exception}]$$

Pairwise interactions between rules $(R_a, R_b)$ are classified into five deterministic categories:

| Interaction Type | Matrix Symbol | Definition & Resolution Protocol |
| :--- | :---: | :--- |
| **Type A: Orthogonal / Compatible** | `OK` | Disjoint `DomainBoundary` (e.g., Python CLI vs. BEHTML CSS). Zero action required. |
| **Type B: Conditional Disjointness** | `COND` | Shared domain boundary partitioned cleanly by mutual `UNLESS` / `"Do NOT use for"` clauses (e.g., Greenfield Scaffolding vs. Existing Codebase Refactoring). Validated safe. |
| **Type C: Redundant Overlap** | `RED` | Identical condition and requirement across two skills. Consolidate into the lower-layer canonical skill and add a negative redirect in the sibling. |
| **Type D: Direct Contradiction** | `ERR_D` | Identical `Condition` and `DomainBoundary` with incompatible `Requirement` or missing mutual negative triggers. **Blocks registration (Exit Code 30)**. |
| **Type E: Priority / Layer Inversion** | `ERR_E` | Lower-layer skill (`L1/L2`) attempts to invoke or override an upper-layer skill (`L4/L5/L6`), violating the Strict Downward Dependency Law. **Blocks registration (Exit Code 30)**. |

---

## 4. Consolidated Error Code Registries

All Layer 2 validators and Layer 6 governance tools emit deterministic integer error codes:

| Code Range | Subsystem | Error Code Definitions |
| :--- | :--- | :--- |
| **`1 - 19`** | Base BEJSON (`bejson-schema-validator`) | `1: E_INVALID_JSON`, `2: E_MISSING_MANDATORY_KEY`, `3: E_INVALID_FORMAT`, `4: E_INVALID_VERSION`, `6: E_INVALID_FIELDS`, `8: E_TYPE_MISMATCH`, `9: E_RECORD_LENGTH_MISMATCH`, `10: E_RESERVED_KEY_COLLISION`, `11: E_INVALID_RECORD_TYPE_PARENT`, `16: E_INVALID_FORMAT_CREATOR` |
| **`20 - 29`** | BEJSON Runtime Access | `21: E_CORE_UNKNOWN_FIELD`, `22: E_POSITIONAL_DRIFT_HARDCODED_INDEX`, `23: E_UNSANITIZED_BOUNDARY_WHITESPACE` |
| **`30 - 49`** | MFDB (`bejson-schema-validator`) | `30: E_MFDB_NOT_MANIFEST`, `32: E_MFDB_MANIFEST_RECORDS_TYPE`, `33: E_MFDB_ENTITY_NOT_FOUND`, `36: E_MFDB_NO_PARENT_HIERARCHY`, `38: E_MFDB_BIDIRECTIONAL_FAIL`, `39: E_MFDB_FK_UNRESOLVED`, `42: E_MFDB_INVALID_ARCHIVE` |
| **`130 - 159`** | Nested BEJSON (`bejson-nesting-core`) | `130: E_NESTING_INVALID_CELL`, `131: E_NESTING_NOT_BEJSON`, `132: E_NESTING_DEPTH_EXCEEDED` (>16), `134: E_NESTING_SCHEMA_MISMATCH`, `135: E_NESTING_CIRCULAR_REF` |
| **`300 - 329`** | BEHTML Spatial (`behtml-schema-validator`) | `301: E_BEHTML_MISSING_ID`, `303: E_BEHTML_DUPLICATE_ID`, `305: E_BEHTML_INVALID_X_ADDRESS`, `306: E_BEHTML_X_SPAN_OVERFLOW` (`x_start + x_span > 8`), `307: E_BEHTML_QUANTIZATION_FAIL` (`height % 32 != 0`), `316: E_BEHTML_INVALID_URL`, `317: E_BEHTML_COLLISION`, `320: E_BEHTML_CYCLIC_PARENT` |
| **`400 - 429`** | Skill Architect Linter (`skill-architect`) | `401: E_SKILL_MISSING`, `402: E_FRONTMATTER_START`, `403: E_FRONTMATTER_UNCLOSED`, `404: E_LINE_BUDGET_EXCEEDED` (>500 body lines), `405: E_MISSING_NAME`, `406: E_INVALID_NAME_SYNTAX`, `407: E_NON_CANONICAL_SUFFIX`, `408: E_MISSING_DESCRIPTION`, `409: E_DESC_OVERFLOW` (>1024 chars), `410: E_MISSING_POSITIVE_TRIGGER`, `411: E_MISSING_NEGATIVE_TRIGGER`, `412: E_MISSING_SIBLING_POINTER`, `413: E_TYPOGRAPHY_DASH_VIOLATION`, `414: E_AGY_UNSANDBOXED`, `415: E_BEJSON_HARDCODED_INDEX` |
| **`430 - 449`** | Ecosystem Cartographer & Coordinator | `430: E_CARTOGRAPHER_DUPLICATE_SKILL`, `431: E_CARTOGRAPHER_TRIGGER_COLLISION` ($\mathcal{C}_{i,j} \neq \emptyset$), `432: E_CARTOGRAPHER_ASYMMETRIC_GUARDRAIL`, `433: E_CARTOGRAPHER_DANGLING_SIBLING_REF`, `434: E_COORDINATOR_UPWARD_DEPENDENCY` ($L(S_a) < L(S_b)$), `435: E_COORDINATOR_CYCLE_DETECTED`, `436: E_COORDINATOR_STAGE_GATE_FAILED`, `437: E_COORDINATOR_UNFROZEN_CONTRACT` |

---

## 5. Lifecycle Hooks & Subdirectory Isolation Contracts

### 5.1 Exclusive Output Subdirectory Partitioning
To prevent concurrent subagents or background daemons from clobbering files, skills route outputs by functional class:
- **Auditors (`-auditor`, `-validator`)**: Write reports exclusively to `reports/audits/*_${TIMESTAMP}.md` and append findings to `dev/security-notes.md` or `dev/dead_code.md` under `fcntl.flock` advisory locks.
- **Ideation Composers (`-composer`)**: Write exclusively to `target/ideas/*_${TIMESTAMP}.md`.
- **Schema Planners (`-planner`, `planning-schema`)**: Write exclusively to `target/schemas/*_${TIMESTAMP}.104a.bejson`.
- **Cartographer Catalogs (`skill-ecosystem-cartographer`)**: Write topology registries to `data/skill_registry_catalog.104a.bejson` and collision matrices to `reports/audits/topology_collision_matrix_${TIMESTAMP}.md`.
- **Coordinator Ledgers (`skill-chain-coordinator`)**: Write DAG execution ledgers to `data/dag_pipeline_ledger.104a.bejson`.

### 5.2 Deterministic Exit Code Standard
All scripts bundled inside `scripts/` across all skills enforce:
- `Exit Code 0`: Clean completion and verified deliverable / validation pass.
- `Exit Code 10`: Path selection, file missing, or `fcntl.flock` advisory lock contention.
- `Exit Code 20`: Environment sourcing failure, sandbox boundary violation, or missing configuration.
- `Exit Code 30`: Schema validation failure, linter gate failure (`Codes 1-449`), or upstream `agy` execution error.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
