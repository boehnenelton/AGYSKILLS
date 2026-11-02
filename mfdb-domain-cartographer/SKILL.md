---
name: mfdb-domain-cartographer
description: >-
  Traverse, discover, catalog, and map federated Multi-File Database (MFDB) clusters across repositories into mfdb_topology_registry.104a.bejson. Identifies manifests (104a.mfdb.bejson and 105a.mfdb.bejson), maps Parent_Hierarchy relationships, foreign-key (_fk) referential graphs, and entity table locations across filesystems. Use when discovering installed MFDB clusters, mapping parent-child database manifests, indexing multi-file databases across projects, or auditing federated entity graph topologies. Do NOT use for BEHTML spatial layout cartography (use behtml-domain-cartographer), CMS platform service mapping (use bejson-cms-domain-cartographer), editing 104a manifest files (use mfdb-104-core), mutating Format 105 manifests and records (use mfdb-105-core), validating cross-entity foreign-key referential integrity (use mfdb-105-validator), packaging single-file .mfdb132 containers (use mfdb-104-chunker), or coordinating whole-database 104 to 105 migrations (use mfdb-105-upgrade-coordinator).
---

# mfdb-domain-cartographer (Layer 6 Federated Database & Cluster Cartographer)

## Summary

`mfdb-domain-cartographer` is the authoritative Layer 6 topological discovery and mapping engine for Elton Boehnen's Multi-File Database (MFDB) architecture across Foundational Era (v1.31/v1.39) and Integrity Era (v1.40). It traverses directories, repositories, and storage partitions to discover database manifests (`104a.mfdb.bejson` and `105a.mfdb.bejson`), linking physical entity tables to their master manifests, resolving bidirectional `Parent_Hierarchy` linkages, and constructing multi-plane referential graphs into `data/mfdb_topology_registry.104a.bejson`.

## When to Use

- Scanning workspaces or system paths to locate all active MFDB database clusters.
- Constructing or refreshing the canonical `data/mfdb_topology_registry.104a.bejson` catalog.
- Auditing bidirectional Parent_Hierarchy links and Master-Slave network topologies across disparate directories.
- Mapping entity table distributions and identifying unmanifested or orphaned `.bejson` tables.
- Preparing global cross-database dependency reports prior to migrations or version upgrades.

## When NOT to Use

- Do NOT use for direct CRUD operations on Foundational Era 104a.mfdb manifests (use `mfdb-104-core`).
- Do NOT use for direct CRUD operations or cell AES-GCM encryption on Integrity Era 105a.mfdb manifests (use `mfdb-105-core`).
- Do NOT use for validating cross-entity foreign-key referential cascades or E30-E39 errors (use `mfdb-105-validator`).
- Do NOT use for collapsing databases into single-file `.mfdb132.bejson` chunk containers (use `mfdb-104-chunker`).
- Do NOT use for orchestrating atomic 104-to-105 database upgrade pipelines (use `mfdb-105-upgrade-coordinator`).

---

## 1. Layer Boundary & Dependency Contract

- **Assigned Skill Tier**: Layer 6 (`L6: Root Orchestration & Meta-Governance`)
- **Codebase Layer Mapping**: `L5_Composition_Root`
- **Exclusive Write-Owner Of**: `data/mfdb_topology_registry.104a.bejson`
- **Allowed Downward Dependencies**: `mfdb-104-core` (L1), `mfdb-105-core` (L1), `mfdb-105-validator` (L2), `bejson-format-core` (L1)
- **Output Artifact Spec**: BEJSON 104a Topology Registry document and Markdown cluster maps.
- **BEJSON Access Policy**: All reads and writes enforce O(1) `field_map` lookups and boundary whitespace sanitization.

---

## 2. Step-by-Step MFDB Discovery Workflow

### Step 1: Multi-Directory Manifest Sweep
Execute the cartographer script to discover all database manifests and entity stores:

```bash
python3 scripts/mfdb_topology_cartographer.py \
  --scan-root "/storage/emulated/0/Admin" \
  --catalog "data/mfdb_topology_registry.104a.bejson" \
  --report "reports/mfdb_cluster_topology.md"
```

### Step 2: Referential Graph Compilation
The cartographer:
- Parses manifest header fields (`Database_Name`, `Database_Version`, `Network_Role`).
- Resolves each entry in `Entities` to its filesystem target.
- Identifies foreign-key (`_fk`) columns and maps cross-table links.
- Classifies database era (`v1.31_Foundational_104` vs `v1.40_Integrity_105`).

### Step 3: Registry Synchronization
Serializes all discovered clusters atomically into `data/mfdb_topology_registry.104a.bejson` and emits an executive cluster overview report in Markdown.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
