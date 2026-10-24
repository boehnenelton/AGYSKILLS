---
name: spark-skill-refactor
description: Audit, refactor, optimize, and harmonize existing Gemini Spark skills individually or in symbiotic clusters to enforce 6-tier layer boundaries, progressive disclosure (<500 lines), Jaccard trigger collision thresholds, and the 4-pillar deliverable taxonomy. Use when inspecting or refactoring SKILL.md files for context bloat, trigger overlap, asymmetric negative guardrails (Codes 430-433), phonetic alias drift, placeholder compliance, and BEJSON 104a data contracts. Do NOT use for designing new skills from scratch (use skill-architect), indexing global skill catalogs (use skill-ecosystem-cartographer), resolving concept definitions (use definitions-cartographer), auditing general policies (use policy-conflict-auditor), Antigravity CLI daemons (use agy-skill-refactor), or application code (use bejson-codebase-refactor).
---
# Spark Skill Refactor

Systematic Layer 6 refactoring, optimization, and harmonization framework for Gemini Spark skills. Enforces 3-stage progressive disclosure, strict line budgets (<500 lines), mathematical anti-collision trigger boundaries, the 4-pillar deliverable taxonomy, and symbiotic inter-skill alignment across the 6-tier architecture.

## Summary

Audits and transforms existing Gemini Spark skills individually or across interconnected domain clusters. Prunes context bloat, eliminates semantic trigger collisions using Jaccard token overlap metrics ($J < 0.25$ or reciprocal negative partitioning), enforces the 4-pillar deliverable taxonomy (`Template`, `Example`, `Demonstration`, `Reference`), normalizes phonetic speech-to-text drift, offloads deep documentation to `references/`, and embeds deterministic validation scripts in `scripts/`.

## When to Use

- Refactoring an existing Gemini Spark skill to eliminate token bloat and enforce the 500-line ceiling.
- Harmonizing a cluster of sibling skills to resolve Cartographer Error Codes 430-433 (duplicate names, Jaccard trigger collisions, asymmetric guardrails, dangling sibling references).
- Partitioning monolithic `SKILL.md` files into 3-stage progressive disclosure structures (`SKILL.md`, `references/`, `scripts/`, `assets/`).
- Auditing skill templates, examples, demonstrations, and references against the 4-pillar deliverable taxonomy and zero-filler placeholder rules.
- Normalizing phonetic speech-to-text distortions (such as `certographer`, `cartographer ancblayers`, or `fillker`) and enforcing Policy 5.1 inline definitions.
- Standardizing inter-skill manifests and registries to BEJSON 104a specifications.

## When NOT to Use

- Designing, scaffolding, or authoring brand-new skills from scratch (use `skill-architect` or `skill-creator`).
- Cataloging installed skills or generating global topology maps without refactoring skill files (use `skill-ecosystem-cartographer`).
- Querying or maintaining canonical terminology and voice alias registries directly (use `definitions-cartographer`).
- Auditing general non-skill policy documents for rule contradictions (use `policy-conflict-auditor`).
- Refactoring Antigravity CLI prompts, headless daemons, or minute-based loops (use `agy-skill-refactor`).
- Refactoring general Python, JavaScript, TypeScript, or Bash application codebases (use `bejson-codebase-refactor` or `arch-layered-refactor`).

## 1. Core Refactoring & Cartographer Principles

1. **Context Window Parsimony**: Challenge every sentence in `SKILL.md`. Strip conversational preambles, historical narratives, and redundant explanations.
2. **Three-Stage Progressive Disclosure**:

   - **Stage 1 (Discovery)**: Keep frontmatter `name` and tripartite `description` under 1024 characters for lean router scanning.
   - **Stage 2 (Activation)**: Keep `SKILL.md` body strictly under 500 lines (partition at 400 lines).
   - **Stage 3 (Execution)**: Offload deep schemas and matrices to `references/<topic>.md` and deterministic validators to `scripts/<tool>.py`.
3. **Mathematical Anti-Collision Protocol (Cartographer Alignment)**:

   - Every skill description must contain three explicit segments: Capability Statement, Positive Triggers (`Use when...`), and Mutual Negative Guardrails (`Do NOT use for X (use skill-architect)`).
   - Sibling skills with pairwise Jaccard positive trigger similarity $J(T^+(S_i), T^+(S_j)) \ge 0.25$ must declare reciprocal negative exclusions so effective activation regions remain disjoint: $A(S_i) \cap A(S_j) = \emptyset$.
4. **Four-Pillar Deliverable Taxonomy Enforcement**:

   - **Template**: 0% hydrated bare structural skeleton with literal spatial placeholders (`Title`, `Content Body`, `Menu Header`) and zero filler (`lorem ipsum`, `foo`, `bar`, `TBD`).
   - **Example**: Minimally hydrated syntax snippet illustrating an isolated pattern or parameter.
   - **Demonstration**: 100% hydrated, interactive, production-ready showcase with realistic telemetry.
   - **Reference**: Canonical specification, error registry, or frozen data contract stored in `references/`.
5. **Semantic Normalization & Policy 5.1 Compliance**:

   - Replace voice-typing and speech-to-text drift (`certographer` -> `Cartographer`, `cartographer ancblayers` -> `Cartographer and Layers`, `fillker` -> `filler`, `be Jason` -> `BEJSON`) with canonical ecosystem identifiers from `definitions-cartographer`.
   - Include a concise one-sentence inline definition on first mention of specialized ecosystem terms.
6. **Verifiable Execution ("Verify, Don't Trust")**: Pair every refactoring pass with deterministic verification via `scripts/spark_skill_linter.py`.

## 2. Six-Tier Architectural Layering

Categorize every refactored skill into its exact layer in the 6-tier hierarchy. Dependencies must flow strictly downward (Layer $N$ may depend only on Layers $\le N - 1$):

- **Layer 1: Core Substrate & Data Format**

  - *Scope*: Invariant data structures (BEJSON 104/104a/105, MFDB manifests, BEHTML 18-field coordinate math), atomic I/O, O(1) field map caching.
  - *Canonical Suffixes*: `-core`, `-nesting-core`, `-mfdb-core`.
- **Layer 2: Domain Engines, Validation & Processing**

  - *Scope*: Deterministic validation algorithms, error diagnostics (Codes 1-159, 300-329, 400-449), schema drift detection, archive and document chunkers.
  - *Canonical Suffixes*: `-validator`, `-chunker`, `-auditor`, `-engine`.
- **Layer 3: Automation Pipelines, CLI & Scaffolding**

  - *Scope*: Language-specific single-file scaffolders, headless sandbox dispatchers, media pipelines, delivery packaging.
  - *Canonical Suffixes*: `-automator`, `-pipeline`, `-scaffold-<lang>`, `-delivery`.
- **Layer 4: UI, Spatial Layout & Visual Presentation**

  - *Scope*: 8-lane / 16-sublane spatial grids, Ry=32px row quantization, z-layer stacking, BECSS Tri-Color tokens, wireframes, navigation trees.
  - *Canonical Suffixes*: `-builder`, `-diagrammer`, `-decomposer`, `-template`, `-preferences`.
- **Layer 5: System Architecture, Ideation & Transformation**

  - *Scope*: Numbered feature menus, macro-concept expansion, identifier naming taxonomies, language-specific MFDB planners, codebase and document refactoring.
  - *Canonical Suffixes*: `-composer`, `-planner`, `-architect`, `-refactor`, `-rewriter`.
- **Layer 6: Root Orchestration & Meta-Governance**

  - *Scope*: Ecosystem skill authoring, topology cartography, definitions cartography, skill refactoring, multi-skill DAG orchestration.
  - *Canonical Suffixes*: `-coordinator`, `-cartographer`, `-recipe-composer`, `skill-architect`, `spark-skill-refactor`.

Consult `references/spark_refactor_matrix.md` for the complete layer matrix, 4-pillar deliverable rules, and error code mappings.

## 3. Individual Skill Refactoring Workflow

Execute this five-step sequence when refactoring a single skill:

### Step 1: Ingestion and Baseline Lint Audit

Fetch the existing skill via `lookup_skills` (and `get_skill_resources` if bundled files exist). Run the linter against the skill directory:

```bash
python3 skills/spark-skill-refactor/scripts/spark_skill_linter.py skills/<skill-name>
```

### Step 2: Tri-Partite Description & Cartographer Guardrail Hardening

Refine the frontmatter `description`:

- Keep total length strictly under 1024 characters.
- Strip vague catch-all verbs (`handle`, `manage`, `process`, `utility`).
- Structure into Capability Statement, `Use when...` triggers, and `Do NOT use for...` guardrails.
- Verify that every sibling skill referenced in `Do NOT use for...` is an active, registered skill name (preventing `Code 433: E_CARTOGRAPHER_DANGLING_SIBLING_REF`).

### Step 3: Body Pruning, Taxonomy Alignment, and Formatting

- Enforce direct, imperative instructions.
- Replace all em-dashes and en-dashes with standard ASCII hyphens (`-`) or periods (`.`).
- Insert a blank line before every bulleted or numbered list block.
- Audit embedded snippets against the 4-pillar taxonomy: remove filler (`lorem ipsum`, `TBD`, `foo`) from Templates, keep Examples minimal, and move exhaustive tables or frozen contracts to `references/`.
- Resolve any contradictory internal rules using the atomic `IF [Condition] AND [Scope] THEN [Requirement] UNLESS [Exception]` normalization pattern from `policy-conflict-auditor`.

### Step 4: Progressive Disclosure Extraction

If `SKILL.md` exceeds 400 lines:

- Extract reference matrices, error tables, and schema catalogs into `references/`.
- Extract validation or inspection logic into `scripts/`.
- Reference extracted files explicitly in `SKILL.md`.

### Step 5: Validation and Persistence

Run `scripts/spark_skill_linter.py` to confirm zero errors and zero warnings. Persist single-file skills with `content` or multi-file skills with `skill_dir` via `skills:update_skill` (preserving the exact `name` and setting `enabled=true` when requested).

## 4. Cluster Harmonization & Collision Audit Workflow

Execute this workflow when harmonizing a domain cluster of related skills:

### Step 1: Cluster Discovery and Pairwise Jaccard Audit

Run the linter in cluster mode across all target skill directories to compute pairwise Jaccard similarity $J(T^+(S_i), T^+(S_j))$ and check reciprocity:

```bash
python3 skills/spark-skill-refactor/scripts/spark_skill_linter.py --cluster skills/
```

### Step 2: Resolve Cartographer Error Codes (430-433)

- **`Code 430: E_CARTOGRAPHER_DUPLICATE_SKILL`**: Consolidate duplicate skill identifiers.
- **`Code 431: E_CARTOGRAPHER_TRIGGER_COLLISION`**: When $J(T^+(S_i), T^+(S_j)) \ge 0.25$, sharpen domain nouns and add explicit negative exclusions between $S_i$ and $S_j$.
- **`Code 432: E_CARTOGRAPHER_ASYMMETRIC_GUARDRAIL`**: When $S_i$ excludes $S_j$ in the same cluster, add the reciprocal exclusion of $S_i$ to $S_j$.
- **`Code 433: E_CARTOGRAPHER_DANGLING_SIBLING_REF`**: Replace outdated or unregistered skill names in negative guardrails with canonical installed skill names.

### Step 3: Shared Substrate Consolidation & BEJSON 104a Alignment

- Delegate duplicated low-level logic (such as field map caching or atomic writes) downward to Layer 1 `-core` skills.
- Standardize all skill registries (`skill_registry_catalog.104a.bejson`, `definitions_registry.104a.bejson`) to BEJSON 104a with mandatory keys (`Format`, `Format_Version`, `Format_Creator: "Elton Boehnen"`, `Records_Type`, `Fields`, `Values`).

## Gotchas and Anti-Patterns

- **Destroying Multi-File Bundles**: Calling `skills:update_skill` with `content` instead of `skill_dir` on a multi-file skill deletes `references/` and `scripts/`. Always inspect `file_names` first and use `skill_dir` for multi-file skills.
- **One-Way Negative Guardrails**: Excluding Skill B from Skill A without updating Skill B to exclude Skill A leaves an asymmetric routing vulnerability (`Code 432`).
- **Upward Layer Dependencies**: Never wire a lower-layer skill (L1-L3) to depend on a higher-layer skill (L4-L6).
- **Taxonomy Contamination**: Never put mock sample copy inside a `Template` or leave unhydrated placeholders inside a `Demonstration`.
