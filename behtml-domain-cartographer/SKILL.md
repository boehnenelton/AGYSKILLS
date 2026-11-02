---
name: behtml-domain-cartographer
description: >-
  Scan, discover, catalog, and map BEHTML spatial interfaces, 8-lane / 16-sublane coordinate allocations, Ry=32px row quantization boundaries, OptionSets, and component schemas across project trees into behtml_spatial_registry.104a.bejson. Generates spatial allocation maps and identifies layout boundary anomalies. Use when discovering installed BEHTML templates, mapping spatial interface structures, cataloging OptionSets across projects, or generating holistic BEHTML spatial routing topologies. Do NOT use for CMS platform service cartography (use bejson-cms-domain-cartographer), MFDB cluster mapping (use mfdb-domain-cartographer), raw coordinate math or element schemas (use behtml-format-core), building and composing individual 18-field BEHTML layouts (use behtml-layout-builder), validating low-level coordinate quantization (use behtml-schema-validator), static asset bundling (use behtml-scaffold-automator), or CSS design token specifications (use behtml-design-preferences).
---

# behtml-domain-cartographer (Layer 6 Spatial Interface & Layout Cartographer)

## Summary

`behtml-domain-cartographer` is the authoritative Layer 6 spatial topology and layout discovery engine for the BEHTML ecosystem. It surveys software projects, repositories, and documentation trees to catalog and index all BEHTML layout files, OptionSet definitions, 18-field `BEHTMLElement` datasets, and responsive breakpoints. It maintains the canonical spatial registry `data/behtml_spatial_registry.104a.bejson`, verifying global alignment with Elton Boehnen's 8-lane horizontal grid ($W_{lane} = 12.5\%$, half-cell $= 6.25\%$) and $R_y = 32\text{px}$ vertical row quantization standards.

## When to Use

- Scanning project workspaces to discover and catalog all existing BEHTML files and components.
- Constructing or refreshing the canonical `data/behtml_spatial_registry.104a.bejson` ledger.
- Generating cross-project spatial topology maps and coordinate allocation summaries.
- Detecting unmapped OptionSets or orphaned spatial components across repository directories.
- Preparing comprehensive spatial inventories prior to multi-page refactoring or compilation.

## When NOT to Use

- Do NOT use for low-level 8-lane coordinate math, half-cell formulas, or format primitive schemas (use `behtml-format-core`).
- Do NOT use for assembling, styling, or rendering individual 18-field `BEHTMLElement` records or page layouts (use `behtml-layout-builder`).
- Do NOT use for validating structural integrity, DOM collisions, or error codes 300-329 (use `behtml-schema-validator`).
- Do NOT use for compiling static asset bundles or injecting Tri-Color CSS tokens (use `behtml-scaffold-automator`).
- Do NOT use for specifying visual BECSS styling, typography, or `#DE2626` color tokens (use `behtml-design-preferences`).

---

## 1. Layer Boundary & Dependency Contract

- **Assigned Skill Tier**: Layer 6 (`L6: Root Orchestration & Meta-Governance`)
- **Codebase Layer Mapping**: `L5_Composition_Root`
- **Exclusive Write-Owner Of**: `data/behtml_spatial_registry.104a.bejson`
- **Allowed Downward Dependencies**: `behtml-format-core` (L1), `behtml-schema-validator` (L2), `bejson-format-core` (L1)
- **Output Artifact Spec**: BEJSON 104a Spatial Registry document and Markdown topology summaries.
- **BEJSON Access Policy**: All reads and writes enforce O(1) `field_map` lookups and boundary whitespace sanitization.

---

## 2. Step-by-Step Spatial Discovery Workflow

### Step 1: Workspace Scan & Spatial Extraction
Run the embedded cartographer CLI to recursively scan target directories for BEHTML documents:

```bash
python3 scripts/behtml_spatial_cartographer.py \
  --scan-root "/path/to/target/project" \
  --catalog "data/behtml_spatial_registry.104a.bejson" \
  --report "reports/behtml_spatial_topology.md"
```

### Step 2: OptionSet & Schema Ingestion
The cartographer analyzes discovered documents for:
- Document Type (e.g. Standard Page, Document with Shelf, Feed, Dashboard).
- Active OptionSet bindings (`SCHEMA_OPTIONSET_v1`).
- Total element count, layer depth, and row quantization bounds ($R_y = 32\text{px}$).
- Coordinate extents across X lanes (1..8) and Y rows.

### Step 3: Registry Synchronization & Reporting
Discovered interfaces are serialized atomically into `data/behtml_spatial_registry.104a.bejson` using standard BEJSON 104a format with field map caching, and an executive Markdown topology report is written to `reports/`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
