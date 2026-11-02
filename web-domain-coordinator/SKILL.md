---
name: web-domain-coordinator
description: >-
  Coordinate and orchestrate end-to-end website generation workflows across the Three-Domain Web Architecture: Domain 1 (The Taxonomy Planner via web-taxonomy-planner), Domain 2 (The Templator via web-large-architect / template-architect), and Domain 3 (The Framework Planner via web-framework-architect). Enforces the 3-phase handoff protocol, anti-collision boundaries, and stage-gate validation checks. When reverse-engineering or auditing existing live websites, delegates to the Decomposition Domain (ui-navigation-decomposer and web-ui-component-mapper). Use when executing end-to-end website creation pipelines, managing inter-domain handoffs, or validating architectural compliance across all three domains. Do NOT use for direct database field planning (use web-taxonomy-planner), direct HTML/CSS template design (use web-large-architect), or standalone route compilation (use web-framework-architect).
---

# Web Domain Coordinator (Triad Orchestrator)

The **Web Domain Coordinator** is the master orchestration skill for the **Three-Domain Web Architecture**. It guarantees that website creation adheres to strict domain separation, sequential stage gates, and anti-collision boundaries between **Taxonomy**, **Templates**, and **Web Frameworks**.

---

## 1. The Three-Domain Triad & The Decomposition Domain

```text
========================================================================================
                      DECOMPOSITION DOMAIN (ANALYSIS & REVERSE-ENGINEERING)
  - ui-navigation-decomposer: Traces & extracts live URL routing, menus, and site maps.
  - web-ui-component-mapper: Deconstructs existing UI interfaces into ASCII component trees.
========================================================================================
                                          │
                    (Optional: Used when analyzing existing sites)
                                          ▼
========================================================================================
                                THREE CREATION DOMAINS
========================================================================================

  ┌─────────────────────────────────┐
  │   DOMAIN 1: TAXONOMY PLANNER    │
  │     (web-taxonomy-planner)      │
  │  - Database Field Definitions   │
  │  - Category & Partition Trees   │
  │  - 104a.taxonomy_schema.bejson  │
  └────────────────┬────────────────┘
                   │
                   ▼ [Stage Gate 1: Verified Taxonomy Manifest]
  ┌─────────────────────────────────┐       ┌─────────────────────────────────┐
  │   DOMAIN 3: FRAMEWORK PLANNER   │ <──── │      DOMAIN 2: THE TEMPLATOR    │
  │    (web-framework-architect)    │       │      (web-large-architect)      │
  │  - 12 Invariant Laws            │       │  - Reusable Design Skeletons    │
  │  - Page-Style vs Feed-Style     │       │  - Horizontal Overflow Defense  │
  │  - Collapsible Sidebar Trees    │       │  - 8-Lane Grid & Ry=32px Rhythm │
  │  - 104a.web_framework.bejson   │       │  - Zero-Filler Skeletons        │
  │  - Physical Site Compilation    │       └─────────────────────────────────┘
  └─────────────────────────────────┘
```

---

## 2. The 3-Phase Execution Pipeline

When building or updating a multi-tier website, the Coordinator enforces this deterministic sequence:

### Phase 1: Taxonomy Definition (Domain 1)
- **Executor**: [`web-taxonomy-planner`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-taxonomy-planner/SKILL.md)
- **Input**: User product concept, domain vision, or entity list.
- **Actions**:
  1. Assign canonical entity prefixes (`<prefix>_field`).
  2. Define primitive types, UUIDs, titles, slugs, and timestamps.
  3. Classify tabular attributes (`"display_target": "table"`) for horizontal scroll tables.
  4. Design website taxonomy namespaces (`links`, `blog`, `wiki`, `docs`) and parent-child partition trees.
- **Gate 1 Verification**: Emits `104a.taxonomy_schema.bejson` and validates field map caching.

### Phase 2: Design File Verification & Overflow Hardening (Domain 2)
- **Executor**: [`web-large-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-large-architect/SKILL.md) & [`template-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-architect/SKILL.md)
- **Input**: Visual standards and responsive layout requirements.
- **Actions**:
  1. Select appropriate template scaffolds from the 13 canonical layouts.
  2. Verify that all templates enforce:
     - `.fw-docked-toolbar` with `overflow-x: auto; flex-wrap: nowrap;`.
     - `.fw-table-scroll` with `overflow-x: auto; max-width: 100%;`.
     - `.fw-sidebar-tree` with `<details class="fw-tree-node">` collapsed by default ("classified to fall").
     - `.fw-breadcrumb-rail` with `overflow-x: auto;`.
     - Strictly functional placeholders (`"Page Title"`, `"Section Heading"`, `"Body Paragraph text"`, zero filler).
- **Gate 2 Verification**: Templates pass the zero-filler linter.

### Phase 3: Framework Articulation & Compilation (Domain 3)
- **Executor**: [`web-framework-architect`](file:///data/data/com.termux/files/home/.gemini/config/skills/web-framework-architect/SKILL.md)
- **Input**: `104a.taxonomy_schema.bejson` (from Phase 1) + Template Catalog (from Phase 2).
- **Actions**:
  1. Assign **Page Style** to all non-blog taxonomies and **Feed Style** exclusively to `/blog/` (Law 3).
  2. Select Terminal Node Cardinality: `folder_index`, `flat_html`, `category_direct`, or `n_tier_folder` (Law 7).
  3. Bind design files to directory depths 0, 1, 2, 3+ (Law 8).
  4. Synthesize the default-collapsed sidebar tree with depth-relative links (Law 4).
  5. Compile isomorphic filesystem directory trees with `index.html` at every level (Laws 1 & 2).
  6. Execute the 7-point Framework Invariant Audit.
- **Gate 3 Verification**: `fw_compiler.py --validate` passes with 0 violations.

---

## 3. Strict Negative Constraints & Boundary Enforcement

The Coordinator enforces that no domain oversteps its boundaries:

| Domain | Allowed Responsibilities | Forbidden Actions (Negative Constraints) |
| :--- | :--- | :--- |
| **Domain 1: Taxonomy** | Database fields, entity prefixes, column types, logical taxonomy & category trees. | **NEVER** write CSS, HTML markup, or 8-lane grid rules. **NEVER** decide folder vs flat file routing. |
| **Domain 2: Template** | Visual design files, spatial containers, horizontal overflow defense, zero-filler skeletons. | **NEVER** model database columns or entity schemas. **NEVER** make website-wide directory or routing decisions. |
| **Domain 3: Framework** | Evaluates options, assigns page/feed styles, binds templates to depths, compiles filesystem. | **NEVER** invent database fields. **NEVER** design raw visual layouts or CSS from scratch. |
| **Decomposition Domain** | Reverse-engineering and analyzing existing websites, DOMs, or apps. | **NEVER** used for forward synthesis or compiling website architectures. |

---

## 4. Operational Script: `coordinate_web_triad.py`

This skill provides an automated pipeline runner at `scripts/coordinate_web_triad.py`:

```bash
# Run the complete 3-phase pipeline verification
python3 ~/.gemini/config/skills/web-domain-coordinator/scripts/coordinate_web_triad.py --verify-all
```
