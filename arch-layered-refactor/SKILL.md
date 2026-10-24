---
name: arch-layered-refactor
description: >-
  Root refactoring and architectural planning skill for decomposing monolithic, tangled, or legacy codebases into strict, decoupled layered architectures across the 6-tier hierarchy. Orchestrates symbiotic skill handoffs across data persistence, domain logic, service ports, UI templates, and scaffolding without stepping on other skills' toes. Use when planning system-wide refactoring, structuring layered codebases, untangling circular dependencies, designing clean layer boundaries, or coordinating multi-skill refactoring workflows. Do NOT use for single-file BEJSON persistence refactoring (use bejson-codebase-refactor), Antigravity CLI prompt automation (use agy-prompt-automator), or isolated schema modeling (use planning-schema-planner).
---
# Layered Refactors

Acts as the root architectural planner and refactoring orchestrator for modern codebases. Decomposes tangled, monolithic, or tightly coupled systems into clean, unidirectional layered architectures. Coordinates specialized ecosystem skills symbiotically by establishing strict contract boundaries, preventing overlapping edits, and ensuring changes build progressively upon stable foundations.

## When to Use

- Planning a root-level refactoring for an existing codebase across Python, TypeScript, JavaScript, or Bash.
- Untangling monolithic files, spaghetti logic, circular imports, or mixed concerns (e.g. database queries embedded directly inside route handlers or UI templates).
- Establishing a clean layered architecture (Presentation -> Application -> Domain -> Persistence -> Substrate).
- Orchestrating multi-skill refactoring workflows where different skills handle data persistence, UI templates, scripting, and validation.
- Modernizing legacy application architectures while preserving functional equivalence and zero downtime.
- Preventing code collisions ("stepping on each other's toes") across concurrent refactoring tasks by locking lower-layer interfaces first.

## Modern 2026 Layered Architecture Principles

Modern codebase refactoring in 2026 combines classic layered architecture with ports-and-adapters and clean domain boundaries. Every refactored system must adhere to three foundational rules:

### 1. The 6-Layer Architectural Hierarchy

Codebases are structured into six explicit layers, ranked from innermost (most stable) to outermost (most volatile):

- **Layer 0: Substrate & Core Primitives (Innermost)**
  - *Scope*: Pure constants, primitive types, invariant assertions, custom error registries, and atomic I/O primitives.
  - *Dependency Rule*: Zero external dependencies. Cannot import any other layer in the application.
  - *Lifecycle*: Locked first; never changes during feature work.

- **Layer 1: Domain Entities & Schemas**
  - *Scope*: Business entity definitions, data schemas (e.g. BEJSON 104/104a/104db structures), field maps, and domain validation logic.
  - *Dependency Rule*: Depends exclusively on Layer 0. Never imports database drivers, web frameworks, or UI code.

- **Layer 2: Persistence & Infrastructure Adapters**
  - *Scope*: Repositories, manifest managers (e.g. MFDB v1.31/v1.32), atomic file storage handlers, cache adapters, and external client wrappers.
  - *Dependency Rule*: Implements domain contracts defined in Layer 1 using Layer 0 primitives. Does not know about HTTP requests or CLI commands.

- **Layer 3: Application Services & Use Cases**
  - *Scope*: Business workflow orchestration, transactional units, domain event dispatching, and multi-entity coordination.
  - *Dependency Rule*: Depends on Layer 1 (entities) and Layer 2 (persistence interfaces). Contains no presentation-specific formatting.

- **Layer 4: Presentation & Transport Adapters**
  - *Scope*: Web framework route controllers (e.g. Flask Blueprints, Express routes), CLI argument parsers, background job dispatchers, and UI templates (e.g. BEHTML/BECSS).
  - *Dependency Rule*: Thin translation layer. Validates transport inputs, calls Layer 3 use cases, and formats responses. Never contains business logic or direct database queries.

- **Layer 5: Composition Root & Runtime Bootstrap (Outermost)**
  - *Scope*: Application entry points (`main.py`, `server.js`, `importer.sh`), environment configuration loading, dependency injection, and process lifecycle management.
  - *Dependency Rule*: Wires together all lower layers and starts the system.

### 2. Strict Unidirectional Dependency Invariant

- Dependencies must flow strictly inward/downward: Layer N may depend on Layer N-1, but Layer N-1 must NEVER depend on Layer N.
- Upward imports and circular references are strictly prohibited.
- If Layer 2 needs to notify Layer 4, it must emit an event or return data through Layer 3; it must never directly call or import Layer 4.

### 3. Closed Layers vs. Open Substrates

- **Closed Layers (Strict Encapsulation)**: Layers 3 and 4 are closed. Layer 4 cannot bypass Layer 3 to query Layer 2 directly. Every user action must route through a defined application use case.
- **Open Substrate (Layer 0)**: Layer 0 is open. Any layer may import shared primitives (e.g. standard error codes, logging utilities, path sanitizers) without violating layered architecture.

## Symbiotic Skill Chaining Matrix

To prevent tools and skills from colliding or overwriting each other's progress, `arch-layered-refactor` serves as the root coordinator, delegating specific layer tasks to specialized skills according to this handoff protocol:

| Architectural Layer | Assigned Ecosystem Skill | Specific Responsibility & Handoff Contract |
|---|---|---|
| **Root Orchestration** | `arch-layered-refactor` | Audits system, defines layers, freezes contracts, plans migration sequence. |
| **Feature Cataloging** | `ideation-feature-composer` / `ideation-macro-composer` | Exhaustively inventories features and operational specs before refactoring begins. |
| **System Architecture** | `planning-schema-planner`<br>`component-taxonomy-architect` | Pre-plans database manifests, canonical prefix registries, synthetic UUID standards, and blueprints. |
| **Layer 0 & 1 (Data/Schemas)** | `bejson-104-core`<br>`bejson-105-core`<br>`mfdb-104-core` | Authors foundational BEJSON schemas, positional field orders, and manifest headers. |
| **Layer 2 (Persistence Refactor)** | `bejson-codebase-refactor` | Refactors legacy data structures (SQLite, raw JSON, CSV) into BEJSON with atomic I/O and field map caching. |
| **Layer 3 & 4 (Scaffolding)** | `bejson-scaffold-python`<br>`bejson-scaffold-javascript`<br>`bejson-scaffold-bash` | Generates self-contained scripts, service modules, CLI tools, and background workers with embedded primitives. |
| **Layer 4 (UI & Navigation)** | `ui-navigation-decomposer`<br>`behtml-layout-builder` | Maps UI navigation hierarchy and constructs deterministic spatial BEHTML grids and templates. |
| **Cross-Layer Validation** | `bejson-104-validator` / `bejson-105-validator` | Verifies structural integrity, manifest-entity paths, and schema parity across all boundaries. |

### Symbiotic Non-Interference Protocol

1. **Contract Freezing First**: Before modifying implementation code, author and lock the interface contracts (types, function signatures, return shapes, schema fields).
2. **Bottom-Up Migration**: Always stabilize lower layers before touching higher layers. Layer 1 schemas must pass validation before Layer 2 persistence is rewritten.
3. **Isolated Working Horizons**: When dispatching work to other skills or subagents, scope each assignment to a single layer. Never permit a presentation refactor task to alter database schemas.
4. **Anti-Corruption Layer (ACL)**: When refactoring a legacy module incrementally, wrap the legacy component with an adapter that exposes the new clean layer interface, allowing other layers to build cleanly without waiting for legacy internals to be fully rewritten.

## Step-by-Step Layered Refactoring Protocol

Follow this 6-stage workflow for every refactoring initiative:

### Stage 1: Codebase Audit & Triage

1. Inventory all files, modules, and entry points in the existing codebase.
2. Build a dependency matrix to identify tight coupling:
   - Where are database queries or file writes located?
   - Where are UI strings or formatting decisions made?
   - Are there circular dependencies or cross-module state mutations?
3. Classify all existing functions into target Layers (0 through 5).

### Stage 2: Contract & Interface Specification

1. Define the domain models and data transfer contracts (Layer 1).
2. Establish canonical prefix tags and synthetic UUID key standards for all entities.
3. Document the public interface signatures for Application Services (Layer 3) and Repositories (Layer 2).
4. Verify that interface parameters and return types use only primitive types or Layer 1 entities, never raw framework objects (e.g. Flask `request` or Express `req`).

### Stage 3: Layer 0 & 1 Substrate Stabilization

1. Extract shared constants, status codes, and error classes into `src/lib/substrate/` (Layer 0).
2. Author BEJSON schemas (104, 104a, 104db) and entity models in `src/domain/` (Layer 1).
3. Validate schemas using `bejson-104-validator` or `bejson-105-validator` to guarantee positional integrity and field typing.
4. Freeze Layers 0 and 1. Do not proceed until these contracts are verified.

### Stage 4: Layer 2 Persistence Modernization

1. Implement repositories and storage managers under `src/persistence/` or `src/lib/`.
2. Hand off storage refactoring to `bejson-codebase-refactor`:
   - Replace direct file writes with atomic routines (`.tmp` write -> `flush` -> `fsync` -> atomic rename).
   - Enforce dynamic field map caching (`bejson_core_get_field_map`) for row lookups.
   - Set up MFDB manifests (`104a.mfdb.bejson`) if using multi-file databases.
3. If legacy callers still exist, create an Anti-Corruption Adapter so old code paths continue to function without breaking.

### Stage 5: Layer 3 Application Service Extraction

1. Extract business logic from route handlers, CLI commands, or monolithic scripts into dedicated use cases in `src/services/`.
2. Ensure each use case performs a single, discrete business transaction:
   - Validates business rules against domain entities.
   - Calls Layer 2 repositories for persistence.
   - Returns clean entity records or result status objects.
3. Keep use cases completely decoupled from HTTP status codes, terminal escape sequences, or UI markup.

### Stage 6: Layer 4 Presentation Decoupling & Layer 5 Bootstrap

1. Refactor entry points, routes, and controllers in `src/web/` or `src/cli/` (Layer 4):
   - Controllers should only parse incoming parameters, validate types, call Layer 3 services, and map results to HTTP/JSON/CLI outputs.
   - For web frontends, delegate template construction to `behtml-layout-builder` and navigation mapping to `ui-navigation-decomposer`.
2. Wire all dependencies in the Composition Root (Layer 5, e.g. `app_admin.py` or `main.py`):
   - Load configuration (`ScriptConfig` in BEJSON 104a).
   - Instantiate repositories, pass them into application services, and register services into controllers.
3. Run end-to-end regression tests to verify full functional equivalence.

## Architectural Anti-Patterns and Gotchas to Avoid

- **The Leaky Route (Bypassing Layer 3)**: Never allow a route controller or CLI script to query a repository or write directly to a database file. All mutations must go through an application service.
- **Upward Reaching**: Never import a controller or web module from a service, repository, or domain file. If lower layers need to signal higher layers, use observer events, callbacks, or return values.
- **God Context Objects**: Avoid passing monolithic context objects (e.g. `app_state`, `global_ctx`, or raw web request objects) deep into inner layers. Pass only the specific, typed values required by the domain.
- **Premature Concurrency Overreach**: In single-threaded runtimes (Node.js) or constrained mobile environments (Android Termux / Pydroid 3), avoid multithreading or process forking. Use serial promise queues or single background daemon threads with explicit pacing delays and memory budgets.
- **Simultaneous Multi-Layer Editing**: Never refactor the presentation layer and persistence layer simultaneously without locked domain contracts. Doing so causes conflicting assumptions and broken interfaces.
- **Destructive Migration**: Never overwrite existing data files in place during refactoring. Always maintain fallback backups and write to new structures atomically with validation before swapping paths.
