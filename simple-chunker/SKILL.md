---
name: simple-chunker
description: >-
  Quick, non-archiving single-file BEJSON project and directory chunking (.104a.bejson.txt) for ephemeral packaging, AI context injection, scratch backups, and ad-hoc unchunking. Specially suited for smaller sub-pieces and individual library families (Lib_JS, Lib_PY, Lib_SH, Lib_TS) without registry overhead. Zero registry tracking, zero history logs, and zero archive directory pollution. Use when needing fast, lightweight, standalone in-place or scratch directory chunks without committing to persistent archive registries. Do NOT use for entire 104/105 libraries bundles or formal archive scoops with versioned tracking (use project-chunker-archiver), full library orchestration (use library-chunker), or MFDB container packaging (use mfdb-104-chunker).
---

# simple-chunker (Layer 2 Ad-Hoc & Ephemeral Chunker)

## Summary

`simple-chunker` is a dedicated, lightweight utility skill for generating quick, non-archiving BEJSON 104a text chunk containers (`.104a.bejson.txt`). Unlike archival tools, `simple-chunker` operates with **zero registry tracking**, **zero history log pollution**, and **zero directory scoops**. It is purpose-built for ephemeral developer workflows: instant AI context snapshots, rapid pre-refactor backups, quick single-file inspections, and chunking smaller modular sub-pieces such as individual library families (`Lib_JS`, `Lib_PY`, `Lib_SH`, `Lib_TS`).

## When to Use

- Chunking smaller sub-pieces and individual library families (e.g. `Lib_JS`, `Lib_PY`, `Lib_SH`, `Lib_TS`) into lightweight flat `.104a.bejson.txt` files without registering them as separate projects.
- Creating quick, ad-hoc single-file chunks of directories or files for prompt injection, AI context bubbles, or sharing.
- Taking ephemeral, in-place pre-refactoring snapshots without modifying or moving source files.
- Emitting chunks directly to standard output (`--stdout`) to pipe into LLM prompts, clipboards, or processing pipelines.
- Inspecting chunk metadata, file manifests, and injected context notes (`--info`) without extracting files to disk.
- Extracting a single file from an existing chunk to stdout (`--cat`) on the fly.
- Unchunking and restoring `.104a.bejson.txt` files directly to loose directory trees or `.zip` archives.

## When NOT to Use

- **Entire Library Bundles (libraries_104 / libraries_105)**: Do NOT use `simple-chunker` to track or snapshot entire library ecosystems (`libraries_104`, `libraries_105`) as whole projects. Use [project-chunker-archiver](file:///data/data/com.termux/files/home/.gemini/config/skills/project-chunker-archiver/SKILL.md) with `--track` and `--chunk`. For unified library chunking across both full snapshots and family chunks, use [library-chunker](file:///data/data/com.termux/files/home/.gemini/config/skills/library-chunker/SKILL.md).
- **Formal Archive Retention & Type Ledger Partitioning**: If packaging releases into `$PROJECTS_ARCHIVE_ROOT/<type>/<project>/` with atomic scoop-and-wipe, manual `-V`/`-P` versioning, and canonical type ledger tracking, use [project-chunker-archiver](file:///data/data/com.termux/files/home/.gemini/config/skills/project-chunker-archiver/SKILL.md).
- **Multi-File Database (MFDB) Mounts**: If packing or sticky-mounting MFDB multi-file databases into `.mfdb132.bejson` containers with SHA-256 lock files, use [mfdb-104-chunker](file:///data/data/com.termux/files/home/.gemini/config/skills/mfdb-104-chunker/SKILL.md).
- **Static AST Code Auditing**: For validating BEJSON field map caching compliance in Python source files, use [policy-bejson-auditor](file:///data/data/com.termux/files/home/.gemini/config/skills/policy-bejson-auditor/SKILL.md).

---

## 1. Core Principles & Non-Archiving Invariants

1. **Zero Registry Pollution**:
   - Never writes to or requires `registry.104a.bejson` or `chunk_history.104a.bejson`.
   - Never alters or requires `bejson_project.json`.
2. **Zero Archive Pollution**:
   - Does not place files into `/storage/emulated/0/Admin/Resources/Chunks/` unless explicitly directed by the caller via `--output` / `-o`.
   - Default output is strictly local: `./Chunked_<dirname>.104a.bejson.txt` in the current working directory.
3. **Zero Destruction (Non-Scooping)**:
   - Source files and directory trees are never wiped, moved, or scooped.
4. **Canonical Chunked-104a Schema**:
   - Emits strict, validated BEJSON 104a flat tabular documents (`File_Name`, `File_Extension`, `File_Content`, `File_Version`, `File_Hash`, `Relative_Path`, `Is_Binary`, `Is_Mounted`).
   - Uses O(1) Field Map Caching (`bejson_core_get_field_map`) for all lookups.
5. **Context Pre-Pending (`!-CONTEXT.txt`)**:
   - The `--context` parameter embeds developer instructions or prompt notes at index 0 without modifying the on-disk source files.

---

## 2. CLI Command Reference (`simple_chunker.py`)

Executable script path:
`python3 ~/.gemini/config/skills/simple-chunker/scripts/simple_chunker.py`

### 2.1 Command Matrix

| Task | Command Syntax |
| :--- | :--- |
| **Quick Chunk (Local/CWD)** | `python3 simple_chunker.py --chunk <target_directory>` |
| **Quick Chunk to Custom Path** | `python3 simple_chunker.py --chunk <dir> --output /path/to/my_chunk.104a.bejson.txt` |
| **Quick Chunk with AI Context** | `python3 simple_chunker.py --chunk <dir> --context "Instructions for LLM review"` |
| **Stream Chunk to stdout** | `python3 simple_chunker.py --chunk <dir> --stdout` |
| **Chunk Specific Extensions** | `python3 simple_chunker.py --chunk <dir> --patterns ".py,.json,.md"` |
| **Chunk with Binary Files** | `python3 simple_chunker.py --chunk <dir> --include-binary` |
| **Inspect Chunk Summary** | `python3 simple_chunker.py --info <chunk_file.104a.bejson.txt>` |
| **View Single File in Chunk** | `python3 simple_chunker.py --cat <chunk_file.104a.bejson.txt> <relative_path>` |
| **Unchunk to Directory** | `python3 simple_chunker.py --unchunk <chunk_file> --output <restore_dir>` |
| **Unchunk Directly to ZIP** | `python3 simple_chunker.py --unchunk <chunk_file> --output <restore_dir> --zip` |

---

## 3. Practical Developer Workflows

### 3.1 Fast AI Prompt Context Preparation
When preparing a set of files or a subfolder to feed into an LLM without cluttering the chat or creating permanent archives:
```bash
# Generate chunk with embedded instructions directly to a scratch file:
python3 ~/.gemini/config/skills/simple-chunker/scripts/simple_chunker.py \
  --chunk "./src" \
  --context "Review these modules for memory leaks and async thread-safety." \
  --output "./scratch_context.104a.bejson.txt"
```

### 3.2 Ephemeral Pre-Refactor Snapshot
Before making major experimental changes to a project directory:
```bash
# Capture instant local snapshot in the project parent directory:
python3 ~/.gemini/config/skills/simple-chunker/scripts/simple_chunker.py \
  --chunk "/path/to/my_feature" \
  --output "/path/to/my_feature/pre_refactor_snapshot.104a.bejson.txt"
```

### 3.3 Quick Inspection Without Unpacking
To verify what files or notes are inside a `.104a.bejson.txt` file before restoring:
```bash
python3 ~/.gemini/config/skills/simple-chunker/scripts/simple_chunker.py \
  --info "./scratch_context.104a.bejson.txt"
```

### 3.4 Extract Single File from Chunk
To extract only a specific configuration or script from a chunk container without unpacking the entire tree:
```bash
python3 ~/.gemini/config/skills/simple-chunker/scripts/simple_chunker.py \
  --cat "./scratch_context.104a.bejson.txt" "config/settings.json" > settings.json
```
