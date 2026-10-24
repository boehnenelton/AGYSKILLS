# BEJSON CMS - Architectural Map & Subsystem Blueprint

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Effective Date: 2026-10-21
RELATIONAL_ID: 8a7f1c24-4e9b-4d62-a108-9d5e3c7b20f1
Version: 100
Release_Version: 300

---

## 1. Executive Summary & Zero-SQL Paradigm

BEJSON CMS is a zero-SQL, self-hosted Content Management System and static site publication framework engineered to operate without heavyweight database daemons (such as MySQL, PostgreSQL, or Redis) and without binary SQLite stores. It runs natively across resource-constrained environments including Android Termux and Pydroid3, as well as desktop Linux, macOS, and Windows workstations.

All persistent domain data is stored in human-readable, schema-strict BEJSON 104 tabular files coordinated by a central Multi-File Database (MFDB v1.31) manifest.

> [!NOTE]
> System Development Policy Override: Canonical `$PROJECT_INDEX_ROOT/cli_project_register.py` is not hosted on this local device environment and is explicitly exempt from automated project registration.

---

## 2. Directory & Repository Topology

The canonical development repository is located at:
`/storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS`

```text
BEJSON_CMS/
├── .bejson_project.json       # Project tracker (v18.29, PKG 145)
├── README.md                  # Professional documentation with TOC and visual tours
├── AGENTS.md                  # Multi-agent operating contracts & instructions
├── CHANGELOG.md               # Continuous chronological release ledger
├── advanced_launcher.py       # Multi-service interactive CLI supervisor with PID tracking
├── cms_launcher.sh            # Classic foreground launcher script
├── config.json                # BEJSON 104a bootstrap configuration
├── dev/                       # Development notes (dead code, variable audits, security)
├── docs/                      # Architectural overviews, findings, and technical reports
├── images/                    # UI screenshots and documentation media assets
├── resources/                 # Base skeletons, CSS themes (dark.css, light.css), templates
├── src/                       # Application source code
│   ├── cms-manage.py          # Unified CLI Toolkit (v18.12)
│   ├── lib/                   # Local core and CMS libraries
│   │   ├── lib_bejson_Core_bejson_core.py
│   │   ├── lib_bejson_Core_bejson_env.py
│   │   ├── lib_bejson_Core_mfdb_core.py
│   │   ├── lib_bejson_CMS_cms_core.py
│   │   ├── lib_bejson_CMS_cms_mfdb.py
│   │   ├── lib_bejson_CMS_cms_ports.py
│   │   └── lib_bejson_CMS_taxonomy.py
│   └── web/                   # Decoupled Flask microservice fleet
│       ├── BEJSON_CMS_Admin.py
│       ├── BEJSON_CMS_Content.py
│       ├── BEJSON_CMS_FileBrowser.py
│       ├── BEJSON_CMS_Interface.py
│       ├── BEJSON_CMS_Media.py
│       ├── BEJSON_CMS_PageEditorV2.py
│       ├── BEJSON_CMS_ProfileManager.py
│       ├── BEJSON_CMS_Publisher.py
│       ├── BEJSON_CMS_Renderers.py
│       ├── BEJSON_CMS_Shared.py
│       └── BEJSON_CMS_System.py
├── storage/                   # Persistent runtime and database storage
│   ├── mfdb/                  # Live MFDB tabular databases
│   │   ├── site_master/       # Central manifest: 104a.mfdb.bejson
│   │   └── site_master/data/  # Federated .104.bejson entity tables
│   ├── builds/                # Exported static site output (HTML, CSS, assets)
│   ├── assets/                # Local uploaded media files
│   ├── exports/               # Snapshot archives and entity data exports
│   ├── logs/                  # Service runtime execution logs
│   ├── standalone_apps/       # Registered standalone mini-applications
│   └── tmp/                   # Transient locks and PID registries
└── tools/                     # Maintenance tools (audit_taxonomy.py, migrate_taxonomy.py)
```

---

## 3. Storage Architecture: MFDB 104 Federation

The live database is orchestrated by the central manifest:
`storage/mfdb/site_master/104a.mfdb.bejson`

This manifest federates 10 independent tabular entity stores located in `storage/mfdb/site_master/`:

| Entity Store | Primary Key | Key Prefix | Responsibility |
| :--- | :--- | :--- | :--- |
| `pages.104.bejson` | `page_uuid` | `page_` | Article content, slugs, publication status, timestamps, and relational FKs (`page_cat_uuid`, `page_author_uuid`) |
| `categories.104.bejson` | `cat_uuid` | `cat_` | Editorial taxonomy categories, slugs, feed types, and descriptions |
| `authors.104.bejson` | `author_uuid` | `author_` | Author profiles, display names, bios, images, and social handles |
| `media_assets.104.bejson` | `asset_uuid` | `asset_` | Local media file metadata, SHA-256 hashes, WebP optimization state |
| `external_media.104.bejson` | `extmedia_uuid`| `extmedia_`| Off-host embeds (PDF documents, external CDN audio/video links) |
| `site_config.104.bejson` | `sys_uuid` | `sys_` | Global site preferences, blog title, tagline, and theme parameters |
| `navigation.104.bejson` | `nav_uuid` | `nav_` | Header navigation links, drawer hierarchies, and ordering indices |
| `advertisements.104.bejson` | `ad_uuid` | `ad_` | Sponsored banners, CTA cards, click URLs, and zone allocations |
| `standalone_apps.104.bejson`| `app_uuid` | `app_` | Sandboxed standalone web applications mounted into the CMS |
| `personas.104.bejson` | `persona_uuid`| `persona_`| AI personas and system prompts for automated content generation |

### Key Referential Integrity Invariants:
1. **Dynamic Field Map Caching**: Every access to BEJSON rows resolves column positions via an O(1) `field_map = {f['name']: i for i, f in enumerate(doc['Fields'])}`. Positional hardcoding (`row[0]`) is strictly avoided.
2. **Atomic Mutations**: Persistent writes write to `.tmp`, execute `fsync()`, and perform atomic rename replacement.
3. **Foreign Key Synchronization**: In `pages.104.bejson`, human-readable `page_cat_name` and `page_author_name` are kept in lockstep with `page_cat_uuid` and `page_author_uuid`.

---

## 4. Service Fleet & Port Topology

The CMS runtime decomposes into specialized Flask microservices that operate concurrently:

| Service | Port | Primary Executable | Core Responsibility |
| :--- | :--- | :--- | :--- |
| **Admin Portal** | `5000` | `src/web/BEJSON_CMS_Admin.py` | Administrative dashboard, metrics, database status, system controls |
| **Static Publisher** | `5001` | `src/web/BEJSON_CMS_Publisher.py` | Compiles live MFDB records into static HTML/CSS in `storage/builds/` |
| **Page Editor V2** | `5002` | `src/web/BEJSON_CMS_PageEditorV2.py` | Live markdown and HTML authoring, preview, and category assignment |
| **Profile Manager** | `5003` | `src/web/BEJSON_CMS_ProfileManager.py` | Author profiles, persona definitions, and AI prompt engineering |

### Process Supervision via `advanced_launcher.py`:
- Tracks process IDs in `storage/tmp/launcher_registry.json`.
- Allows individual microservices to be stopped or restarted without killing the entire fleet.
- Color-coded terminal HUD using `#DE2626` accent styling per Policy 8.1.
