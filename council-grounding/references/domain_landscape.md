# Domain Landscape and Environmental Topology

> **Skill**: `council-grounding` (Layer 5 Grounding & Domain Cartographer)  
> **Author**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Release_Version**: 300 | **Schema**: BEJSON 104a

---

## 1. Canonical Ecosystem Domains

Elton Boehnen's software ecosystem is organized into tightly bounded, mutually reinforcing domains. The council must understand these architectural pillars before offering advisory suggestions or generating execution plans.

### 1.1 Data Substrate Domain (BEJSON & MFDB)
- **Foundational Era (libraries_104)**:
  - Formats: BEJSON 104, 104a, 104db, Nested 104, MFDB v1.31, MFDB v1.32.
  - Characteristics: Dense 2D arrays (`Fields` and `Values`), O(1) Field Map Cache (`field_map = {f['name']: idx for idx, f in enumerate(doc['Fields'])}`), boundary whitespace sanitization (Policy Section 10.9), atomic disk writes (`.tmp` -> flush -> `fsync` -> `replace`).
  - Strict Negative Constraints: Positional index access (`row[0]`) is strictly forbidden; hardcoded field offset lookups are prohibited.
- **Integrity Era (libraries_105)**:
  - Formats: Format 105, 105a, 105db, MFDB v1.40.
  - Characteristics: UUIDv4 record and field level fingerprints, E90-E95 integrity verification, automated upgrade tooling (`bejson_upgrade_cli.py`). Development libraries reside at `$ADMIN_LIBRARIES_105`; do not load unless instructed.

### 1.2 User Interface & Spatial Layout Domain (BEHTML)
- **Spatial Geometry**: Strict 8-lane horizontal grid (`x_start + x_span <= 8`), 16-sublane precision (6.25% half-cells), row quantization at `Ry = 32px` heights (`y_start * 32`, `y_span * 32`).
- **Visual Design Rules**: BECSS Tri-Color palette strictly enforced: `#000000` (Canvas Background), `#FFFFFF` (Primary Text/Lines), `#DE2626` (Red Accent/Telemetry/Borders).
- **Zero Filler Law**: No dummy lorem ipsum; all structural templates use literal structural placeholders (`Title`, `Content Body`, `Menu Header`).

### 1.3 Library Hierarchy & Codebase Governance
- **Libraries 104 (Stable / Frozen)**: Located at `$ADMIN_LIBRARIES_104` (or `$ADMIN_LIBRARIES`). The production workhorse. Do NOT alter official library directories without explicit user instruction.
- **Libraries 105 (Development / Active)**: Located at `$ADMIN_LIBRARIES_105`. Experimental stage; isolated from production tools.

### 1.4 Global Daily Logging System
- **Authoritative Sink**: Daily UTC partition `$GLOBAL_LOGS/Log-<YYYY-MM-DD>.bejson`.
- **Sensitive Operations**: Routes to `$GLOBAL_LOGS_SECURE/Log-<YYYY-MM-DD>-secure.bejson` with automated `[redacted: secure entry]` placeholders written to public daily log.
- **Context Payload**: Structured JSON `--context` payload detailing `task`, `status`, `files_modified`, and execution telemetry.

### 1.5 Project Registration & Archival Engine
- **Canonical Type Ledger**: `$PROJECT_TYPE_LEDGER` (`project_type_ledger.104a.bejson`). All tools must query pre-existing types before declaring new ones.
- **Project Chunker**: `$PROJECT_CHUNKER` (`project_chunker.py`). Authoritative engine for tracking (`--track`), chunking (`--chunk`), verified atomic scooping (`--scoop`), and querying (`--list`).
- **Project Archive Partitioning**: `$PROJECTS_ARCHIVE_ROOT/<type>/<project_name>/`. Strictly partitioned by Type Ledger subfolders.
- **Version Formula**: Solid integer versioning (`Name_Case-V#-PKG#`), package version bumped before every delivery.

---

## 2. Canonical Environment Resolution

All operational paths must be resolved dynamically from `/storage/emulated/0/.env/user/definitions.json` (canonical source of truth):
- `INTERNAL_STORAGE`: `/storage/emulated/0`
- `PROJECTS_ARCHIVE_ROOT`: `/storage/emulated/0/Admin/Core/Projects_Archive`
- `GLOBAL_LOGS`: `/storage/emulated/0/Admin/System/Global_Logs`
- `LOGGING_TOOL`: `/storage/emulated/0/Admin/System/tools/logging_tool/logging_tool.py`
- `PROJECT_TYPE_LEDGER`: `/storage/emulated/0/Admin/Dev/Policy/project_type_ledger.104a.bejson`
- `PROJECT_CHUNKER`: `/storage/emulated/0/Admin/System/Project_Chunker`
- `ADMIN_LIBRARIES_104`: `/storage/emulated/0/Admin/Libraries/libraries_104`
- `ADMIN_LIBRARIES_105`: `/storage/emulated/0/Admin/Libraries/libraries_105`
- `JOB_MANAGEMENT`: `/storage/emulated/0/Admin/System/Job_Management`
