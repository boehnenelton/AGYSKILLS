---
name: mfdb-multi-architect
description: >-
  Architect, plan, and scaffold Multi-File Database (MFDB) topologies, federated
  multi-manifest clusters, and relational entity schemas across Python, JavaScript,
  TypeScript, and Bash. Merges centralized single-site master architectures with
  decentralized multi-domain federations, canonical prefix registries, synthetic
  UUID standards, bidirectional Parent_Hierarchy links, Network_Role governance
  (Master, Slave, Proxy, Standalone), and coordinate pointer resolution. Use when
  designing multi-file databases, planning federated data topologies, structuring
  multi-manifest clusters, modeling cross-file relational entity graphs, or generating
  administrative MFDB schemas. Do NOT use for low-level MFDB manifest CRUD (use
  mfdb-104-core), single-file 104 table operations (use bejson-104-core), black-box
  MFDB v1.40 FK validation (use mfdb-105-validator), single-file schema era allocation
  (use planning-schema-planner), or packaging MFDB containers (use mfdb-104-chunker).
---

# mfdb-multi-architect (Layer 5 Multi-File Database Architect & Topology Planner)

## Summary

`mfdb-multi-architect` is the canonical Layer 5 system architecture, planning, and design skill for Multi-File Databases (MFDB v1.31/v1.32/v1.40) and federated multi-manifest clusters. It merges and modernizes legacy single-system generators (`mfdb-system-architect`) and language-specific planners (`mfdb-python-architecture-planning`, `mfdb-javascript-architecture-planning`, `mfdb-typescript-architecture-planning`) into a unified, polyglot architectural design engine.

This skill establishes multi-plane storage topologies, bidirectional parent-child linkages, canonical snake_case naming taxonomies, synthetic UUID standards, zero-SQL relational graph projections, and deterministic manifest verification without daemon or B-tree overhead.

## When to Use

- Designing and planning multi-file databases, multi-manifest clusters, or federated data topologies before writing application code.
- Selecting between Centralized Single-Site Master, Federated Domain Clusters, or Hierarchical Proxy Mesh topologies.
- Defining canonical entity prefix registries (e.g., `page_`, `user_`, `asset_`, `sensor_`) and synthetic UUIDv4 primary/foreign key graphs.
- Structuring multi-plane storage architectures (Index Plane, Tracker Plane, Storage/Snapshot Plane, Superseded Conflict Plane).
- Generating production-ready MFDB manifests (`104a.mfdb.bejson`) and dense entity schemas (`data/<entity>.104.bejson`) with bidirectional `Parent_Hierarchy` handshakes.
- Designing zero-SQL relational graph workflows, event sourcing CQRS pipelines, cognitive multi-agent memory banks, or edge telemetry meshes.

## When NOT to Use

- Executing low-level CRUD operations on existing `104a.mfdb.bejson` manifests or entity tables (use `mfdb-104-core`).
- Manipulating standalone, single-file BEJSON 104/104a documents outside an MFDB cluster (use `bejson-104-core`).
- Validating Format 105 MFDB v1.40 cross-entity foreign key referential integrity and cascade rules (use `mfdb-105-validator`).
- Deciding between Foundational Era 104 and Integrity Era 105 for a single standalone file (use `planning-schema-planner`).
- Packaging or mounting single-file `.mfdb132.bejson` chunk containers (use `mfdb-104-chunker`).
- Decomposing monolithic application class hierarchies across the 6-tier architecture (use `arch-layered-refactor`).

---

## 1. Multi-MFDB Topology Selection Matrix

Before modeling schemas, resolve the database cluster topology based on coupling, write concurrency, and domain lifecycle boundaries:

| Topology Archetype | Directory Topology | Concurrency & Lock Scope | Primary Use Cases | Tradeoffs |
| :--- | :--- | :--- | :--- | :--- |
| **Topology A: Centralized Single-Site Master** | `storage/mfdb/104a.mfdb.bejson`<br>`data/<entity>.104.bejson` | Single PID lock per manifest; transactions lock entire database cluster | Content Management Systems (BEJSON CMS), blogs, desktop utilities, single-user tools | Simple joins and atomic backups; write bottleneck under high concurrent multi-worker loads |
| **Topology B: Federated Multi-Domain Cluster** | `storage/master/104a.mfdb.bejson`<br>`domains/<domain>/104a.mfdb.bejson`<br>`domains/<domain>/data/*.bejson` | Independent PID lock per domain manifest; zero cross-domain lock contention | Multi-tenant platforms, microservice event stores, e-commerce suites, multi-team workflows | Maximum write throughput; cross-domain joins require loading multiple manifests |
| **Topology C: Hierarchical Proxy Mesh** | `cluster/root.104a.mfdb.bejson`<br>`nodes/<node_id>/proxy.104a.mfdb.bejson`<br>`nodes/<node_id>/data/*.bejson` | Localized lock per edge node; master aggregates metadata asynchronously | Distributed edge telemetry, tactical field mesh, autonomous multi-agent swarms, IoT hubs | Offline autonomy and local resilience; requires eventual consistency reconciliation |

Detailed topological comparison charts reside in [`references/topology_and_taxonomies.md`](./references/topology_and_taxonomies.md).

---

## 2. Bidirectional Linkage & Network_Role Taxonomy

Multi-MFDB eliminates centralized database daemon catalogs by enforcing **Bidirectional Manifest Verification**:

```text
+-----------------------------------------------------------------------------+
|                          MULTI-MFDB FEDERATION GRAPH                        |
+-----------------------------------------------------------------------------+
                                       |
                     +-----------------+-----------------+
                     |                                   |
         [Root Manifest: Master]             [Audit Manifest: Master]
        104a.mfdb.bejson (Root Hub)         audit.mfdb.bejson (Security)
                     |                                   |
       +-------------+-------------+                     |
       |                           |                     |
  (Parent_Hierarchy)          (Parent_Hierarchy)    (Parent_Hierarchy)
       v                           v                     v
[Entity: Slave]             [Entity: Slave]       [Entity: Slave]
projects.104.bejson        trackers.104.bejson   access_log.104.bejson
```

### 2.1 The Network_Role Taxonomy
Every file in a Multi-MFDB cluster declares an explicit operational role in its root header:
- **`Master`**: Root orchestration manifest. Declares relative entity paths, schemas, and checksums. Never stores raw domain rows.
- **`Slave`**: Dense domain entity table (`Values`). Must point to its authoritative `Master` via `Parent_Hierarchy`.
- **`Proxy`**: Intermediate regional manifest. Acts as `Slave` to the cluster root while acting as `Master` to localized entity tables.
- **`Standalone`**: Self-contained autonomous table operating independently without parent mediation.

### 2.2 Error Code Governance (E30-E38)
All Multi-MFDB designs must halt deterministically on standard linkage violations:
- `E30 (E_MFDB_MISSING_MANIFEST)`: Manifest file missing at resolved path.
- `E31 (E_MFDB_INVALID_FORMAT_VERSION)`: Format version mismatch (e.g. `104a` vs `105a` without an era adapter).
- `E32 (E_MFDB_MISSING_RECORDS_TYPE)`: Missing required `Records_Type` declaration array.
- `E33 (E_MFDB_MISSING_FIELDS)`: Missing canonical `Fields` schema definition.
- `E34 (E_MFDB_MISSING_VALUES)`: Missing `Values` tabular matrix.
- `E35 (E_MFDB_UNRESOLVED_PARENT_HIERARCHY)`: Child `Parent_Hierarchy` path cannot be resolved on disk.
- `E36 (E_MFDB_CYCLIC_DEPENDENCY)`: Circular parent-child linkage detected ($A \to B \to C \to A$).
- `E37 (E_MFDB_NETWORK_ROLE_MISMATCH)`: Role contradiction (e.g. entity declares `Master` but registered as child `Slave`).
- `E38 (E_MFDB_UNREGISTERED_ENTITY)`: Entity exists on disk but is omitted from parent manifest.

Full linkage specifications reside in [`references/multi_mfdb_linkage_spec.md`](./references/multi_mfdb_linkage_spec.md).

---

## 3. Canonical Field Taxonomies & Prefix Registries

To guarantee cross-table readability, prevent namespace collisions, and enable zero-SQL equi-joins, all Multi-MFDB entity models must enforce the **Canonical Prefix Registry Standard**:

### 3.1 Prefix Mandate Rules
1. **Explicit 3-6 Character Prefix**: Every entity must possess an immutable lowercase prefix (e.g., `proj_`, `auth_`, `page_`, `task_`).
2. **Universal Column Prefixing**: Every column in the entity's `Fields` array must be `snake_case` prefixed by that entity's tag.
3. **Synthetic UUID Primary Keys**: Column 0 of every entity must be `<prefix>_uuid` (or `<prefix>_id`) containing an RFC 4122 Version 4 UUID. Natural keys (slugs, titles, usernames) are strictly prohibited as primary keys.
4. **Explicit Foreign Keys**: Foreign keys must reference the target entity using `<target_prefix>_uuid_fk` or `<target_entity>_uuid_fk` (e.g., `page_author_uuid_fk`).
5. **Timestamp Standards**: All timestamps must be UTC ISO-8601 strings (`YYYY-MM-DDTHH:MM:SSZ`) suffixed with `_created_at` or `_updated_at`.

### 3.2 Canonical Prefix Table Exemplar

```text
Entity Name           Prefix      Primary Key (Col 0)    Sample Fields
-----------------------------------------------------------------------------------------------------
ProjectMaster         proj_       proj_uuid              proj_name, proj_version, proj_status, proj_created_at
TrackerLineage        track_      track_uuid             track_proj_uuid_fk, track_pkg_ver, track_checksum
UserAccount           usr_        usr_uuid               usr_username, usr_email_hash, usr_role, usr_created_at
ContentPage           page_       page_uuid              page_title, page_slug, page_usr_uuid_fk, page_status
MediaAsset            asset_      asset_uuid             asset_filename, asset_sha256, asset_size_bytes
AuditEvent            audit_      audit_uuid             audit_usr_uuid_fk, audit_event_type, audit_timestamp
```

---

## 4. Multi-Plane Storage Architecture

For high-scale systems, data artifacts are segregated across four functional storage planes:

```text
storage/
├── master/                      # [Index Plane]
│   └── data/registry.bejson     # Global project catalogue, cluster routing, partition bounds
├── trackers/                    # [Tracker Plane]
│   └── data/<entity>.bejson     # Chronological append-only mutation history & version lineage
├── snapshots/                   # [Storage / Payload Plane]
│   └── <entity>/data/*.bejson   # Deep immutable snapshot chunks (V100-PKG100.bejson)
└── superseded/                  # [Collision Isolation Plane]
    └── <entity>/data/*          # Non-destructive quarantine for divergent concurrent mutations
```

- **Index Plane**: Fast $O(1)$ routing metadata. Never bloated with heavy domain payloads.
- **Tracker Plane**: Complete historical audit trail. Mutations append new rows; history is never destructively overwritten.
- **Storage Plane**: Content-addressed or version-partitioned snapshot chunks containing full entity payloads.
- **Superseded Plane**: Conflict isolation chamber. Conflicting multi-worker updates are quarantined without data loss.

---

## 5. Step-by-Step Multi-MFDB Design Workflow

Follow this five-step workflow when planning and architecting any Multi-MFDB system:

```text
+-------------------+     +--------------------+     +-------------------+
| Step 1: Select    | --> | Step 2: Establish  | --> | Step 3: Compile   |
| Cluster Topology  |     | Prefix Taxonomies  |     | Manifests & Links |
+-------------------+     +--------------------+     +-------------------+
                                                               |
                                                               v
+-------------------+     +--------------------+     +-------------------+
| Step 5: Execute   | <-- | Step 4: Scaffold   | <-- | Step 3b: Verify   |
| Stage Gate Linter |     | Service Substrate  |     | Cycle Freedom     |
+-------------------+     +--------------------+     +-------------------+
```

### Step 1: Select Cluster Topology
1. Evaluate domain isolation and concurrency requirements using the Topology Selection Matrix.
2. Define the cluster root directory structure (`config/`, `data/`, `storage/`, `dev/`, `docs/`).
3. Determine `Network_Role` assignments (`Master` for manifests, `Slave` for data tables).

### Step 2: Establish Canonical Prefix Taxonomies
1. List all relational entities (minimum 2 to 4 entities per MFDB cluster).
2. Assign unique 3-6 character prefixes to each entity.
3. Define synthetic UUIDv4 primary keys and explicit `_fk` foreign keys with cascade policies (`cascade`, `null`, `default`, `restrict`).

### Step 3: Compile Manifest and Entity Schemas
1. Build `104a.mfdb.bejson` root manifest declaring all entity tables in `Values`.
2. Construct each entity table with `Parent_Hierarchy: "../104a.mfdb.bejson"`.
3. Verify that the dependency graph forms a Directed Acyclic Graph (DAG) with zero circular references (E36).

### Step 4: Scaffold Service Substrate and Primitives
Run the bundled black-box scaffolder script to instantiate the complete Multi-MFDB directory tree and service engine:

```bash
python3 scripts/multi_mfdb_scaffolder.py \
  --topology "federated" \
  --name "Cognitive_Swarm_MFDB" \
  --entities "agents:agent_,memories:mem_,telemetry:telem_" \
  --output-dir "target/cognitive_swarm" \
  --validate
```

### Step 5: Execute Pre-Flight Stage Gate Verification
1. Run `mfdb-105-validator` (for 105 clusters) or `bejson-schema-validator` (for 104 clusters) to verify structural and referential integrity.
2. Confirm exit code `0` before proceeding to application service scaffolding or UI layer implementation.

---

## 6. Reference Shards & Blueprint Artifacts

For deep specifications and production reference implementations, consult these companion reference documents:

- **Linkage Specification**: [`references/multi_mfdb_linkage_spec.md`](./references/multi_mfdb_linkage_spec.md) (Bidirectional handshakes, E30-E38 error codes, coordinate pointer math, and cycle detection).
- **Topology & Taxonomies**: [`references/topology_and_taxonomies.md`](./references/topology_and_taxonomies.md) (Topological blueprints, prefix registries, and foreign key cascade semantics).
- **Production Systems Blueprints**: [`references/systems_blueprints.md`](./references/systems_blueprints.md) (Autonomous AI agent memory meshes, tactical edge field mesh, zero-SQL CQRS event stores, cryptographic audit ledgers, and polyglot plugin substrates).

---

## Credits & Attribution

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
