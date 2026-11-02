---
name: bejson-chunker-engine
description: >-
  Serialize and unchunk directories, codebases, scratch folders, and Admin
  Library families (104/105 Lib_JS, Lib_PY, Lib_SH, Lib_TS) into standardized
  single-file flat BEJSON text containers (.104a.bejson.txt or .bejson.txt)
  using the Chunked-104a schema and Simple_Chunker_CLI. Unifies flat directory
  packaging, ephemeral scratch snapshots, stage-and-snap cross-system collections,
  and library subsystem archiving without project tracker overhead. Use when
  packaging codebases into single-file text archives, unchunking .bejson.txt files,
  creating prompt context snapshots, or archiving library families. Do NOT use
  for whole-project release packaging with versioned ZIPs and registry tracking
  (use project-chunker-archiver), packing or mounting single-file MFDB containers
  (use mfdb-104-chunker), single-file 104 table operations (use bejson-104-core),
  or validating BEJSON schemas (use bejson-schema-validator).
---

# Skill: `bejson-chunker-engine` (Layer 2 Text Chunker & Container Engine)

- **Version**: `100`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 2 (Domain Processing & Packaging Engine)`
- **Format Standard**: `Chunked-104a (.104a.bejson.txt / .bejson.txt)`
- **Embedded Tool**: [`scripts/Simple_Chunker_CLI.py`](./scripts/Simple_Chunker_CLI.py)
- **Staged Tool**: `/storage/emulated/0/Admin/Dev/Tools/Chunker_CLI/Simple_Chunker_CLI.py`
- **Reference Specification**: [`references/chunked_104a_spec.md`](./references/chunked_104a_spec.md)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Purpose & Architectural Scope

`bejson-chunker-engine` is the canonical Layer 2 engine for collapsing directory trees, codebases, and library modules into portable, single-file flat BEJSON text archives (`.104a.bejson.txt`) and unpacking them back to intact filesystem structures.

This engine unifies three previously fragmented workflows:
1. **Flat Directory Chunking**: Packaging project repositories without project tracker overhead.
2. **Ephemeral Scratch Snapshots**: Creating lightweight, MIME-evading text files for LLM context injection or temporary backups.
3. **Admin Library Subsystem Chunking**: Packaging modular language families (`Lib_JS`, `Lib_PY`, `Lib_SH`, `Lib_TS`) and Stage-and-Snap cross-system collections into `/storage/emulated/0/Admin/Libraries/Chunked_Libraries/`.

---

## 2. Core Invariants & Defaults

1. **Zero Tracker Dependency**: Operates independently of `bejson_project.json` and registry databases.
2. **Default Destination**: Generated chunks route to `/storage/emulated/0/Admin/Resources/Chunks/Chunked_<name>.104a.bejson.txt` unless overridden via `--dest`.
3. **Text-First Discipline (`Is_Binary: False`)**: Excludes binaries by default to keep files lightweight and prompt-injectable. Pass `--include-binary` only when required.
4. **MIME Evasion (`.bejson.txt`)**: Appends `.txt` to prevent mobile operating systems or cloud platforms from misidentifying or blocking files.
5. **Stage-and-Snap Protocol**: Temporary cross-system collection directories are staged, chunked, and immediately pruned.

---

## 3. Operational CLI Command Reference

The engine is executed directly via Python 3.10+:

```bash
# Via embedded skill script
python3 ~/.gemini/config/skills/bejson-chunker-engine/scripts/Simple_Chunker_CLI.py [OPTIONS]
```

### Common Workflows

| Task | Command |
| :--- | :--- |
| **Chunk Directory to Default Storage** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_dir>` |
| **Chunk to Custom Output Directory** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_dir> --dest <output_folder>` |
| **Chunk Library Family** | `python3 scripts/Simple_Chunker_CLI.py --chunk /storage/emulated/0/Admin/Libraries/libraries_104/Lib_PY --dest /storage/emulated/0/Admin/Libraries/Chunked_Libraries/104` |
| **Chunk with Context Description** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_dir> --context "Pre-migration snapshot"` |
| **Chunk with File Extension Filters** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_dir> --patterns ".py,.ts,.json"` |
| **Unchunk Container to Directory Tree** | `python3 scripts/Simple_Chunker_CLI.py --unchunk <chunk_file.bejson.txt> --dest <restore_dir>` |

---

## 4. Execution & Subagent Containment Contract (Level 3 Guardrail)

When invoking subagents or automated chunking daemons from `bejson-chunker-engine`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Chunk target directory using bejson-chunker-engine and return destination path."
```

---

## When NOT to Use

Do NOT use `bejson-chunker-engine` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Packaging release versions with tracker DB registration and ZIPs**: Redirect immediately to `project-chunker-archiver`.
- **Packaging or mounting single-file MFDB containers (.mfdb132.bejson)**: Redirect immediately to `mfdb-104-chunker`.
- **Executing table-level CRUD on individual BEJSON files**: Redirect immediately to `bejson-104-core`.
- **Validating BEJSON schema structural integrity**: Redirect immediately to `bejson-schema-validator`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
