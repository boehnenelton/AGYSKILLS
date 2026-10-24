# BEJSON CMS - cms-manage.py Unified CLI Toolkit Reference

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Effective Date: 2026-10-21
RELATIONAL_ID: d3e4f5a6-7b8c-4d9e-0f1a-2b3c4d5e6f7a
Version: 100
Release_Version: 300

---

## 1. Overview & Architecture

`cms-manage.py` is the unified command-line interface for BEJSON CMS operations. Located at `src/cms-manage.py` (Version 18.12), it bypasses legacy disconnected workspaces and operates directly against live data via `lib_bejson_CMS_cms_core.py` (`CMSCore`) targeting `storage/mfdb/site_master/104a.mfdb.bejson`.

### Global CLI Syntax
```bash
python3 src/cms-manage.py [--version] [-h] <command> [<args>]
```

---

## 2. Diagnostics, Health & Integrity

### `status`
Displays current storage root, live manifest existence, mounted status, and dirty state flags.
```bash
python3 src/cms-manage.py status
```

### `doctor`
Performs an automated health audit:
1. **Orphaned FK Audit**: Detects any `PageRecord` referencing a category name (`page_cat_name`) or author name (`page_author_name`) that does not exist in `categories.104.bejson` or `authors.104.bejson`.
2. **Case-Insensitive Collision Audit**: Flags duplicate display names across `AuthorProfile`, `Category`, `NavLink`, `SocialLink`, and `AI_Profile`.
- Returns Exit Code `0` if clean, Exit Code `1` if issues are discovered (suitable for CI/CD checks and cron jobs).
```bash
python3 src/cms-manage.py doctor
```

### `find <entity> <query>`
Performs a fuzzy, case-insensitive name-to-UUID lookup across all 10 registered entity types.
```bash
python3 src/cms-manage.py find author "Elton"
python3 src/cms-manage.py find category "Tech"
python3 src/cms-manage.py find page "Getting Started"
```

---

## 3. Disaster Recovery & Snapshot Management

### `backup`
Creates a full, timestamped snapshot archive of the live MFDB store into `storage/exports/`.
```bash
python3 src/cms-manage.py backup
```

### `restore <backup_path>`
Safely restores the live MFDB state from a verified backup zip archive using `safe_extract_zip`.
```bash
python3 src/cms-manage.py restore storage/exports/backup_20261021_120000.zip
```

### `factory-reset`
Resets the live database back to initial bootstrap seeds (`Uncategorized` category, default site configuration, and default author). Prompts for explicit interactive confirmation.
```bash
python3 src/cms-manage.py factory-reset
```

---

## 4. Entity Lifecycle Commands

### Pages (`page`)
- `page add <title> <slug> --author <author> --cat <category> --content <file_or_text>`
  Automatically resolves `page_cat_uuid` and `page_author_uuid` via `_resolve_page_fk_uuids()`.
- `page update <uuid> [--title <title>] [--content <text>] [--cat <category>]`
- `page delete <uuid>`
- `page list`
- `page import <file> [--format json|csv]`
  Imports records with automatic fresh UUID allocation to prevent identifier collisions.

### Categories (`category`)
- `category add <name> <slug> [--desc <desc>] [--type <type>]`
- `category rename <slug> <new_name>`
  Renames the category and automatically cascades the new name to every matching `page_cat_name` across `pages.104.bejson`. Protects the canonical `"Uncategorized"` category from renaming.
- `category merge <source_slug> <into_slug>`
  Reassigns all pages in `source_slug` to `into_slug`, updates `page_cat_uuid` to the target category UUID, and deletes the source category.
- `category delete <slug>`
- `category list`

### Authors (`author`)
- `author add <name> [--bio <bio>] [--image <url>]`
  Guarded against duplicate additions case-insensitively.
- `author rename <old_name> <new_name>`
  Renames the author profile and cascades updates to all referencing page bylines.
- `author update <name> [--bio <bio>] [--image <url>]`
- `author delete <name>`
- `author list`

### Navigation & Social Links (`navlink` / `social`)
- `navlink add <label> <url> [--order <int>]`
- `navlink delete <label>`
- `navlink list`
- `social add <platform> <url>`
- `social delete <platform>`
- `social list`

### Media Assets & Off-Host Embeds (`asset`)
- `asset add <file_path>`
  Hashes file, records MIME type, and registers in `media_assets.104.bejson`.
- `asset delete <asset_filename>`
- `asset optimize [--dry-run]`
  Scans PNG assets, converts them into compressed WebP format, updates live asset records, and re-points markdown page references.
- `asset add-external <name> <url> [--type pdf|video]`
  Registers external embedded media (e.g. PDF documents or third-party hosted content).
- `asset delete-external <uuid>`
- `asset list-external`

### Standalone Web Apps (`app`)
- `app add <name> [--desc <desc>] [--entry <path>] [--image <url>]`
  Registers standalone applications with automated `app_created_at` timestamping.
- `app delete <uuid>`
- `app list`

### Site Configuration (`config`)
- `config set <key> <value> [--desc <desc>]`
- `config delete <key>`
- `config list`

### Microservice Foreground Runner (`serve`)
Starts a single CMS service in the foreground (blocks until Ctrl+C):
```bash
python3 src/cms-manage.py serve cms        # Starts Admin Portal on Port 5000
python3 src/cms-manage.py serve publisher  # Starts Static Publisher on Port 5001
python3 src/cms-manage.py serve editorv2   # Starts Page Editor V2 on Port 5002
python3 src/cms-manage.py serve profiles   # Starts Profile Manager on Port 5003
```
