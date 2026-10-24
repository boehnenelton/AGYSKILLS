---
name: project-bejson-cms-grounding
description: >-
  Grounding, architectural mapping, schema inspection, and operational navigation for the zero-SQL BEJSON CMS publishing platform and MFDB data layer. Use when analyzing BEJSON CMS architecture, navigating src/web microservices, inspecting 104a.mfdb.bejson schemas, or auditing static publishing pipelines. Do NOT use for active cms-manage.py CLI execution workflows (use project-bejson-cms-manage), raw single-table BEJSON CRUD (use bejson-104-core), general multi-file database manifest validation (use mfdb-104-core), or general skill scaffolding (use skill-architect).
---

# project-bejson-cms-grounding (Layer 5 Project Domain Grounding & Architectural Mapper)

## Summary

`bejson-cms-grounding` provides authoritative grounding, architectural blueprints, schema specifications, and operational navigation patterns for the zero-SQL BEJSON CMS platform located at `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`. It bridges the high-level decoupled microservices in `src/web/`, the central Multi-File Database (MFDB v1.31) manifest in `storage/mfdb/site_master/104a.mfdb.bejson`, and the unified command-line toolkit `src/cms-manage.py`.

## When to Use

- Analyzing or modifying the BEJSON CMS codebase, its Flask microservice fleet, or its static export publisher.
- Navigating the 10 federated BEJSON 104 entity tables (`pages`, `categories`, `authors`, `media_assets`, `external_media`, `site_config`, `navigation`, `advertisements`, `standalone_apps`, `personas`).
- Inspecting administrative CLI capabilities, health checks (`doctor`), cascading renames, or disaster recovery architecture.
- Auditing foreign-key synchronization (`page_cat_uuid`, `page_author_uuid`) and case-insensitive uniqueness constraints.
- Supervising persistent background processes via `advanced_launcher.py`.

## When NOT to Use

- Running active CLI management commands, entity CRUD mutations, or database backups via cms-manage.py (use `project-bejson-cms-manage`).
- Direct low-level CRUD mutations on standalone `.104.bejson` tables without CMS domain rules (use `bejson-104-core`).
- Validating general MFDB manifest schemas and parent-child hierarchy trees outside the CMS domain (use `mfdb-104-core`).
- Authoring or scaffolding new multi-tier agent skills or linting skill packages (use `skill-architect`).

---

## 1. System Topology & Core Repository Mapping

Canonical Repository Path: `/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`

```text
BEJSON_CMS/
|-- .bejson_project.json       # Project tracker (v18.29, PKG 145)
|-- README.md                  # Comprehensive documentation and visual tours
|-- advanced_launcher.py       # Background service manager (PID tracking, #DE2626 theme)
|-- cms_launcher.sh            # Classic interactive shell launcher
|-- config.json                # Bootstrap 104a configuration
|-- src/
|   |-- cms-manage.py          # Unified CLI Toolkit (v18.12)
|   |-- lib/                   # Domain and core libraries (CMSCore, MFDBManager, Ports)
|   `-- web/                   # Decoupled Flask microservice fleet
|       |-- BEJSON_CMS_Admin.py          (Port 5000: Admin portal and dashboard)
|       |-- BEJSON_CMS_Publisher.py      (Port 5001: Zero-JS static site compiler)
|       |-- BEJSON_CMS_PageEditorV2.py   (Port 5002: Dynamic markdown/HTML editor)
|       `-- BEJSON_CMS_ProfileManager.py (Port 5003: Author and persona configuration)
`-- storage/
    |-- mfdb/site_master/      # Central database manifest and entity stores
    |   |-- 104a.mfdb.bejson   # Central site manifest
    |   `-- *.104.bejson       # 10 tabular entity stores
    `-- builds/                # Static export destination (pure HTML/CSS)
```

> [!NOTE]
> Policy Override Record: `$PROJECT_INDEX_ROOT/cli_project_register.py` is not hosted on this device. Automated project registration is explicitly exempt per user instruction.

---

## 2. Storage Architecture: MFDB 104 Federation

All persistent storage routes through `storage/mfdb/site_master/104a.mfdb.bejson`. Ten independent tabular stores maintain strict domain isolation:

1. **`pages.104.bejson`** (PK: `page_uuid`, prefix: `page_`): Article body, slug, metadata, and synchronized foreign keys (`page_cat_uuid`, `page_author_uuid`).
2. **`categories.104.bejson`** (PK: `cat_uuid`, prefix: `cat_`): Editorial categories with case-insensitive uniqueness and protected `"Uncategorized"` category.
3. **`authors.104.bejson`** (PK: `author_uuid`, prefix: `author_`): Author profiles, avatars, and bios with case-insensitive uniqueness.
4. **`media_assets.104.bejson`** (PK: `asset_uuid`, prefix: `asset_`): Local media registry, MIME types, and SHA-256 hashes.
5. **`external_media.104.bejson`** (PK: `extmedia_uuid`, prefix: `extmedia_`): Off-host linked media (PDFs, external CDN video).
6. **`site_config.104.bejson`** (PK: `sys_uuid`, prefix: `sys_`): Global key-value site parameters.
7. **`navigation.104.bejson`** (PK: `nav_uuid`, prefix: `nav_`): Header and drawer menu items with ordering weights.
8. **`advertisements.104.bejson`** (PK: `ad_uuid`, prefix: `ad_`): Ad units, target URLs, and placement zones.
9. **`standalone_apps.104.bejson`** (PK: `app_uuid`, prefix: `app_`): Mounted mini-apps with `app_created_at` timestamps.
10. **`personas.104.bejson`** (PK: `persona_uuid`, prefix: `persona_`): AI personas and system prompts linked via `persona_author_fk`.

### Dynamic Field Map Invariant
In compliance with BEJSON Core standards, table rows are never accessed via static hardcoded positional offsets. All column lookups compile an O(1) dictionary:

```python
field_map = {f["name"]: i for i, f in enumerate(doc["Fields"])}
page_title = row[field_map["page_title"]]
```

---

## 3. CLI Operations via `cms-manage.py`

The CLI tool operates at `src/cms-manage.py` against live data:

### Health Diagnostics
- `python3 src/cms-manage.py status`: Storage paths, manifest presence, and dirty change status.
- `python3 src/cms-manage.py doctor`: Audits orphaned FK references (`page_cat_name`, `page_author_name`) and case-insensitive duplicate names.
- `python3 src/cms-manage.py find <entity> <query>`: Fuzzy name-to-UUID lookup across all 10 registered entities.

### Cascading Modifications
- `category rename <slug> <new_name>`: Renames category display name and cascades updates to all referencing `page_cat_name` entries across `pages.104.bejson`.
- `category merge <source_slug> <into_slug>`: Reassigns pages from source to destination category, updates `page_cat_uuid`, and deletes source.
- `author rename <old_name> <new_name>`: Cascades author rename across all matching page bylines.

### Disaster Recovery & Maintenance
- `backup`: Produces timestamped zip snapshot in `storage/exports/`.
- `restore <zip_path>`: Atomic restore using safe zip extraction.
- `asset optimize`: Automatic PNG to WebP conversion and live markdown link updating.
- `serve <service>`: Foreground execution for single service testing (`cms`, `publisher`, `editorv2`, `profiles`).

---

## 4. Verification Workflow

Run the bundled verification script to ensure the environment, manifest, and live diagnostics pass:

```bash
python3 scripts/verify_cms_environment.py
```

Detailed specifications reside in:
- Architectural map: [`references/bejson_cms_architectural_map.md`](./references/bejson_cms_architectural_map.md)
- CLI Toolkit reference: [`references/cms_manage_cli_reference.md`](./references/cms_manage_cli_reference.md)
- Schema registry: [`references/entity_schema_registry.md`](./references/entity_schema_registry.md)
