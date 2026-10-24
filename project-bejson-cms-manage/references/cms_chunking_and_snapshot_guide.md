# BEJSON CMS - Chunking & Snapshotting Guide via chunking-core

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Effective Date: 2026-10-21
RELATIONAL_ID: 3a2b1c4d-5e6f-7081-92a3-b4c5d6e7f8a9
Version: 100
Release_Version: 300

---

## 1. Overview & Paradigm

While `cms-manage.py backup` generates standard `.zip` archives of live storage, BEJSON CMS also integrates natively with the **`chunking-core`** skill framework (`Simple_Chunker_CLI.py`).

Chunking serializes directory hierarchies, source code files, and tabular BEJSON databases into a single, flat, human-readable BEJSON text file (`.104a.bejson.txt`).

### Advantages of Chunked Snapshots:
- **Zero-Binary Text Portability**: Produces lightweight plain-text containers suitable for Git tracking, LLM context windows, and cross-platform transport.
- **MIME Evasion**: Uses `.bejson.txt` extensions to prevent binary attachment blocks in web and email environments.
- **No External Daemon or SQLite**: Pure Python 3.10+ execution.

---

## 2. Using `chunking-core` for BEJSON CMS Snapshots

The canonical `chunking-core` tool resides at:
- `~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py`
- `/storage/emulated/0/Admin/Dev/Tools/Chunker_CLI/Simple_Chunker_CLI.py`

### 2.1 Full Codebase Snapshot
To chunk the entire CMS project into `/storage/emulated/0/Admin/Resources/Chunks/`:
```bash
python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
  --chunk /storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS \
  --context "Full BEJSON CMS Codebase Snapshot"
```

### 2.2 Database-Only Snapshot (MFDB State)
To snapshot strictly the live MFDB database manifest and 10 entity tables without logs or static builds:
```bash
python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
  --chunk /storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS/storage/mfdb \
  --dest /storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS/storage/exports \
  --context "MFDB Live Database Snapshot"
```

### 2.3 Restoring from a Chunked Snapshot
To unchunk a snapshot back into a target directory:
```bash
python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
  --unchunk /storage/emulated/0/Admin/Resources/Chunks/Chunked_BEJSON_CMS.104a.bejson.txt \
  --dest /storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS_Restored
```

---

## 3. Dedicated `cms_chunker_tool.py`

The custom wrapper tool at `scripts/cms_chunker_tool.py` automates project-specific snapshots with predefined flags:

```bash
# Snapshot live database only (manifest + 10 tables)
python3 scripts/cms_chunker_tool.py --db-only

# Snapshot entire CMS project
python3 scripts/cms_chunker_tool.py --full

# Unchunk snapshot
python3 scripts/cms_chunker_tool.py --restore <path_to_chunk_file>
```
