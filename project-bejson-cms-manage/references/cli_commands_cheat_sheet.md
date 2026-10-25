# BEJSON CMS - cms-manage CLI Command Cheat Sheet & Recipes

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Effective Date: 2026-10-21
RELATIONAL_ID: 9c8b7a6f-5e4d-3c2b-1a0f-8e7d6c5b4a32
Version: 100
Release_Version: 300

---

## 1. Fast Command Index

All commands run via the unified CLI entrypoint:
`python3 /storage/emulated/0/Admin/Dev/Python/Development/BEJSON_CMS/src/cms-manage.py <command> [<args>]`

| Command | Subcommand | Description | Example |
| :--- | :--- | :--- | :--- |
| `status` | - | Print data root, live manifest path, dirty state | `cms-manage.py status` |
| `doctor` | - | Audit orphaned FKs and duplicate name collisions | `cms-manage.py doctor` |
| `find` | `<entity> <query>` | Case-insensitive fuzzy search returning UUIDs | `cms-manage.py find author "Elton"` |
| `backup` | - | Create live MFDB snapshot zip in `storage/exports/` | `cms-manage.py backup` |
| `restore` | `<zip>` | Restore database from verified zip archive | `cms-manage.py restore backup.zip` |
| `factory-reset`| - | Reset DB to canonical bootstrap seeds | `cms-manage.py factory-reset` |
| `export` | `<entity> <file>` | Export entity records to JSON or CSV | `cms-manage.py export pages pages.json` |
| `import` | `<entity> <file>` | Import records with fresh UUID generation | `cms-manage.py import pages pages.json` |
| `page` | `add` | Create article and resolve FK UUIDs | `cms-manage.py page add "Title" --category "BEJSON"` |
| `page` | `import` | Import pre-compiled HTML page or app embed | `cms-manage.py page import --html post.html --title "Title" --category "BEJSON" --type blog` |
| `page` | `update` | Update page title, content, or category | `cms-manage.py page update <uuid> --title "New"` |
| `page` | `delete` | Delete page by UUID | `cms-manage.py page delete <uuid>` |
| `page` | `list` | List all pages | `cms-manage.py page list` |
| `category` | `add` | Add new category | `cms-manage.py category add "Dev" "dev"` |
| `category` | `rename` | Rename category (cascades across all pages) | `cms-manage.py category rename "dev" "Development"` |
| `category` | `merge` | Merge source category into target and delete source | `cms-manage.py category merge "old-slug" "new-slug"` |
| `category` | `delete` | Delete category by slug | `cms-manage.py category delete "slug"` |
| `author` | `add` | Add author profile (case-insensitive dedup) | `cms-manage.py author add "Jane Doe" --bio "Writer"` |
| `author` | `rename` | Rename author (cascades to all page bylines) | `cms-manage.py author rename "Jane Doe" "Jane Smith"` |
| `author` | `update` | Update author bio or image | `cms-manage.py author update "Jane" --bio "New bio"` |
| `asset` | `add` | Register media file with SHA-256 hash | `cms-manage.py asset add /path/to/img.png` |
| `asset` | `optimize` | Convert PNG assets to WebP and repoint references | `cms-manage.py asset optimize` |
| `asset` | `add-external` | Register external PDF or CDN media | `cms-manage.py asset add-external "Report" "https://..."` |
| `app` | `add` | Register standalone web application | `cms-manage.py app add "Dashboard" --entry "index.html"` |
| `config` | `set` | Set site config key/value | `cms-manage.py config set site_title "My CMS"` |
| `serve` | `<service>` | Start foreground service (`cms`, `publisher`, etc.) | `cms-manage.py serve publisher` |

---

## 2. Practical Execution Recipes

### Recipe A: Safe Category Consolidation
Merge a legacy category into a primary category without orphaning article records:
```bash
# 1. Health check baseline
python3 src/cms-manage.py doctor

# 2. Backup current state
python3 src/cms-manage.py backup

# 3. Merge legacy category into target
python3 src/cms-manage.py category merge "dev-notes" "engineering"

# 4. Verify zero orphaned pages remain
python3 src/cms-manage.py doctor
```

### Recipe B: Batch Asset Optimization
Convert raw image assets to modern WebP format while preserving markdown page link integrity:
```bash
# 1. Preview changes without mutation
python3 src/cms-manage.py asset optimize --dry-run

# 2. Execute optimization and file link updates
python3 src/cms-manage.py asset optimize

# 3. Re-export static site to apply new asset links
python3 src/cms-manage.py serve publisher
```
