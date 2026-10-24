---
name: file-archive-coordinator
description: >-
  Coordinate session initialization maintenance and archive retention by sweeping download directories for project packages, parsing solid integer versions, compressing loose directories into ZIPs, cataloging into the projects archive, and pruning duplicate builds. Use when running session initialization maintenance, sweeping download folders, compressing unzipped project drops, enforcing archive retention, or pruning duplicate builds. Do NOT use for generic 3-phase autonomous workflow pipelines (use domain-scoped-coordinators), single-skill DAG execution (use skill-chain-coordinator), or packaging codebases into single-file BEJSON text chunks (use chunking-core).
---

# file-archive-coordinator (Layer 6 Session Initialization Maintenance & Archive Retention)

## Summary

`file-archive-coordinator` operates at Layer 6 (`L6_Composition_Root`) to automate the session initialization maintenance sweep mandated by policy. It inspects `/storage/emulated/0/Download/` for `(PROJECT_NAME)-(VERSION)-(PKGVERSION)` packages and directories, compresses loose folders into ZIP archives, enforces retention rules by preserving only the latest build in the download station, moves prior releases to their dedicated `$PROJECTS_ARCHIVE_ROOT/<ProjectName>/` folder, and safely prunes duplicate builds using SHA-256 integrity verification.

## When to Use

- Executing session initialization maintenance sweeps across `/storage/emulated/0/Download/`.
- Parsing solid integer project versions and package identifiers (`Name_Case-V#-PKG#`).
- Compressing loose, unzipped project folders into standard ZIP archives before archiving.
- Cataloging historical project archives into `$PROJECTS_ARCHIVE_ROOT/<ProjectName>/`.
- Enforcing download retention (latest build retained in Download, older builds archived).
- Deduplicating and pruning identical intermediate builds across archives.

## When NOT to Use

- Do NOT use for generic 3-phase autonomous goal formulation and delivery (use `domain-scoped-coordinators`).
- Do NOT use for single-skill Directed Acyclic Graph (DAG) coordination (use `skill-chain-coordinator`).
- Do NOT use for packaging codebases into single-file BEJSON flat archives (use `chunking-core`).
- Do NOT use for multi-file MFDB container packing or mounting (use `mfdb-104-chunker`).

---

## 1. Architectural Invariants & Policy Grounding

- **Policy §1.1 & §3.1 Grounding**: All project packages must adhere to solid numeric versioning and mapping rules (`(PROJECT_NAME)-(VERSION)-(PKGVERSION)`).
- **Canonical Environment Paths**: Storage paths are resolved dynamically from `/storage/emulated/0/.env/user/paths.json` (`PROJECTS_ARCHIVE_ROOT` and `INTERNAL_STORAGE`). Never hardcode directory paths in runtime business logic.
- **Embedded Tooling**: Operations are driven by the deterministic Python tool [`scripts/project_archive_janitor.py`](./scripts/project_archive_janitor.py).
- **CLI Launcher**: Globally runnable via [`~/.local/bin/project-archive-janitor`](file:///data/data/com.termux/files/home/.local/bin/project-archive-janitor).

---

## 2. Step-by-Step Operational Procedure

### Step 1: Package Discovery & Regex Matching
1. Query `DOWNLOAD_ROOT` for files and directories matching:
   ```regex
   ^(?P<project_name>[A-Za-z0-9_]+)-V(?P<version>[0-9_]+)-PKG(?P<pkg_version>[0-9_]+)(?:-(?P<build>[0-9_]+))?(?P<archive_ext>\.zip)?$
   ```
2. Group discovered packages by canonical project name.

### Step 2: Loose Directory Compression
1. For any loose directory matching the package pattern, compile into a `.zip` archive using `zipfile.ZipFile(..., zipfile.ZIP_DEFLATED)`.
2. Purge the uncompressed directory only after successful archive generation.

### Step 3: Version Ordering & Download Retention
1. Sort project packages ascending by `(version_tuple, package_tuple, build_number, mtime)`.
2. Designate the highest entry as the **active latest version**.
3. Retain the active latest version in `/storage/emulated/0/Download/`.

### Step 4: Archive Relocation & Deduplication
1. For each older version:
   - Check if an identical file exists in `/storage/emulated/0/Admin/Core/Projects_Archive/<ProjectName>/`.
   - Compute SHA-256 checksums:
     - If checksum matches: safely prune the duplicate from Download.
     - If filename collides but checksum differs: append microsecond disambiguation timestamp.
     - If unique: atomically move the file into the project's archive folder.

---

## 3. CLI Command Reference

* **Simulate Sweep (Dry-Run Mode):**
  ```bash
  project-archive-janitor --dry-run
  ```
* **Execute Full Maintenance Sweep:**
  ```bash
  project-archive-janitor --sweep
  ```
* **Inspect Active Configuration & Paths:**
  ```bash
  project-archive-janitor --config
  ```
* **Display Version & Author Metadata:**
  ```bash
  project-archive-janitor --version
  ```

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
