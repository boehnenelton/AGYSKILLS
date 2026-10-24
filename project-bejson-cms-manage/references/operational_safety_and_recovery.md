# BEJSON CMS - Operational Safety, Data Integrity & Recovery Protocol

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Effective Date: 2026-10-21
RELATIONAL_ID: e5f6a7b8-9c0d-1e2f-3a4b-5c6d7e8f9a0b
Version: 100
Release_Version: 300

---

## 1. Data Integrity & Negative Guardrails

`cms-manage.py` implements runtime constraints designed to prevent silent data corruption or orphaned references:

### 1.1 The "Uncategorized" Protection Guard
- The default category `"Uncategorized"` (`cat_name: "Uncategorized"`, `cat_slug: "uncategorized"`) is load-bearing. The system self-heal mechanism recreates this category on boot if missing.
- `cms-manage.py` strictly refuses to rename or delete the `"Uncategorized"` category to avoid creating orphaned records or duplicate recovery entries.

### 1.2 Referential Integrity Cascades
- **Category Renames**: When `category rename <slug> <new_name>` is called, the CLI updates `cat_name` in `categories.104.bejson` and immediately cascades the update to `page_cat_name` across all matching rows in `pages.104.bejson`.
- **Category Merges**: When `category merge <source> <into>` is executed, all referencing pages have their `page_cat_name` updated to the target category name and their `page_cat_uuid` set to the target category UUID. The source category is deleted only after the cascade completes.
- **Author Renames**: Calling `author rename <old> <new>` updates `author_display_name` in `authors.104.bejson` and cascades the updated name to `page_author_name` across all matching page bylines.

### 1.3 Case-Insensitive Uniqueness Enforcement
- Author profile additions (`author add`) and Category additions (`category add`) compare names case-insensitively before insertion.
- `doctor` reports any collisions that could lead to ambiguous entity lookups.

---

## 2. Disaster Recovery Protocol

### 2.1 Generating Pre-Mutation Snapshots
Always generate a verified snapshot before performing non-trivial batch updates, bulk imports, or migrations:
```bash
python3 src/cms-manage.py backup
```
Snapshots are compressed zip archives written to `storage/exports/` containing the exact byte-level state of all 10 tabular stores and manifest definitions.

### 2.2 Restoring from Archive
In the event of accidental data corruption or schema mismatch:
```bash
python3 src/cms-manage.py restore /storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS/storage/exports/<backup_name>.zip
```
The restore procedure validates the zip structure, checks for path traversal vulnerabilities (`safe_extract_zip`), and atomically replaces corrupted stores.
