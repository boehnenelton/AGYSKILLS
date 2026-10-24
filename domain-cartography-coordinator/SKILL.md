---
name: domain-cartography-coordinator
description: >-
  Coordinate multi-domain architectural cartography and typing pipelines by scheduling turn delays, auditing skill DAGs, extracting ubiquitous terms, and routing to Python, BEHTML, and Bash domain typers. Use when executing multi-domain architectural mapping, decomposing project visions into typed contracts, or orchestrating Python, BEHTML, and Bash domain typers. Do NOT use for generic 3-phase autonomous goal and delivery pipelines (use domain-scoped-coordinators), single-skill DAG execution (use skill-chain-coordinator), or cataloging installed skill topologies (use skill-ecosystem-cartographer).
---

# domain-cartography-coordinator (Layer 6 Multi-Domain Architectural Pipeline)

## Summary

`domain-cartography-coordinator` orchestrates the complete front-end decomposition of a high-level project vision into rigorous, multi-domain typed contracts prior to code generation. It integrates turn-delay scheduling, a tri-pillar cartography audit (skills, terms, domain types), dynamic stack routing, and domain-specialized typers for Python (Backend), BEHTML (Presentation), and Bash (Scaffolding).

## When to Use

- Ingesting a high-level project vision and decomposing it into typed architectural verticals before code generation.
- Running the tri-pillar cartography sequence: `skill_cartographer`, `terms_cartographer`, and `domain_type_cartographer`.
- Extracting ubiquitous language, entity prefixes, and semantic suffixes (`_metric`, `_timestamp`, `_flag`, `_fk`) across domains.
- Synthesizing structural contracts for Python backend services (`typing.Protocol`, BEJSON 104a schemas, `<family>_<component>_<verb>_<target>` signatures).
- Defining spatial layout contracts for BEHTML interfaces (8-lane / 16-sublane geometry, `Ry=32px` quantization, Policy §8.1 Tri-Color tokens).
- Constructing POSIX-compliant Bash scaffolding contracts (self-locating paths, atomic write primitives, standard CLI flags).

## When NOT to Use

- Do NOT use for generic 3-phase autonomous goal formulation and disk delivery (use `domain-scoped-coordinators`).
- Do NOT use for single-skill Directed Acyclic Graph (DAG) execution (use `skill-chain-coordinator`).
- Do NOT use for cataloging installed skills or auditing pairwise trigger collisions (use `skill-ecosystem-cartographer`).
- Do NOT use for raw single-table BEJSON CRUD (use `bejson-104-core` or `bejson-105-core`).
- Do NOT use for formatting standalone publication books or reports (use `publication-html-builder`).

---

## 1. Architectural Topology & Execution Graph

```
[Project Vision & Objective]
  │
  ▼
planning_coordinator (Layer 6: Turn-delay scheduling & phase orchestration)
  │
  ├── 1. skill_cartographer (Audits capabilities, identifies missing skills & tool DAG)
  ├── 2. terms_cartographer (Extracts ubiquitous language, entity prefixes & semantic suffixes)
  └── 3. domain_type_cartographer (Partitions the system into architectural verticals)
        │
        ▼
     domain_router (Evaluates domain stack & dispatches to specialized domain engines)
        │
        ├── [Domain A: Python / Backend]
        │     ├── python_cartography_terms (Python idioms, stdlib primitives, typing protocols)
        │     └── python_domain_typer
        │           ├── Interfaces & Protocols (structural contracts)
        │           ├── BEJSON Schemas (104/104a tabular definitions & field maps)
        │           ├── Function Signatures (<family>_<component>_<verb>_<target>)
        │           └── Classes & Managers (<Domain><Family><Subsystem><Role>)
        │
        ├── [Domain B: BEHTML / Presentation]
        │     ├── behtml_cartography_terms (8-lane coordinates, Ry=32px quantization, BECSS Tri-Color)
        │     └── behtml_domain_typer (BEHTMLElement spatial schemas, container templates)
        │
        └── [Domain C: Bash / Scaffolding]
              ├── bash_cartography_terms (POSIX constraints, jq primitives, exit codes)
              └── bash_domain_typer (CLI flags, environment variables, self-locating paths)
```

---

## 2. Component Specifications

### 2.1 Layer 6 Orchestrator & Tri-Pillar Cartographers

1. **`planning_coordinator`**:
   - Manages conversational turn-delay scheduling ($N = K + 1$) ensuring architectural contracts are fully frozen before code generation begins.
   - Gates downstream execution until all three cartography audits pass.
2. **`skill_cartographer`**:
   - Queries `skill-ecosystem-cartographer` to inspect installed tools across workspace, global, and plugin skill paths.
   - Detects capability gaps and flags missing tool or execution nodes before generation starts.
3. **`terms_cartographer`**:
   - Extracts ubiquitous domain terms using `definitions-cartographer` and `code-taxonomy-architect`.
   - Normalizes naming into Policy §6.1 Hierarchy-Group-Purpose standard: `<hierarchy_or_scope>_<group_or_domain>_<purpose_or_role>`.
   - Enforces canonical semantic suffixes: `_metric`, `_count`, `_timestamp`, `_flag`, `_fk`, `_url`.
4. **`domain_type_cartographer`**:
   - Analyzes project scope and partitions the architectural components into independent verticals: Backend (Python), Presentation (BEHTML), and Automation/Scaffolding (Bash).

### 2.2 Domain Router & Specialized Execution Engines

1. **`domain_router`**:
   - Evaluates the partition manifest from `domain_type_cartographer` and routes tasks to the corresponding specialized domain engines.
2. **Domain A: Python / Backend**:
   - **`python_cartography_terms`**: Maps standard library primitives (`pathlib.Path`, `logging`, `typing`), eliminates prohibited single-letter identifiers, and identifies required BEJSON family libraries.
   - **`python_domain_typer`**:
     - *Interfaces & Protocols*: Declares structural contracts using `typing.Protocol` and runtime validation.
     - *BEJSON Schemas*: Builds 104/104a tabular definitions with mandatory `FieldMap` O(1) cache mappings.
     - *Function Signatures*: Formats all routine signatures as `<family>_<component>_<verb>_<target>` (e.g., `lib_bejson_Core_validate_record_entry`).
     - *Classes & Managers*: Normalizes class names into `<Domain><Family><Subsystem><Role>` (e.g., `SwitchyardIngestQueueManager`).
3. **Domain B: BEHTML / Presentation**:
   - **`behtml_cartography_terms`**: Ingests visual tokens and spatial geometry rules from `behtml-design-preferences` and `behtml-104-builder`.
   - **`behtml_domain_typer`**:
     - *Spatial Constraints*: Restricts elements to 8-lane ($12.5\%$) or 16-sublane ($6.25\%$) columns with `Ry=32px` row quantization.
     - *Palette Enforced*: Policy §8.1 Tri-Color tokens (`#000000`, `#FFFFFF`, `#DE2626`).
     - *Templates*: Scaffolds zero-filler document, shelf, dashboard, or feed layout structures.
4. **Domain C: Bash / Scaffolding**:
   - **`bash_cartography_terms`**: Formulates shell standards: POSIX parameter expansions, Termux paths (`/data/data/com.termux/files/...`), and `jq` filter idioms.
   - **`bash_domain_typer`**:
     - *Path Bootstrap*: Generates self-locating script resolution functions (`get_script_path`) adhering to Policy §4.2.
     - *CLI Flags*: Scaffolds standard options: `--version`, `--config`, `--reset`, `--help` per Policy §4.7.
     - *Atomic Persistence*: Enforces `jq ... > tmp && mv -f` file write primitives.
     - *Exit Codes*: Embeds deterministic exit codes (`0` clean, `10` picker, `20` env, `30` schema error).

---

## 3. Operational Step-by-Step Procedure

### Stage 1: Ingestion & Tri-Pillar Cartography
1. `planning_coordinator` accepts the raw Project Vision & Objective.
2. `skill_cartographer` audits available skills and outputs a capability matrix.
3. `terms_cartographer` extracts ubiquitous terms, entity prefixes, and semantic suffixes into a Terms Manifest (`data/terms_manifest.104a.bejson`).
4. `domain_type_cartographer` outputs an architectural partition plan (`data/domain_partitions.104a.bejson`).

### Stage 2: Domain Router Dispatch
1. `domain_router` parses the partition plan and dispatches parallel sub-dossiers to active domains:
   - Python sub-dossier -> `python_domain_typer`
   - BEHTML sub-dossier -> `behtml_domain_typer`
   - Bash sub-dossier -> `bash_domain_typer`

### Stage 3: Type Synthesis & Contract Freezing
1. Each domain typer synthesizes strict typed contracts, schemas, and signatures.
2. `planning_coordinator` validates cross-domain referential integrity (e.g., Python backend schemas match BEHTML UI table columns and Bash CLI arguments).
3. The resulting **Architectural Type Dossier** is frozen in `exports/` and passed to code generators.

---

## 4. Mandatory Quality Gates

- **Zero-Filler Skeleton Law**: All generated templates and sample payloads must contain literal placeholder labels (`Title`, `Content Body`), never lorem ipsum or conversational fluff.
- **Strict GUID Prohibition**: Retain `"GUID_PLACEHOLDER"` in all generated project metadata. Never auto-assign global `Project_GUID`.
- **Field Map Cache Compliance**: All BEJSON manipulations across Python and Bash must use dynamic O(1) field map lookups. Positional row indexing (raw integer offsets) is strictly forbidden.
- **Negative Constraints Gate**: Ensure Python ≥ 3.10, standard `logging` (no `print()`), self-locating script paths, and Policy §8.1 Tri-Color tokens.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
