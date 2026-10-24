---
name: project-bejson-cms-manage
description: >-
  Operational CLI workflow execution, entity lifecycle management, health auditing, disaster recovery, and single-file Chunked-104a database staging for BEJSON CMS using cms-manage.py and cms_database_chunker.py. Use when executing cms-manage commands, running CMS doctor audits, managing pages, categories, or authors, performing database snapshot chunking, or optimizing assets. Do NOT use for architectural navigation or schema grounding (use project-bejson-cms-grounding), low-level raw BEJSON file mutations (use bejson-104-core), or general skill scaffolding (use skill-architect).
---

# project-bejson-cms-manage (Layer 3 Project Domain Management & CLI Operations)

## Summary

`project-bejson-cms-manage` provides operational execution workflows, command orchestration, entity lifecycle mutations, health checks, and single-file Chunked-104a database staging for BEJSON CMS located at `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`. It drives the live management layer via `src/cms-manage.py` and the embedded custom variant of Simple Chunker (`scripts/cms_database_chunker.py`).

## When to Use

- Executing live administrative commands via `cms-manage.py` (status, doctor, backup, restore, reset).
- Mutating CMS entities: creating or editing pages, categories, author profiles, navigation links, social links, ads, or standalone apps.
- Executing cascading category renames (`category rename`), category merges (`category merge`), or author renames (`author rename`).
- Performing fuzzy entity lookups across all 10 registered types using `find <entity> <query>`.
- Converting image assets from PNG to WebP and updating markdown page references via `asset optimize`.
- Staging and snapshotting the entire live database into a single flat `.104a.bejson.txt` archive using `cms_database_chunker.py`.
- Running a single foreground Flask service for testing via `serve <service>`.

## When NOT to Use

- Architectural navigation, sitemaps, port topology, or static build pipeline grounding (use `project-bejson-cms-grounding`).
- Low-level standalone BEJSON CRUD operations outside the CMS domain (use `bejson-104-core`).
- Authoring or scaffolding new agent skill manifests or auditing skill topologies (use `skill-architect`).

---

## 1. Primary CLI Entrypoint (`cms-manage.py`)

The live management CLI is located at:
`/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS/src/cms-manage.py`

Execute directly via Python 3:
```bash
python3 /storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS/src/cms-manage.py <command> [<args>]
```

Or via the bundled execution runner:
```bash
python3 scripts/run_cms_manage.py <command> [<args>]
```

### Essential Commands
- **`status`**: Inspects CMS data root, live manifest existence, and dirty state.
- **`doctor`**: Verifies zero orphaned category/author references on pages and detects case-insensitive duplicate names across entities.
- **`find <entity> <query>`**: Fuzzy case-insensitive name-to-UUID lookup across all 10 registered entity types.
- **`backup`**: Creates an automated timestamped snapshot zip in `storage/exports/`.
- **`restore <zip_path>`**: Atomically restores database state from a verified zip file.

---

## 2. Entity Management & Cascade Protocol

All entity modifications respect database referential integrity:

### 2.1 Category Operations
- `category add <name> <slug> [--desc <text>] [--type <kind>]`
- `category rename <slug> <new_name>`: Updates category title and cascades the new name to all matching `page_cat_name` entries in `pages.104.bejson`.
- `category merge <source_slug> <into_slug>`: Reassigns pages from `source_slug` to `into_slug`, updates `page_cat_uuid`, and deletes the source.
- *Guard*: The system protects `"Uncategorized"` (`cat_name: "Uncategorized"`) from deletion or rename.

### 2.2 Author Operations
- `author add <name> [--bio <text>] [--image <url>]`: Case-insensitively deduplicated.
- `author rename <old_name> <new_name>`: Renames author profile and cascades the update to all matching page bylines.

### 2.3 Page Operations
- `page add <title> <slug> --author <name> --cat <name> --content <text>`: Automatically resolves and sets `page_cat_uuid` and `page_author_uuid`.
- `page update <uuid> [--title <title>] [--content <text>] [--cat <category>]`
- `page delete <uuid>`
- `page list`

### 2.4 Media Optimization & External Media
- `asset optimize [--dry-run]`: Converts PNG images to compressed WebP format and automatically updates active markdown page links.
- `asset add-external <name> <url> [--type pdf|video]`: Registers off-host embed media.

---

## 3. Database Staging & Snapshot Chunker (`cms_database_chunker.py`)

The skill embeds a custom variant of Simple Chunker specialized for full BEJSON CMS database staging:

```bash
# Snapshot only the central site_master database (manifest + 10 tables)
python3 scripts/cms_database_chunker.py --site-master

# Stage and snapshot the full MFDB database directory
python3 scripts/cms_database_chunker.py --stage

# Stage database including base64-encoded binary assets
python3 scripts/cms_database_chunker.py --stage --include-binary

# Restore a Chunked-104a snapshot back into the live database
python3 scripts/cms_database_chunker.py --restore /storage/emulated/0/Admin/Resources/Chunks/Chunked_BEJSON_CMS_SiteMaster_20261021_145618.104a.bejson.txt
```

### Snapshot Invariants:
1. Conforms to the canonical **Chunked-104a** schema (`Schema_Name: Chunked-104a`).
2. Calculates SHA-256 cryptographic hashes for every file.
3. Restores with strict SHA-256 verification and atomic file writes.

---

## 4. Operational References

- Command Cheat Sheet: [`references/cli_commands_cheat_sheet.md`](./references/cli_commands_cheat_sheet.md)
- Safety & Recovery Guide: [`references/operational_safety_and_recovery.md`](./references/operational_safety_and_recovery.md)
- Chunking & Snapshot Guide: [`references/cms_chunking_and_snapshot_guide.md`](./references/cms_chunking_and_snapshot_guide.md)
