---
name: project-chunker-archiver
description: >-
  Automate verified project archiving, snapshotting, atomic scoop-and-wipe, and multi-version tracking using Project_Chunker and BEJSON 104a snapshot containers. Sweeps and processes project directories and release ZIPs, detects and registers canonical project types (python, bash, react, skill, website, app, library) from the Type Ledger and statuses (Active, Inactive, Archived), executes 100% byte-verified atomic scoops, and manages the master projects registry. Use when archiving projects, chunking codebases into portable BEJSON snapshots, scooping verified directories, defining version/pkg overrides, or restoring project releases from snapshots. Do NOT use for raw single-file table CRUD (use bejson-104-core) or MFDB manifest editing (use mfdb-104-core).
---

# project-chunker-archiver (Layer 6 Verified Project Archiving & Snapshot Management)

## Summary

`project-chunker-archiver` operates at Layer 6 (`L6_Composition_Root`) to provide tamper-evident, zero-SQL project archiving and lifecycle management backed by Elton Boehnen's `Project_Chunker` and the `lib_bejson_Projects_*` library family. It transitions archiving from loose ZIP drops to byte-verified BEJSON 104a snapshot containers (`.bejson`), multi-version tracker databases, and a queryable master registry with first-class **Type** (conforming to the Canonical Project Type Ledger) and **Status** (Active, Inactive, Archived, Legacy) governance.

## When to Use

- Archiving projects or packages with verified byte-for-byte SHA-256 integrity before source deletion.
- Converting project directory trees or incoming release ZIPs into single-file BEJSON 104a snapshot containers.
- Scooping source directories (`--scoop`) with atomic wipe only after verification against stored snapshots.
- Querying, filtering, and listing registered project releases by **Type** (`--filter-type python`, `--filter-type bash`, etc.) and **Status** (`--filter-status Active`, `--filter-status Archived`).
- Overriding or manually defining project version (`-V`, `--ver`, `--project-version`), package version (`-P`, `--pkg`, `--package`), project type (`--type`), or status (`--status`) on the CLI.
- Updating metadata on existing registered projects (`--set-version`, `--set-pkg`, `--set-type`, `--set-status`).
- Lossless restoration (`--restore <UUID>`) of archived codebases to original paths or new destinations.

## When NOT to Use

- Do NOT use for basic loose ZIP directory sweeping without chunking (use `file-archive-coordinator` for initial download sorting).
- Do NOT use for raw single-file BEJSON CRUD operations without project manifests (use `bejson-104-core`).
- Do NOT use for multi-file MFDB database manifest linkage and schema federation (use `mfdb-104-core`).
- Do NOT use for generic 3-phase autonomous task loops (use `domain-scoped-coordinators`).

---

## 1. Architectural Invariants & Policy Grounding

- **Pre-Existing Type Supremacy (Policy Directives)**: All project types must query and reuse pre-existing types from the Canonical Project Type Ledger (`$PROJECT_TYPE_LEDGER` -> `/storage/emulated/0/Admin/Dev/Policy/project_type_ledger.104a.bejson`): `python`, `bash`, `react`, `website`, `app`, `skill`, `powershell`, `angular`, `android_app`, `library`.
- **Status Field Governance**: Tracker schemas mandate `Status` with standardized values: `Active`, `Inactive`, `Archived`, `Legacy`.
- **Zero-SQL 3-Pillar Persistence**:
  1. **Master Registry** (`storage/master/data/registry.bejson`): Maps `Versioned_UUID` to `Project_Name`, `Tracker_File`, `Project_Version`, `Package_Version`, `Original_Path`, `Snapshot_File`, `Status`, `Updated_At`, and `Type`.
  2. **Tracker Database** (`storage/trackers/data/<project>.bejson`): Multi-version history of project manifests.
  3. **Snapshot Chunks** (`storage/project_snapshots/<project>/data/*.bejson`): Serialized file trees with SHA-256 digests and base64 binary encoding.
- **Atomic Scoop Guarantee**: The `--scoop` command serializes the snapshot to disk, reloads it from disk, executes a 100% byte-for-byte comparison against live files, and only unlinks the source directory after parity is proven.
- **Dynamic Pathing & Zero Hardcoding**: Storage roots and ledger paths resolve from environment variables (`PROJECT_CHUNKER_STORAGE_ROOT`, `PROJECT_TYPE_LEDGER`, `INTERNAL_STORAGE`) or portable relative script anchors.

---

## 2. Core Workflows & CLI Reference

All commands run through the Project_Chunker CLI engine located at `$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py` (or through the companion script launcher).

### 2.1 Full Verified Archive & Scoop (`--scoop`)
To archive a project directory, verify it against the chunk snapshot, and safely remove the source files:
```bash
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" /path/to/MyTool-V2-PKG10 --scoop
```

### 2.2 Archiving with Type and Status Specification
Specify or override project type and status explicitly:
```bash
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" /path/to/MyTool-V2-PKG10 --scoop --type python --status Active
```

### 2.3 Manual Version & Package Definition
When source directories or ZIPs lack versioned folder names or trackers, manually specify version and package numbers:
```bash
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" /path/to/my_unversioned_tool --scoop --name MyTool -V 102 -P 10
```

### 2.4 Zip Intake & Verification
Process release ZIPs, verify content, index tracker, generate snapshot chunk, and safely remove the ZIP:
```bash
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" /path/to/MyTool-V2-PKG10.zip --identity-from-filename
```

### 2.5 Querying & Filtering Registry
Filter registered releases by project type or lifecycle status:
```bash
# Filter all Python projects
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" --list --filter-type python

# Filter all Archived projects
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" --list --filter-status Archived

# View versions for a specific project
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" --versions MyTool --filter-status Active
```

### 2.6 Updating Registered Project Metadata
Update status, type, version, or pkg on an existing registered entry by UUID (or prefix >= 8 chars):
```bash
# Mark a release as Archived
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" <UUID_OR_PREFIX> --set-status Archived

# Update project type
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" <UUID_OR_PREFIX> --set-type bash

# Manually update version or pkg
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" <UUID_OR_PREFIX> --set-version 103 --set-pkg 12
```

### 2.7 Restoring an Archived Project
Deploy a snapshot back to its original location or a custom destination:
```bash
# Restore to original recorded location
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" --restore <UUID_OR_PREFIX>

# Restore to custom destination
python3 "$PROJECT_CHUNKER_ROOT/CLI/project_chunker.py" --restore <UUID_OR_PREFIX> --dest /storage/emulated/0/Admin/Dev/Repos/RestoredTool
```

---

## 3. Storage Layout & Directory Structure

```
storage/
├── master/
│   └── data/
│       └── registry.bejson          # Central lookup registry (v3 schema with Type & Status)
├── trackers/
│   └── data/
│       └── <project_name>.bejson    # Multi-version manifest history per project
├── project_snapshots/
│   └── <project_name>/
│       └── data/
│           └── <project>-V<ver>-PKG<pkg>.bejson  # Single-file chunk containers
└── superseded/
    └── <project_name>/              # Pre-existing snapshots kept when replaced with differing content
```

---

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
