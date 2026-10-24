---
name: bejson-document-chunker
description: >-
  Author, index, manipulate, assemble, mount, and manage chunked documents across BEJSON document systems (Lib_MD markdown indexing and Doc_Chunker 104db document projects). Use when chunking markdown files, managing document categories and paragraph-split chunks, tagging chunks, setting chunk statuses (draft, review, final, skip), compiling documents to Markdown with table of contents, mounting/committing document projects, or performing delimiter imports. Do NOT use for codebase archive packaging (use chunking-core) or MFDB multi-file database container mounting (use mfdb-104-chunker).
---

# Skill: `bejson-document-chunker` (Layer 2)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2`
- **Era & Library Binding**: `104 (Foundational Era - libraries_104 / Lib_MD & Doc_Chunker)`
- **Canonical Library Root**: `/storage/emulated/0/Admin/Core/libraries/libraries_104`
- **Target Formats**: `BEJSON 104db (Document_Categories + Chunks) & Markdown Chunk Indexes`
- **Embedded Tool**: `scripts/Doc_Chunker.py`
- **Date Created**: `2026-10-24`
- **RELATIONAL_ID**: `4e6a8b1c-9d2f-4a3e-8c5b-7d1e0f3a5b9c`
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-document-chunker` operates at **Layer 2** of the 6-Tier Layered Skill Architecture. It provides structured document management, multi-record `104db` database document authoring, paragraph splitting, chunk lifecycle states, and Markdown compilation with auto-generated tables of contents.

### Bound Canonical Modules
- `Lib_PY/Core/lib_bejson_Core_bejson_core.py`
- `Lib_PY/Core/lib_bejson_Core_bejson_validator.py`
- `Lib_PY/Utility/lib_bejson_Utility_bejson_utility.py`
- `scripts/Doc_Chunker.py` (v3.0.0 standalone document management engine)

---

## 2. Core Structural & Policy Invariants

1. **Multi-Record Schema (104db)**: Documents utilize two distinct record types in one file: `Document_Categories` and `Chunks`, discriminated by `Record_Type_Parent`.
2. **Mount/Commit Cycle**: Mounting explodes schema chunks into temporary `.txt` files in a workspace; committing validates and synchronizes edits back to the schema.
3. **Chunk Lifecycle**: Chunks track categories, index positions, tags, and status lifecycles (`draft`, `review`, `final`, `skip`).
4. **Mandatory Field Map Cache**: Column offsets are resolved through cached dictionary lookups per Policy §6.2.

---

## 3. CLI Tool Reference (`scripts/Doc_Chunker.py`)

The skill provides the executable script `scripts/Doc_Chunker.py`:

```bash
# Create a new document project
python3 scripts/Doc_Chunker.py --doc-new "System_Specification"

# List and select document projects
python3 scripts/Doc_Chunker.py --doc-list
python3 scripts/Doc_Chunker.py --doc-sel 0

# Add categories and chunks
python3 scripts/Doc_Chunker.py --doc-cat-add "Introduction"
python3 scripts/Doc_Chunker.py --doc-chunk-add "Introduction" --label "Overview" --content "System overview text..."

# Set tags and status
python3 scripts/Doc_Chunker.py --doc-chunk-tag <chunk_id> --tags "core,architecture"
python3 scripts/Doc_Chunker.py --doc-chunk-set-status <chunk_id> --status final

# Mount document for editing and commit back
python3 scripts/Doc_Chunker.py --doc-mount
python3 scripts/Doc_Chunker.py --doc-commit

# Compile document to Markdown with Table of Contents
python3 scripts/Doc_Chunker.py --doc-compile

# Import delimited text into chunks
python3 scripts/Doc_Chunker.py --doc-import-file draft.txt --delimiter "---" --category "Drafts"
```

---

## 4. Execution & Subagent Containment Contract (Level 3 Guardrail)

When invoking subagents or CLI verification tools from `bejson-document-chunker`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Execute bejson-document-chunker verification gate and return deterministic JSON status."
```

---

## When NOT to Use

Do NOT use `bejson-document-chunker` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Codebase and project directory chunking**: Redirect immediately to `chunking-core`.
- **Multi-File Database (MFDB) single-file container packaging and sticky mounting**: Redirect immediately to `mfdb-104-chunker`.
- **Standard single-file 104/104a CRUD**: Redirect immediately to `bejson-104-core`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
