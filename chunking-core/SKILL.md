---
name: chunking-core
description: >-
  Chunk directories, codebases, project repositories, and Admin Library systems (104/105 Lib_JS, Lib_PY, Lib_SH, Lib_TS) into standardized single-file flat BEJSON archives (.104a.bejson.txt or .bejson.txt) using the Chunked-104 schema, and unchunk archives back to directory trees or zip files using Simple_Chunker_CLI. Automatically routes 4-system library chunk requests directly to /storage/emulated/0/Admin/Libraries/Chunked_Libraries/<104|105>. Defaults to Is_Binary off (pure text files only), chunk-in-target disabled, no project tracker required, and saves chunks by default to /storage/emulated/0/Admin/Resources/Chunks. Use when packaging, backing up, or restoring code projects or Admin library systems to and from single-file BEJSON text containers. Do NOT use for Chunked-132 MFDB container mounting (use mfdb-104-chunker) or general AST code auditing.
---

# Skill: `chunking-core`

- **Purpose**: Single-file BEJSON project chunking and unchunking to and from `.104a.bejson.txt` / `.bejson.txt` files with zero project tracker dependency.
- **Embedded Tool**: `scripts/Simple_Chunker_CLI.py` (also staged at `/storage/emulated/0/Admin/Dev/Tools/Chunker_CLI/Simple_Chunker_CLI.py`)
- **Primary Runtime**: Python 3.10+ (Self-contained standalone build, zero external library dependencies)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `3420f25f-2f0f-429c-a77b-6022f8cc4265`
- **Version**: `1.0.1`

---

## 1. Core Principles & Operational Defaults

`chunking-core` provides rapid, lightweight serialization and extraction of entire directory structures into single-file flat BEJSON documents using the canonical **Chunked-104a** schema.

### Operational Invariants & Defaults:
1. **No Tracker Required**:
   - Runs purely standalone. Does not require or write `bejson_project.json` or interact with project registries.
2. **Default Destination (`/storage/emulated/0/Admin/Resources/Chunks`)**:
   - Unless an explicit output destination is provided via `--dest` or `--output`, all generated chunks are automatically saved directly to `/storage/emulated/0/Admin/Resources/Chunks/Chunked_<project_name>.104a.bejson.txt`.
3. **Default `Is_Binary` Off**:
   - Binary files (compiled binaries, images, objects) are **excluded by default** to keep archives strictly text-based and lightweight.
   - All chunked records have `Is_Binary: False`.
   - Pass `--include-binary` only when binary file inclusion is explicitly needed.
4. **Chunk-in-Target Disabled by Default**:
   - Chunks are never copied into the target directory (`chunked5/`) unless explicitly requested via `--chunk-in-target`.
5. **MIME-Evading `.bejson.txt` Standard**:
   - Output files use the `.104a.bejson.txt` extension by default (`evade_mime: True`), enabling frictionless transfer across platforms without MIME-type blocking.
   - Unchunking natively parses `.bejson.txt`, `.104a.bejson.txt`, `.104db.bejson.txt`, and `.bejson` files.

---

## 2. Tool Roster & Execution References

`chunking-core` provides three complementary chunking tools:
1. **`Simple_Chunker_CLI.py`** (`scripts/Simple_Chunker_CLI.py`): Zero-tracker, lightweight text-first chunker defaulting to `/storage/emulated/0/Admin/Resources/Chunks`.
2. **`CLI_Chunker.py`** (`scripts/CLI_Chunker.py`): Standalone build supporting dual schemas (`104` flat and `104db` relational) with registered history and direct-to-ZIP unchunking.
3. **`Project_Chunker`** (`/storage/emulated/0/Admin/Dev/Python/Development/Project_Chunker/CLI/project_chunker.py`): Flagship hybrid project chunker and tracker backed by the 3-pillar architecture (Tracker DB, Master Registry, and Per-Project Snapshots).

### 2.1 Simple_Chunker_CLI Command Matrix

| Task | Command Syntax |
|---|---|
| **Chunk to Default Storage** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_directory>` |
| **Chunk to Custom Directory** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_directory> --dest <output_folder>` |
| **Chunk with Context Note** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_directory> --context "Architecture notes"` |
| **Chunk Including Binary Files** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_directory> --include-binary` |
| **Chunk with Custom Extensions** | `python3 scripts/Simple_Chunker_CLI.py --chunk <target_directory> --patterns ".py,.ts,.json"` |
| **Unchunk to Directory** | `python3 scripts/Simple_Chunker_CLI.py --unchunk <chunk_file.bejson.txt> --dest <restore_dir>` |
| **Unchunk Direct to ZIP** | `python3 scripts/Simple_Chunker_CLI.py --unchunk <chunk_file.bejson.txt> --dest <restore_dir> --zip` |
| **List History & Registry** | `python3 scripts/Simple_Chunker_CLI.py --list-chunk-index`<br>`python3 scripts/Simple_Chunker_CLI.py --list-unchunk-index` |

### 2.2 Project_Chunker (Advanced Tracking & Archival)

Located at `/storage/emulated/0/Admin/Dev/Python/Development/Project_Chunker/`:
```bash
# Track and snapshot a project
python3 /storage/emulated/0/Admin/Dev/Python/Development/Project_Chunker/CLI/project_chunker.py /path/to/project --track --chunk

# Verified scoop (snapshot + delete source files)
python3 /storage/emulated/0/Admin/Dev/Python/Development/Project_Chunker/CLI/project_chunker.py /path/to/project --track --scoop

# Restore from snapshot UUID
python3 /storage/emulated/0/Admin/Dev/Python/Development/Project_Chunker/CLI/project_chunker.py --restore <UUID> --dest /path/to/restore
```

---

## 3. Workflow Examples

### Example 1: Chunking a Repository
```bash
# Chunk the repository (saves to /storage/emulated/0/Admin/Resources/Chunks/Chunked_MyProject.104a.bejson.txt)
python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
    --chunk "/path/to/MyProject"
```

### Example 2: Chunking with Injected Context
The `--context` flag automatically writes `!-CONTEXT.txt` into the root of the target directory before chunking. Because `!` sorts before alphanumeric characters, it is guaranteed to be the very first file record in the resulting BEJSON archive:
```bash
python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
    --chunk "/path/to/MyProject" \
    --context "This chunk contains the v1.0.0 client core modules."
```

### Example 3: Unchunking Directly to a ZIP Archive
```bash
python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
    --unchunk "/storage/emulated/0/Admin/Resources/Chunks/Chunked_MyProject.104a.bejson.txt" \
    --dest "/path/to/restored_export" \
    --zip
# Output: /path/to/restored_export.zip
```

### Example 4: Chunking Admin Libraries (4 Systems Architecture)
Chunk all 4 core language systems (`Lib_JS`, `Lib_PY`, `Lib_SH`, `Lib_TS`) into their dedicated repository under `Chunked_Libraries`:

```bash
# Chunk all 4 systems of 104 Libraries:
for sys in Lib_JS Lib_PY Lib_SH Lib_TS; do
    python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
        --chunk "/storage/emulated/0/Admin/Libraries/libraries_104/$sys" \
        --dest "/storage/emulated/0/Admin/Libraries/Chunked_Libraries/104"
done

# Chunk all 4 systems of 105 Libraries:
for sys in Lib_JS Lib_PY Lib_SH Lib_TS; do
    python3 ~/.gemini/config/skills/chunking-core/scripts/Simple_Chunker_CLI.py \
        --chunk "/storage/emulated/0/Admin/Libraries/libraries_105/$sys" \
        --dest "/storage/emulated/0/Admin/Libraries/Chunked_Libraries/105"
done
```

---

## 4. Chunked-104a Schema Specification

Generated archives adhere to the BEJSON 104a Chunked schema:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Schema_Name": "Chunked-104a",
  "Schema_Version": "1.0.1",
  "Records_Type": ["Chunked"],
  "Fields": [
    {"name": "File_Name",      "type": "string"},
    {"name": "File_Extension", "type": "string"},
    {"name": "File_Content",   "type": "string"},
    {"name": "File_Version",   "type": "string"},
    {"name": "File_Hash",      "type": "string"},
    {"name": "Relative_Path",  "type": "string"},
    {"name": "Is_Binary",      "type": "boolean"},
    {"name": "Is_Mounted",     "type": "boolean"}
  ],
  "Values": [
    [
      "main.py",
      ".py",
      "print('hello world')",
      "latest",
      "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed",
      "src/main.py",
      false,
      false
    ]
  ]
}
```

---

## 5. When to Use & When NOT to Use

### Use This Skill When:
- Collapsing an entire multi-file project into a single portable `.104a.bejson.txt` container.
- Unchunking a `.bejson.txt` or `.bejson` file back into an unpacked project directory tree or `.zip` archive.
- Creating clean, text-only backups without project tracker files (`bejson_project.json`).
- Automatically staging chunked archives in the standard system archive pool (`/storage/emulated/0/Admin/Resources/Chunks`).
- Packaging the 4 Admin Library systems (`Lib_JS`, `Lib_PY`, `Lib_SH`, `Lib_TS`) into `/storage/emulated/0/Admin/Libraries/Chunked_Libraries/<104|105>`.

### Do NOT Use This Skill When:
- Packaging Multi-File Databases (MFDB) into `.mfdb132.bejson` chunk containers (use `mfdb-104-chunker`).
- Structured document project management, paragraph splitting, or Markdown compiling (use `bejson-document-chunker`).
- Modifying individual cells or querying relational tables in `.104.bejson` stores (use `bejson-104-core`).
- Upgrading 104 files to Format 105 UUID structures (use `bejson-105-upgrade-automator`).

---

## 6. Admin Libraries & 4-System Architectural Mapping

### 6.1 The 4 Systems
The central Admin Libraries ecosystem is partitioned across 4 runtime languages:
- **`Lib_JS`**: JavaScript runtime helpers, browser libraries, and DOM/UI scripts.
- **`Lib_PY`**: Python 3.10+ core algorithms, CMS backends, and tooling.
- **`Lib_SH`**: Bash / POSIX scripts, CLI menus, animations, and system scripts.
- **`Lib_TS`**: TypeScript typed schemas, interfaces, and utilities.

### 6.2 Source & Destination Topology
| Asset Tier | Source Path | Target Chunked Folder | Generated Chunks |
|---|---|---|---|
| **104 Libraries** | `/storage/emulated/0/Admin/Libraries/libraries_104` | `/storage/emulated/0/Admin/Libraries/Chunked_Libraries/104` | `Chunked_Lib_JS.104a.bejson.txt`<br>`Chunked_Lib_PY.104a.bejson.txt`<br>`Chunked_Lib_SH.104a.bejson.txt`<br>`Chunked_Lib_TS.104a.bejson.txt` |
| **105 Libraries** | `/storage/emulated/0/Admin/Libraries/libraries_105` | `/storage/emulated/0/Admin/Libraries/Chunked_Libraries/105` | `Chunked_Lib_JS.104a.bejson.txt`<br>`Chunked_Lib_PY.104a.bejson.txt`<br>`Chunked_Lib_SH.104a.bejson.txt`<br>`Chunked_Lib_TS.104a.bejson.txt` |
| **Scaffolds** | `/storage/emulated/0/Admin/Resources/Templates` | `/storage/emulated/0/Admin/Libraries/Chunked_Libraries/scaffolds` | `Chunked_Scaffold.104a.bejson.txt` |
| **Taxonomy** | `/storage/emulated/0/Admin/Libraries/Taxonomies` | `/storage/emulated/0/Admin/Libraries/Chunked_Libraries/taxonomy` | `Chunked_Taxonomies.104a.bejson.txt` |

### 6.3 Semantic Decoder & Speech-to-Text Normalization
When user requests contain acoustic, typo, or shorthand patterns, resolve them immediately according to this map:
- `chjnk`, `chunk`, `cunk`, `chumk` $\rightarrow$ invoke `chunking-core` skill via `Simple_Chunker_CLI.py`.
- `4 systems`, `four systems`, `thf 4 systems`, `all systems` $\rightarrow$ iterate through `Lib_JS`, `Lib_PY`, `Lib_SH`, `Lib_TS`.
- `104 libs`, `104 libraries` $\rightarrow$ `/storage/emulated/0/Admin/Libraries/libraries_104`.
- `105 libs`, `105 libraries` $\rightarrow$ `/storage/emulated/0/Admin/Libraries/libraries_105`.
- `chunked libraries folder in Admin Libraries` $\rightarrow$ `/storage/emulated/0/Admin/Libraries/Chunked_Libraries` (route into subfolder `104/` or `105/` based on library generation requested).
