# Antigravity & Gemini Skills Consolidated Ecosystem

**Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
**Release:** Release_Version 300 / 301 Era  
**Date:** 2026-10-24  
**Total Production Skills:** 84  

---

## 1. Architectural Layer Hierarchy (L1–L6)

| Layer | Tier Code | Description | Count |
| :---: | :--- | :--- | :---: |
| **L1** | `L0_Substrate_L1_Entities` | Core primitives, data structures, and format invariants | 9 |
| **L2** | `L1_Validation_L2_Verification` | Black-box validators, schema checkers, and policy gates | 12 |
| **L3** | `L2_Adapters_L3_Services` | Language scaffolders, CLI standardizers, and operational tools | 21 |
| **L4** | `L4_Presentation_Transport` | BEHTML builders, spatial templates, and UI components | 12 |
| **L5** | `L3_Use_Cases_Cross_Layer_Blueprinting` | Architecture planners, idea extractors, and taxonomy mappers | 17 |
| **L6** | `L5_Composition_Root` | Root orchestrators, cartographers, and DAG execution pipelines | 12 |

---

## 2. Master Skills Catalog

### Layer 1: L0_Substrate_L1_Entities (9 skills)

| Skill Directory | Canonical Name | Purpose & Triggers |
| :--- | :--- | :--- |
| [`behtml-format-core`](./behtml-format-core) | `behtml-format-core` | Foundational data format specification, coordinate math, 8-lane/16-sublane spatial schemas (18-field BEHTMLElement, SCHEMA_OPTIONSET_v1), zero filler placeholde... |
| [`bejson-104-core`](./bejson-104-core) | `bejson-104-core` | Create, read, update, delete, and query Foundational Era BEJSON 104, 104a, and 104db documents using libraries_104 (Release 300) across Python, JavaScript, Type... |
| [`bejson-104-nesting-core`](./bejson-104-nesting-core) | `bejson-104-nesting-core` | Embed, extract, flatten, and query recursive BEJSON 104 documents inside individual parent table cells using NestAddress(parent_path, row, col, depth) coordinat... |
| [`bejson-105-core`](./bejson-105-core) | `bejson-105-core` | Create, read, update, and manage Integrity Era BEJSON 105, 105a, and 105db documents using libraries_105 (v3.5.3+) across Python, JavaScript, TypeScript, and Ba... |
| [`bejson-sanitization-core`](./bejson-sanitization-core) | `bejson-sanitization-core` | Sanitize boundary-layer BEJSON payloads, dictionary keys, and record rows across Python, JavaScript, and Bash per Policy §10.9 prior to Field Map Cache compilat... |
| [`chunking-core`](./chunking-core) | `chunking-core` | Chunk directories, codebases, project repositories, and Admin Library systems (104/105 Lib_JS, Lib_PY, Lib_SH, Lib_TS) into standardized single-file flat BEJSON... |
| [`large-website-architect`](./large-website-architect) | `large-website-architect` | Architect, design, and scaffold production-ready large multi-page websites, documentation portals, taxonomy feeds, media galleries, and e-books using clean BEHT... |
| [`mfdb-104-core`](./mfdb-104-core) | `mfdb-104-core` | Create, link, query, and validate Foundational Era Multi-File Databases (MFDB v1.31/v1.39) comprising a central 104a.mfdb.bejson manifest and dense BEJSON 104 e... |
| [`template-architect`](./template-architect) | `template-architect` | Architect, scaffold, and optimize bare-bones structural application templates and UI wireframes across BEHTML, HTML/CSS, Python, and web frameworks adhering to ... |

### Layer 2: L1_Validation_L2_Verification (12 skills)

| Skill Directory | Canonical Name | Purpose & Triggers |
| :--- | :--- | :--- |
| [`audit-efficiency-auditor`](./audit-efficiency-auditor) | `audit-efficiency-auditor` | Audit codebases, scripts, BEJSON stores, and skill bundles for computational inefficiency, duplicate routines, dead code, redundant I/O passes, subprocess thras... |
| [`behtml-schema-validator`](./behtml-schema-validator) | `behtml-schema-validator` | Validate structural integrity, coordinate quantization (8-lane/32px), collision freedom, zero-filler compliance, and schema adherence for BEHTML documents acros... |
| [`bejson-104-validator`](./bejson-104-validator) | `bejson-104-validator` | Validate Foundational Era BEJSON 104, 104a, and 104db documents and parent-child list trees for E01-E12 structural integrity, POL-002 104a primitive-only field ... |
| [`bejson-105-validator`](./bejson-105-validator) | `bejson-105-validator` | Validate Integrity Era BEJSON 105, 105a, and 105db documents for strict E90-E95 UUID integrity (field_uuid presence/uniqueness E90/E91, reserved record_uuid row... |
| [`bejson-document-chunker`](./bejson-document-chunker) | `bejson-document-chunker` | Author, index, manipulate, assemble, mount, and manage chunked documents across BEJSON document systems (Lib_MD markdown indexing and Doc_Chunker 104db document... |
| [`bejson-enforcement-suite-builder`](./bejson-enforcement-suite-builder) | `bejson-enforcement-suite-builder` | Generate and execute mandatory Policy §10.6 runtime enforcement test suites (Conformance, Manifest Integrity, Round-Trip, Lifecycle Smoke, Post-Reset) and facto... |
| [`bejson-schema-validator`](./bejson-schema-validator) | `bejson-schema-validator` | Validate structural integrity, schema adherence, primitive field constraints, and era-specific invariants across all BEJSON formats (104, 104a, 104db, 105, 105a... |
| [`mfdb-104-chunker`](./mfdb-104-chunker) | `mfdb-104-chunker` | Package, unpack, and sticky-mount Multi-File Databases and software repositories into single-file Chunked-104a containers (.mfdb132.bejson) with SHA-256 .mfdb13... |
| [`mfdb-105-validator`](./mfdb-105-validator) | `mfdb-105-validator` | Validate Integrity Era MFDB v1.40 federated multi-file databases for cross-entity foreign-key (_fk) referential integrity (E39 E_MFDB_UNRESOLVED_FK), fk_on_dele... |
| [`playwright-debugger-auditor`](./playwright-debugger-auditor) | `playwright-debugger-auditor` | Execute automated Playwright headless browser diagnostic audits on web applications, SPAs, HTML5 canvas tools, and JavaScript games on Android Termux. Traps con... |
| [`policy-bejson-auditor`](./policy-bejson-auditor) | `policy-bejson-auditor` | Audit BEJSON application source code, owning writers, and schema registries for Policy §6.2 O(1) field_map cache compliance (zero raw row[i] positional indexing... |
| [`policy-conflict-auditor`](./policy-conflict-auditor) | `policy-conflict-auditor` | Audit technical policies, guidelines, directives, and system prompts by treating them as deterministic rule systems. Extracts atomic rules, normalizes condition... |

### Layer 3: L2_Adapters_L3_Services (21 skills)

| Skill Directory | Canonical Name | Purpose & Triggers |
| :--- | :--- | :--- |
| [`adversarial-code-reviewer`](./adversarial-code-reviewer) | `adversarial-code-reviewer` | Conducts strict, adversarial, logic-first reviews of single-file Flask applications and lightweight API services before execution or deployment. Use when evalua... |
| [`agy-prompt-automator`](./agy-prompt-automator) | `agy-prompt-automator` | Author, structure, and execute Antigravity CLI (agy) prompts, headless tasks, targeted project audits, and BEJSON 104a workflows with user-directed sandboxing a... |
| [`bejson-105-upgrade-automator`](./bejson-105-upgrade-automator) | `bejson-105-upgrade-automator` | Automate atomic migration of Foundational Era BEJSON 104, 104a, and 104db documents to Integrity Era Format 105, 105a, and 105db using libraries_105 lib_bejson_... |
| [`bejson-diagrammer-cli`](./bejson-diagrammer-cli) | `bejson-diagrammer-cli` | Generate, extend, validate, and inject systems architecture and workflow diagrams using the BEJSON Diagrammer CLI and prompt ledger instructions, in two output ... |
| [`bejson-media-pipeline`](./bejson-media-pipeline) | `bejson-media-pipeline` | Build, architect, and maintain automated FFmpeg media automation toolkits, dropzone-based processing pipelines, and standalone audio/video tools backed by BEJSO... |
| [`bejson-scaffold-bash`](./bejson-scaffold-bash) | `bejson-scaffold-bash` | Scaffold new standalone Bash scripts/tools for Elton Boehnen's BEJSON/MFDB ecosystem (Termux/Android-ready) using bundled starter templates embedding the BEJSON... |
| [`bejson-scaffold-javascript`](./bejson-scaffold-javascript) | `bejson-scaffold-javascript` | Scaffold new standalone vanilla-JavaScript or Node.js files for Elton Boehnen's BEJSON/MFDB ecosystem using bundled starter templates embedding BEJSON Core erro... |
| [`bejson-scaffold-python`](./bejson-scaffold-python) | `bejson-scaffold-python` | Scaffold new standalone Python scripts/tools for Elton Boehnen's BEJSON/MFDB ecosystem using bundled starter templates that embed the BEJSON Core error registry... |
| [`cli-ai-standardizer`](./cli-ai-standardizer) | `cli-ai-standardizer` | Create, scaffold, or refactor standalone Python CLI AI file-processing and prompting tools powered by stdlib REST API dispatch (Gemini REST, OpenAI-compatible R... |
| [`cli-processing-standardizer`](./cli-processing-standardizer) | `cli-processing-standardizer` | Create or refactor CLI file-processing tools to adhere to self-bootstrapping directory initialization, built-in default configuration extraction on first run, p... |
| [`cli-standardizer`](./cli-standardizer) | `cli-standardizer` | Scaffold, standardize, or refactor standalone Python CLI tools with embedded configuration defaults, first-run config bootstrapping, embedded BEJSON Core and Va... |
| [`file-subfolder-automator`](./file-subfolder-automator) | `file-subfolder-automator` | Scaffold standardized relative subfolder architectures (lib, config, data, exports, backups, dev, docs), migrate misplaced tracking files to dev per Policy §1.3... |
| [`gemini-interactions-core`](./gemini-interactions-core) | `gemini-interactions-core` | Build, manage, stream, and persist Gemini multi-turn conversations and sessions using the Google GenAI Interactions API (client.interactions.create, client.inte... |
| [`gemini-tooling-manager`](./gemini-tooling-manager) | `gemini-tooling-manager` | Declare, configure, and execute custom client functions and built-in tools (google_search, code_execution, url_context, file_search, mcp_server, computer_use) u... |
| [`hostile-audit-finalizer`](./hostile-audit-finalizer) | `hostile-audit-finalizer` | Conducts adversarial quality audits prior to task completion, verifies strict surgical scope (§5.1), synchronizes dev/change-log.md with bejson_project.json, lo... |
| [`job-workflow-manager`](./job-workflow-manager) | `job-workflow-manager` | Create, template, manage, and sequentially execute jobs 1 task at a time adhering to Elton Boehnen's JobMaker BEJSON 104a Job Schema and 104db Registry standard... |
| [`playwright-stealth-agent`](./playwright-stealth-agent) | `playwright-stealth-agent` | Navigate protected web applications and anti-bot challenge surfaces on Android Termux using cloaked browser fingerprints and human behavioral physics. Injects C... |
| [`playwright-termux-automation`](./playwright-termux-automation) | `playwright-termux-automation` | Start, stop, navigate, scrape, screenshot, and manage native Chromium and Playwright browser automation workflows directly on Android Termux (ARM64) without PRo... |
| [`project-bejson-cms-manage`](./project-bejson-cms-manage) | `project-bejson-cms-manage` | Operational CLI workflow execution, entity lifecycle management, health auditing, disaster recovery, and single-file Chunked-104a database staging for BEJSON CM... |
| [`readme-visual-enhancer`](./readme-visual-enhancer) | `readme-visual-enhancer` | Author, upgrade, audit, and visually enrich README documentation adhering strictly to professional developer standards: no hardcoded absolute paths (except user... |
| [`skills-backup-manager`](./skills-backup-manager) | `user:skills-backup-manager` | Audit, package, and back up user-created skills to the dedicated Google Drive skill ecosystem folders whenever skills are added, modified, or on a scheduled cad... |

### Layer 4: L4_Presentation_Transport (12 skills)

| Skill Directory | Canonical Name | Purpose & Triggers |
| :--- | :--- | :--- |
| [`behtml-104-builder`](./behtml-104-builder) | `behtml-104-builder` | Build and render Foundational Era vertical domain artifacts using libraries_104 specialized families including BEHTML and BEHTML_IDE tabular markup, Headless CM... |
| [`behtml-design-preferences`](./behtml-design-preferences) | `behtml-design-preferences` | Enforce the authoritative BEHTML design knowledge, principles, spatial grid mathematics, and visual preferences: Policy 8.1 Tri-Color tokens (#FFFFFF, #000000, ... |
| [`behtml-templates`](./behtml-templates) | `behtml-templates` | Scaffold and instantiate production BEHTML interfaces using canonical exemplar templates: Document with Shelf (16-sublane Ry=32px document with 150x150px slots)... |
| [`bejson-tui-menu-builder`](./bejson-tui-menu-builder) | `bejson-tui-menu-builder` | Build high-density 57-column terminal user interfaces (TUIs) and daemon status menus enforcing the BEJSON Positional Telemetry Discipline: strict separation of ... |
| [`code-manual-builder`](./code-manual-builder) | `code-manual-builder` | Architect, structure, and generate multi-page technical documentation websites, e-book manuals, and code compendiums with clean SEO hierarchies (root/category/f... |
| [`prompt-placeholder-composer`](./prompt-placeholder-composer) | `prompt-placeholder-composer` | Compose deterministic {{VAR:-default}} placeholder slot schemas for BEJSON 104 and 105 file templates, owning writer skeletons, and agy_presets.104a.bejson prom... |
| [`publication-html-builder`](./publication-html-builder) | `publication-html-builder` | Build and format standalone editorial HTML documents, technical specifications, and publication views backed by the canonical 16-sublane (6.25% edge gutters, 87... |
| [`template-104-template`](./template-104-template) | `template-104-template` | Generate zero-filler Foundational Era BEJSON 104, 104a, and 104db data files, lib_<family>_taxonomy.py constant registries, and Policy §10.4 owning writer modul... |
| [`template-105-template`](./template-105-template) | `template-105-template` | Generate zero-filler Integrity Era BEJSON 105, 105a, and 105db data files, UUID-fingerprinted taxonomy registries, and Policy §10.4 owning writer modules backed... |
| [`template-literal-skeleton`](./template-literal-skeleton) | `template-literal-skeleton` | Enforce the global Zero-Filler Skeleton Law across templates of all formats (HTML, CLI menus, UI layouts, scripts, BEJSON): output strict, bare-bones structural... |
| [`ui-navigation-decomposer`](./ui-navigation-decomposer) | `ui-navigation-decomposer` | Traces, extracts, decomposes, and maps the complete hierarchical navigation structure, site architecture, and spatial BEHTML/BECSS UI layout of any web page, we... |
| [`web-ui-component-mapper`](./web-ui-component-mapper) | `web-ui-component-mapper` | Extract, structure, and map complete component-level interface hierarchies of web applications, CMS platforms, admin portals, and dashboards into clean, databas... |

### Layer 5: L3_Use_Cases_Cross_Layer_Blueprinting (17 skills)

| Skill Directory | Canonical Name | Purpose & Triggers |
| :--- | :--- | :--- |
| [`bejson-codebase-refactor`](./bejson-codebase-refactor) | `bejson-codebase-refactor` | Refactor, update, and optimize codebases, scripts, or application modules to utilize BEJSON (104, 104a, 104db, Nested 104, MFDB v1.31/v1.32) architectures whene... |
| [`bejson-doc-rewriter`](./bejson-doc-rewriter) | `bejson-doc-rewriter` | Use when rewriting technical coding architectures, system design documents, tutorials, API specifications, and software guides by transposing standard data form... |
| [`book-writer`](./book-writer) | `book-writer` | Emulate Elton Boehnen's Cli_Bookwriter multi-turn chained-context book generation engine with an embedded SEO-ready publication HTML template. Guides the user t... |
| [`code-taxonomy-architect`](./code-taxonomy-architect) | `code-taxonomy-architect` | Design and standardize BEJSON entity field prefixes, snake_case column identifiers, UTC ISO-8601 <entity>_created_at timestamp conventions, and lib_bejson_<Fami... |
| [`component-taxonomy-architect`](./component-taxonomy-architect) | `component-taxonomy-architect` | Architect canonical schema_registry.104a.bejson specifications defining immutable UUIDv4 primary keys, _fk foreign-key relationships with explicit on_delete beh... |
| [`concept-idea-pattern-extraction`](./concept-idea-pattern-extraction) | `concept-idea-pattern-extraction` | Extract, distill, cluster, and normalize raw concepts, seed ideas, heuristic proxy signals, recurring design archetypes, and reusable system patterns from unstr... |
| [`concept-nuance-pattern-analysis`](./concept-nuance-pattern-analysis) | `concept-nuance-pattern-analysis` | Analyze and dissect subtle conceptual nuances, latent structural invariants, micro-patterns, mechanical couplings, edge-case failure modes, and architectural tr... |
| [`ideation-blog-post-planner`](./ideation-blog-post-planner) | `ideation-blog-post-planner` | Scan directories, codebases, and repositories to discover active development artifacts, extract technical motifs, and formulate structured blog post concepts ca... |
| [`ideation-feature-composer`](./ideation-feature-composer) | `ideation-feature-composer` | Formulate 25-50 point sequentially numbered feature catalogs. Use when brainstorming product feature menus, authoring comprehensive CLI command trees, or struct... |
| [`ideation-interview-composer`](./ideation-interview-composer) | `ideation-interview-composer` | Iteratively interviews the user through predefined baseline questions (document vs codebase, sub-types, subjects) and dynamic follow-up inquiries, researches do... |
| [`ideation-macro-composer`](./ideation-macro-composer) | `ideation-macro-composer` | Compose massive, multi-dimensional conceptual frameworks, macro systems, and expansive domain architectures from small, abstract, or vague seed concepts. Use wh... |
| [`planning-schema-planner`](./planning-schema-planner) | `planning-schema-planner` | Execute Turn 1 schema and Era allocation planning to partition project data artifacts cleanly between Foundational Era libraries_104 (104, 104a, 104db, Nested 1... |
| [`playwright-visual-testing`](./playwright-visual-testing) | `playwright-visual-testing` | Execute automated multi-viewport screenshot captures, perceptual pixel diffing, horizontal layout overflow detection, and Policy §8.1 Tri-Color token compliance... |
| [`project-bejson-cms-grounding`](./project-bejson-cms-grounding) | `project-bejson-cms-grounding` | Grounding, architectural mapping, schema inspection, and operational navigation for the zero-SQL BEJSON CMS publishing platform and MFDB data layer. Use when an... |
| [`publication-blog-post-writer`](./publication-blog-post-writer) | `publication-blog-post-writer` | Draft and assemble comprehensive 4-part technical blog posts across sequential stages: Stage 1 creates sectional outlines, Stages 2 through 4 draft dedicated co... |
| [`taxonomy-ui-component-architect`](./taxonomy-ui-component-architect) | `taxonomy-ui-component-architect` | Synthesize, generate, and map comprehensive, optimized UI component architectures and interface tree maps directly from backend data taxonomies, entity schemas,... |
| [`ui-component-taxonomy-architect`](./ui-component-taxonomy-architect) | `ui-component-taxonomy-architect` | Architect, generate, and optimize comprehensive data taxonomies, entity schemas, and identifier hierarchies tailored directly to UI component maps for BEJSON 10... |

### Layer 6: L5_Composition_Root (12 skills)

| Skill Directory | Canonical Name | Purpose & Triggers |
| :--- | :--- | :--- |
| [`agy-skill-refactor`](./agy-skill-refactor) | `agy-skill-refactor` | Audit, refactor, modernize, and harmonize Antigravity CLI (agy) skills, prompt presets, and headless automation daemons. Enforces the 2026 Anti-Collision Constr... |
| [`arch-layered-refactor`](./arch-layered-refactor) | `arch-layered-refactor` | Root refactoring and architectural planning skill for decomposing monolithic, tangled, or legacy codebases into strict, decoupled layered architectures across t... |
| [`definitions-cartographer`](./definitions-cartographer) | `definitions-cartographer` | Index, query, resolve, and audit canonical ecosystem terminology, inline concept definitions (Policy §5.1), acronyms, and semantic speech-to-text aliases using ... |
| [`domain-cartography-coordinator`](./domain-cartography-coordinator) | `domain-cartography-coordinator` | Coordinate multi-domain architectural cartography and typing pipelines by scheduling turn delays, auditing skill DAGs, extracting ubiquitous terms, and routing ... |
| [`domain-scoped-coordinators`](./domain-scoped-coordinators) | `domain-scoped-coordinators` | Route and orchestrate autonomous multi-agent pipelines using global_dispatcher and domain-scoped coordinators across Phase 1 (Goal Formulation & Gatekeeping via... |
| [`file-archive-coordinator`](./file-archive-coordinator) | `file-archive-coordinator` | Coordinate session initialization maintenance and archive retention by sweeping download directories for project packages, parsing solid integer versions, compr... |
| [`project-delivery-packager`](./project-delivery-packager) | `project-delivery-packager` | Package and deliver compliant project releases by incrementing package versions, generating Versioned_UUID and file-level RELATIONAL_IDs, enforcing .beignore ru... |
| [`skill-architect`](./skill-architect) | `skill-architect` | Design, scaffold, validate, and register multi-tier Antigravity CLI (agy) agent skills enforcing the 6-Tier Layered Skill Architecture (L1-L6), unidirectional d... |
| [`skill-chain-coordinator`](./skill-chain-coordinator) | `skill-chain-coordinator` | Orchestrate multi-skill Directed Acyclic Graph (DAG) execution flows, manage stage state transitions, delegate isolated subagent handoffs, and enforce determini... |
| [`skill-chain-recipe-composer`](./skill-chain-recipe-composer) | `skill-chain-recipe-composer` | Conceptualize, structure, and compose end-to-end skill chain recipes across the 6-tier architecture to reach desired outcomes. Evaluates target objectives again... |
| [`skill-ecosystem-cartographer`](./skill-ecosystem-cartographer) | `skill-ecosystem-cartographer` | Catalog installed Antigravity CLI (agy) skills across workspace, global, and plugin directories, map layer routing topologies, register input/output functional ... |
| [`spark-skill-refactor`](./spark-skill-refactor) | `spark-skill-refactor` | Audit, refactor, optimize, and harmonize existing Gemini Spark skills individually or in symbiotic clusters to enforce 6-tier layer boundaries, progressive disc... |

---

## 3. Maintenance, Audits & Verification

All consolidation tracking artifacts reside in [`dev/`](./dev/):
- [`dev/checklist-20261023-235528.md`](./dev/checklist-20261023-235528.md): Granular execution checklist & verification audit.
- [`dev/change-log.md`](./dev/change-log.md): Record of deduplication, superset merges, and reference repairs.
- [`dev/variable_naming_issues.md`](./dev/variable_naming_issues.md): Tracked naming and namespace observations.
- [`dev/security-notes.md`](./dev/security-notes.md): Security considerations and observations.

