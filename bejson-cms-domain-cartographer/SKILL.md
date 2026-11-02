---
name: bejson-cms-domain-cartographer
description: >-
  Discover, catalog, and map BEJSON CMS platform microservices, route blueprints, dynamic page templates, content databases, and static export pipelines into cms_service_map.104a.bejson. Maps service dependencies across standalone BEJSON_CMS and tools/NA-CMS. Use when discovering installed CMS microservices, mapping CMS route endpoints, cataloging CMS data stores (pages_db, posts_db, media_db), or generating holistic CMS architectural service topologies. Do NOT use for BEHTML spatial layout cartography (use behtml-domain-cartographer), MFDB cluster mapping (use mfdb-domain-cartographer), grounding CMS architecture or code inspections (use project-bejson-cms-grounding), active CMS operational management (use project-bejson-cms-manage), drafting blog content (use bejson-cms-blog-writer), scouting blog post ideas (use bejson-cms-admin-scout), or compiling and publishing static sites (use bejson-cms-publish-automator).
---

# bejson-cms-domain-cartographer (Layer 6 CMS Architecture & Service Cartographer)

## Summary

`bejson-cms-domain-cartographer` is the authoritative Layer 6 platform discovery and topological mapping engine for the zero-SQL BEJSON CMS ecosystem. It surveys both the standalone application (`BEJSON_CMS`) and the embedded platform (`tools/NA-CMS`) to catalog microservice blueprints, HTTP route controllers, dynamic HTML layout skeletons, underlying BEJSON/MFDB stores (`pages_db`, `posts_db`, `media_db`), and static publication export targets into `data/cms_service_map.104a.bejson`.

## When to Use

- Discovering installed CMS installations, extensions, and microservice components across repositories.
- Constructing or refreshing the canonical `data/cms_service_map.104a.bejson` ledger.
- Mapping Flask blueprint endpoints, REST routes, and content dispatch handlers.
- Cataloging CMS database stores, tracking entity counts, and verifying schema alignment.
- Preparing comprehensive system dependency inventories before CMS migrations or major releases.

## When NOT to Use

- Do NOT use for grounding, code inspection, or structural navigation of the CMS codebase (use `project-bejson-cms-grounding`).
- Do NOT use for active operational runtime commands like starting daemons or adding users (use `project-bejson-cms-manage`).
- Do NOT use for authoring, editing, or combining 4-part blog publication content (use `bejson-cms-blog-writer`).
- Do NOT use for scanning Admin repositories to discover active development topics (use `bejson-cms-admin-scout`).
- Do NOT use for automating static site builds, preview server binding, or screenshot capture (use `bejson-cms-publish-automator`).

---

## 1. Layer Boundary & Dependency Contract

- **Assigned Skill Tier**: Layer 6 (`L6: Root Orchestration & Meta-Governance`)
- **Codebase Layer Mapping**: `L5_Composition_Root`
- **Exclusive Write-Owner Of**: `data/cms_service_map.104a.bejson`
- **Allowed Downward Dependencies**: `project-bejson-cms-grounding` (L5), `mfdb-104-core` (L1), `bejson-format-core` (L1)
- **Output Artifact Spec**: BEJSON 104a Service Map document and Markdown topology summaries.
- **BEJSON Access Policy**: All reads and writes enforce O(1) `field_map` lookups and boundary whitespace sanitization.

---

## 2. Step-by-Step CMS Discovery Workflow

### Step 1: Platform Directory Scan
Execute the cartographer script to discover CMS modules, endpoints, and data stores:

```bash
python3 scripts/bejson_cms_cartographer.py \
  --scan-root "/storage/emulated/0/Admin" \
  --catalog "data/cms_service_map.104a.bejson" \
  --report "reports/cms_service_topology.md"
```

### Step 2: Route & Store Graph Construction
The cartographer:
- Parses Flask blueprints (`@app.route`, `@bp.route`) and extracts HTTP methods.
- Maps database stores (`data/*.bejson`, `pages_db.bejson`, `posts_db.bejson`).
- Resolves template dependencies and static distribution targets.
- Compiles service health status and route counts.

### Step 3: Registry Synchronization
Atomically writes discovered services into `data/cms_service_map.104a.bejson` and emits an executive service map summary in Markdown.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
