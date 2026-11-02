# Council Deliberation Framework & Perspectives

> **Skill**: `council-advise` (Layer 5 Council Advisor & Iterative Planner)  
> **Author**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Release_Version**: 300 | **Schema**: BEJSON 104a

---

## 1. The Four Council Voices

Whenever complex architectural choices, system expansions, refactors, or multi-step initiatives are presented, `council-advise` convenes four distinct analytical perspectives to review the grounded operational state from `council-grounding`:

### 1.1 The Substrate Guardian (Data Invariants & Standard Integrity)
- **Primary Focus**: Data durability, schema invariance, and Policy Section 6.2 / Section 10 compliance.
- **Key Invariants**:
  - Mandatory O(1) Field Map Caching (`field_map = {f['name']: idx for idx, f in enumerate(doc['Fields'])}`). Positional row indexing (`row[i]`) is rejected.
  - Boundary whitespace sanitization on all dictionary keys and table cells (Policy Section 10.9).
  - Era isolation: `libraries_104` (stable, frozen core) vs `libraries_105` (development).
  - Spatial quantization: BEHTML 8-lane/16-sublane grid, Ry=32px, and BECSS Tri-Color (`#000000`, `#FFFFFF`, `#DE2626`).

### 1.2 The Ecosystem Architect (Ecosystem Hierarchy & Registry Supremacy)
- **Primary Focus**: 6-Tier Layered Skill Architecture (L1-L6) and environment store governance.
- **Key Invariants**:
  - Canonical Environment Store: All paths resolve from `definitions.json` (canonical source of truth replacing deprecated `paths.json`).
  - Pre-existing Type Supremacy: Canonical Project Type Ledger (`project_type_ledger.104a.bejson`) must be queried before declaring or assigning types.
  - Project Chunker Engine: `$PROJECT_CHUNKER` governs tracking, chunking, and verified atomic scooping (`--scoop`).
  - Unidirectional Downward Dependencies: Upper layers invoke lower layers; lower layers never know about upper layers.

### 1.3 The Operational Strategist (Historical Context & System Trajectory)
- **Primary Focus**: Contextual continuity, past mistakes avoidance, and long-term momentum.
- **Key Invariants**:
  - Global Daily Logs Sink: Studies `$GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson` entries to see what was just finished, what broke, and what needs consolidation.
  - Incremental Progress: Avoid massive risky leaps; deliver modular, versioned packages (`Name_Case-V#-PKG#`).
  - Dual-Path Secure Logging: Ensures sensitive secrets are never logged to public sinks.

### 1.4 The Tactical Executor (Surgical Delivery & Verification Gates)
- **Primary Focus**: Feasibility, definition of done (DoD), and execution safety.
- **Key Invariants**:
  - Surgical Scope: Modify only requested targets; match existing code style without refactoring adjacent files.
  - Automated Stage Gates: Every plan must have a machine-executable verification assertion (linter, unit test, exit code 0).
  - Atomic File Replacements: All file writes proceed via `.tmp` -> flush -> `fsync` -> `replace`.

---

## 2. Deliberation Synthesis & Trade-Off Matrix

For every proposal, the council synthesizes a 3-option tradeoff assessment:
1. **Conservative Option**: Minimal changes, zero external dependencies, maximum backward compatibility.
2. **Balanced Option (Recommended)**: Clean architectural alignment, modern standard compliance, automated DoD verification.
3. **Pioneering Option**: Full migration to newest patterns, deeper modularization, higher upfront effort.
