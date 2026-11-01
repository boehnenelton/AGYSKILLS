---
name: library-chunker
description: >-
  Orchestrate and execute the dual-tier and stage-and-snap chunking workflows for Elton Boehnen's BEJSON & MFDB Admin Libraries (libraries_104 Foundational Era and libraries_105 Integrity Era). Tracks and snapshots entire 104 and 105 ecosystems as separate standalone projects using Project_Chunker (--track, --chunk), serializes individual language families (Lib_JS, Lib_PY, Lib_SH, Lib_TS) into flat .104a.bejson.txt containers using Simple_Chunker_CLI, and executes ephemeral stage-and-snap collections (e.g. Core modules across all systems) with automatic post-chunk staging cleanup. Use when chunking 104 or 105 libraries, refreshing Chunked_Libraries, or packaging cross-system library slices. Do NOT use for single non-library application repos (use project-chunker-archiver), ad-hoc file scratch chunks (use simple-chunker), or MFDB container mounting (use mfdb-104-chunker).
---

# library-chunker (Layer 3 / Layer 6 Dedicated Library Chunking Engine)

## Summary

`library-chunker` is the canonical skill governing the packaging, snapshotting, and chunk serialization of Elton Boehnen's Admin Libraries (`libraries_104` and `libraries_105`). It codifies the architectural boundary between **whole project tracking** and **modular sub-piece serialization**, ensuring that:
1. Entire library suites are tracked as separate, registered projects in the Project Chunker Master Registry.
2. Individual language families (`Lib_JS`, `Lib_PY`, `Lib_SH`, `Lib_TS`) are chunked into lightweight flat BEJSON text containers (`.104a.bejson.txt`).
3. Cross-system collections (such as compiling `Core` from every system) follow the **Stage-and-Snap** paradigm: staging into a temporary folder, chunking, and immediately wiping the staging directory.
4. Outdated chunks in `$CHUNKED_LIBRARIES/` are pruned per `Admin/Libraries/AGENTS.MD` retention rules.

## When to Use

- Chunking the complete `libraries_104` or `libraries_105` codebase as separate registered projects.
- Chunking individual language families (`Lib_JS`, `Lib_PY`, `Lib_SH`, `Lib_TS`) into `$CHUNKED_LIBRARIES/<104|105>/`.
- Running **Stage-and-Snap** workflows: copying arbitrary cross-system subsystems into temporary staging (e.g. `$ADMIN_LIBRARIES/stage/`), chunking the staged package, and immediately deleting the staging folder.
- Synchronizing and pruning `/storage/emulated/0/Admin/Libraries/Chunked_Libraries/` so only the latest version of each chunk is preserved.
- Executing the turnkey `library_chunker.py` CLI script to update all library chunk targets in a single command.

## When NOT to Use

- **Standalone User Applications & Tools**: For general application projects, tools, or release ZIPs outside the Admin Libraries ecosystem, use [project-chunker-archiver](file:///data/data/com.termux/files/home/.gemini/config/skills/project-chunker-archiver/SKILL.md).
- **Ad-Hoc Ephemeral Developer Chunks**: For quick in-place single-directory snapshots or prompt context injection without library destination rules, use [simple-chunker](file:///data/data/com.termux/files/home/.gemini/config/skills/simple-chunker/SKILL.md).
- **MFDB Sticky Container Mounts**: For packing or mounting multi-file databases into `.mfdb132.bejson` containers with SHA-256 locks, use [mfdb-104-chunker](file:///data/data/com.termux/files/home/.gemini/config/skills/mfdb-104-chunker/SKILL.md).
- **AST Code Policy Auditing**: For auditing Python source files for field-map caching compliance, use [policy-bejson-auditor](file:///data/data/com.termux/files/home/.gemini/config/skills/policy-bejson-auditor/SKILL.md).

---

## 1. The Tri-Tier Library Chunking Architecture

Library chunking is strictly partitioned into three complementary operational tiers:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      LIBRARY CHUNKING ARCHITECTURE                     │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 1: ENTIRE LIBRARY SUITES (Project Chunker with --track & --chunk) │
│ - Separate projects: libraries_104 and libraries_105                   │
│ - Master Registry & Tracker DB registration                            │
│ - Deployed to: $CHUNKED_LIBRARIES/<104|105>/libraries_<era>-V*.bejson  │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 2: LANGUAGE FAMILY SUBSYSTEMS (Simple Chunker)                    │
│ - Modular pieces: Lib_JS, Lib_PY, Lib_SH, Lib_TS                      │
│ - Flat Chunked-104a schema (.104a.bejson.txt)                          │
│ - Deployed to: $CHUNKED_LIBRARIES/<104|105>/Chunked_<family>.104a...   │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 3: EPHEMERAL STAGE-AND-SNAP (Cross-System Subsets)                │
│ - Arbitrary collections (e.g. Core across PY, JS, TS, SH)              │
│ - 1. Copy to $ADMIN_LIBRARIES/stage/                                   │
│ - 2. Chunk staged directory via Simple Chunker                         │
│ - 3. Immediately delete $ADMIN_LIBRARIES/stage/ after chunking         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Retention & Destination Policy (`AGENTS.MD`)

Per `/storage/emulated/0/Admin/Libraries/AGENTS.MD`:
> *"Latest library chunks should be copied to `/storage/emulated/0/Admin/Libraries/Chunked_Libraries` after cleaning up outdated chunks."*

### Standard Directory Topology:
- **104 Chunks Sink**: `$CHUNKED_LIBRARIES/104/` (`/storage/emulated/0/Admin/Libraries/Chunked_Libraries/104`)
- **105 Chunks Sink**: `$CHUNKED_LIBRARIES/105/` (`/storage/emulated/0/Admin/Libraries/Chunked_Libraries/105`)
- **Staging Dropzone**: `$ADMIN_LIBRARIES/stage/` (`/storage/emulated/0/Admin/Libraries/stage`)
- **Compiled Output**: `$ADMIN_LIBRARIES/Compiled_Core/` (`/storage/emulated/0/Admin/Libraries/Compiled_Core`)

Whenever a new full snapshot is copied to `Chunked_Libraries/`, all previous versions of that full snapshot (e.g., older `libraries_104-V*.bejson`) are deleted so that only the latest version remains.

---

## 3. CLI Command Reference

### 3.1 Turnkey Orchestrator (`library_chunker.py`)

The skill embeds a unified CLI engine at `scripts/library_chunker.py`:

```bash
# Chunk everything across both 104 and 105 (full projects + all 4 families):
python3 ~/.gemini/config/skills/library-chunker/scripts/library_chunker.py --target all --tier all

# Chunk only 104 libraries (full + families):
python3 ~/.gemini/config/skills/library-chunker/scripts/library_chunker.py --target 104 --tier all

# Chunk only 105 libraries:
python3 ~/.gemini/config/skills/library-chunker/scripts/library_chunker.py --target 105 --tier all

# Chunk only language families (Lib_JS, Lib_PY, Lib_SH, Lib_TS) for 104:
python3 ~/.gemini/config/skills/library-chunker/scripts/library_chunker.py --target 104 --tier families

# Execute stage-and-snap for cross-system Core modules:
python3 ~/.gemini/config/skills/library-chunker/scripts/library_chunker.py --target 104 --stage-snap
```

### 3.2 Manual Tier 1: Entire Library Snapshotting (Project Chunker)

```bash
# --- Entire libraries_104 ---
python3 "$PROJECT_CHUNKER/CLI/project_chunker.py" --track "$ADMIN_LIBRARIES_104"
python3 "$PROJECT_CHUNKER/CLI/project_chunker.py" --chunk "$ADMIN_LIBRARIES_104"
# Copy snapshot to Chunked_Libraries/104 and prune older versions

# --- Entire libraries_105 ---
python3 "$PROJECT_CHUNKER/CLI/project_chunker.py" --track "$ADMIN_LIBRARIES_105" -V 5.8.1 -P 112 --type library
python3 "$PROJECT_CHUNKER/CLI/project_chunker.py" --chunk "$ADMIN_LIBRARIES_105" -V 5.8.1 -P 112 --type library
# Copy snapshot to Chunked_Libraries/105 and prune older versions
```

### 3.3 Manual Tier 2: Language Family Chunking (Simple Chunker)

```bash
# Chunk all 4 systems for 104:
for sys in Lib_JS Lib_PY Lib_SH Lib_TS; do
    python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
        --chunk "$ADMIN_LIBRARIES_104/$sys" \
        --dest "$CHUNKED_LIBRARIES/104"
done

# Chunk all 4 systems for 105:
for sys in Lib_JS Lib_PY Lib_SH Lib_TS; do
    python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
        --chunk "$ADMIN_LIBRARIES_105/$sys" \
        --dest "$CHUNKED_LIBRARIES/105"
done
```

### 3.4 Manual Tier 3: Stage-and-Snap Cross-System Subsets

When compiling arbitrary subsets (e.g. all `Core` directories across all 4 systems):
```bash
# 1. Create staging directory
mkdir -p "$ADMIN_LIBRARIES/stage"

# 2. Copy target modules into staging
cp -r "$ADMIN_LIBRARIES_104/Lib_PY/Core" "$ADMIN_LIBRARIES/stage/Lib_PY_Core"
cp -r "$ADMIN_LIBRARIES_104/Lib_JS/Core" "$ADMIN_LIBRARIES/stage/Lib_JS_Core"
cp -r "$ADMIN_LIBRARIES_104/Lib_TS/Core" "$ADMIN_LIBRARIES/stage/Lib_TS_Core"
cp -r "$ADMIN_LIBRARIES_104/Lib_SH/Core" "$ADMIN_LIBRARIES/stage/Lib_SH_Core"

# 3. Chunk the staged directory
python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
    --chunk "$ADMIN_LIBRARIES/stage" \
    --dest "$ADMIN_LIBRARIES/Compiled_Core"

# 4. Mandatory cleanup: remove the staging directory
rm -rf "$ADMIN_LIBRARIES/stage"
```

---

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
