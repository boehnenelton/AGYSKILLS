# Spark Skill Refactoring Matrix and Cartographer Standards

## 1. Six-Tier Architectural Taxonomy (L1-L6)

The Gemini Spark skill ecosystem is organized into six decoupled layers with strict downward-only dependencies (Layer $N$ depends only on Layers $\le N - 1$):

| Layer | Layer Name | Codebase Isomorphism | Primary Responsibility | Canonical Suffixes | Canonical Skills |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **L1** | **Core Substrate & Data Format** | L0 Substrate & L1 Entities | Invariant schemas (BEJSON 104/105, BEHTML 18-field math), atomic I/O, O(1) field map caching | `-core`, `-nesting-core`, `-mfdb-core` | `bejson-104-format-core`, `bejson-105-format-core`, `behtml-format-core` |
| **L2** | **Domain Engines, Validation & Processing** | L1 Validation & L2 Verification | Deterministic validation, error diagnostics (Codes 1-159, 300-329), archive & document chunking | `-validator`, `-chunker`, `-auditor`, `-engine` | `bejson-104-schema-validator`, `bejson-105-schema-validator`, `behtml-schema-validator` |
| **L3** | **Automation Pipelines, CLI & Scaffolding** | L2 Adapters & L3 Services | Single-file language scaffolders, headless CLI dispatchers, media pipelines, ZIP delivery | `-automator`, `-pipeline`, `-scaffold-<lang>`, `-delivery` | `agy-prompt-automator`, `bejson-105-scaffold-python`, `file-delivery` |
| **L4** | **UI, Spatial Layout & Presentation** | L4 Presentation Adapters | 8-lane / 16-sublane spatial grids, Ry=32px row quantization, BECSS Tri-Color tokens, sitemaps | `-builder`, `-diagrammer`, `-decomposer`, `-template`, `-preferences` | `behtml-layout-builder`, `behtml-design-preferences`, `publication-html-builder` |
| **L5** | **System Architecture, Ideation & Transformation** | L3 Use Cases & Blueprints | Feature menus, macro ideation, naming taxonomies, MFDB planners, codebase & doc refactoring | `-composer`, `-planner`, `-architect`, `-refactor`, `-rewriter` | `code-taxonomy-architect`, `mfdb-105-python-planner`, `bejson-105-codebase-refactor` |
| **L6** | **Root Orchestration & Meta-Governance** | L5 Composition Root | Skill authoring, topology cartography, definitions cartography, skill refactoring, DAG orchestration | `-coordinator`, `-cartographer`, `-recipe-composer`, `-refactor` | `skill-ecosystem-cartographer`, `definitions-cartographer`, `skill-architect`, `spark-skill-refactor`, `policy-conflict-auditor` |

## 2. Four-Pillar Deliverable Taxonomy (Definitions Cartographer Contract)

All artifacts embedded in or produced by refactored skills must adhere to the 4-pillar taxonomy enforced by `definitions-cartographer`:

| Pillar | Hydration Level | Allowed Content | Prohibited Content | Canonical Location |
| :--- | :--- | :--- | :--- | :--- |
| **Template** | 0% Hydrated | Bare structural skeleton with literal spatial placeholder labels (`Title`, `Content Body`, `Menu Header`, `Menu Item 1`) | Real copy, mock data, `lorem ipsum`, `foo`, `bar`, `TBD`, `[Insert X]` | `assets/` or inline template blocks |
| **Example** | Minimally Hydrated | Focused, isolated snippet demonstrating a single syntax rule, CLI flag, or function call | Full application scaffolding or multi-module boilerplate | `SKILL.md` workflow steps |
| **Demonstration** | 100% Hydrated | Interactive, production-ready showcase with complete realistic telemetry and active controls | Unhydrated placeholders, dead buttons, or stub functions | Standalone demo deliverables |
| **Reference** | Frozen Contract | Authoritative schema specifications, error registries, lookup matrices, and formal invariants | Conversational tutorials or mutable scratchpad notes | `references/*.md` |

## 3. Phonetic Speech-to-Text Alias Normalization

When refactoring skills or prompts authored via voice input, normalize phonetic distortions to their canonical targets:

| Phonetic / Voice-Input Drift | Canonical Ecosystem Identifier | Target Skill / Domain |
| :--- | :--- | :--- |
| `certographer` | `Cartographer` | `skill-ecosystem-cartographer` / `definitions-cartographer` |
| `cartographer ancblayers` | `Cartographer and Layers` | 6-Tier Layered Architecture (`L1-L6`) |
| `fillker` | `filler` | Zero-Filler Skeleton Law (`global-templating` / `template-architect`) |
| `shelf doc` | `Template_Document_With_Shelf.html` | `publication-html-builder` |
| `pollock` | `Policy` | `policy-conflict-auditor` |
| `be Jason` / `B JSON` | `BEJSON` | `bejson-104-format-core` / `bejson-105-format-core` |
| `B HTML` | `BEHTML` | `behtml-format-core` / `behtml-layout-builder` |
| `antigrav` | `Antigravity CLI (agy)` | `agy-prompt-automator` / `agy-skill-refactor` |

## 4. Global & Cartographer Error Registry Mapping

When auditing and harmonizing skills, classify all structural, data, and topological violations using the unified numerical error registry:

| Code | Symbolic Constant | Category | Description | Remediation |
| :--- | :--- | :--- | :--- | :--- |
| 101 | `E_FORMAT_INVALID` | BEJSON Core | Missing or invalid `Format` root key | Set root key to `"BEJSON"` |
| 102 | `E_CREATOR_INVALID` | BEJSON Core | `Format_Creator` is not `"Elton Boehnen"` | Enforce canonical creator identity |
| 110 | `E_POSITIONAL_DRIFT` | BEJSON Core | `Values` row length does not match `Fields` count | Restore positional parity with `Fields` |
| 120 | `E_ATOMIC_WRITE_FAIL` | Substrate I/O | Atomic temp-file replacement failed | Clean temporary artifact and retry atomic rename |
| 130 | `E_LINE_BUDGET_EXCEEDED` | Skill Linter | `SKILL.md` exceeds the 500-line hard ceiling | Extract deep tables and schemas to `references/` |
| 131 | `E_FILLER_PLACEHOLDER` | Taxonomy | Forbidden filler token (`lorem ipsum`, `TBD`, `foo`) in skeleton | Replace with literal functional label (`Title`, `Content Body`) |
| 201 | `E_TRIGGER_COLLISION` | Legacy Router | Overlapping positive triggers in skill descriptions | Refine domain vocabulary and add negative guardrails |
| 430 | `E_CARTOGRAPHER_DUPLICATE_SKILL` | Cartographer | Duplicate canonical skill name within scan scope | Merge or deprecate duplicate skill entry |
| 431 | `E_CARTOGRAPHER_TRIGGER_COLLISION` | Cartographer | Pairwise positive trigger Jaccard overlap $J(T^+(S_i), T^+(S_j)) \ge 0.25$ without mutual exclusion | Add reciprocal `Do NOT use for...` guardrails so $A(S_i) \cap A(S_j) = \emptyset$ |
| 432 | `E_CARTOGRAPHER_ASYMMETRIC_GUARDRAIL` | Cartographer | Skill $S_i$ excludes sibling $S_j$, but $S_j$ does not exclude $S_i$ | Add symmetric negative exclusion to sibling skill $S_j$ |
| 433 | `E_CARTOGRAPHER_DANGLING_SIBLING_REF` | Cartographer | Negative guardrail references an unregistered or renamed skill | Update pointer to the canonical registered skill name |
