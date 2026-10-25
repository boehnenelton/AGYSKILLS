# NewAgent CMS (`newagent-manage.py`) Full CLI Reference

Author: Elton Boehnen  
Repository: `/storage/emulated/0/Admin/Dev/Repos/NewAgent/tools/NA-CMS`  
Version: `20.1`  
Relational_ID: `3e7c1a9d-5f2b-4d8e-9a3c-6b1f8e4d2c7a`  

---

## Command Matrix

| Command Group | Command Syntax | Description |
|---|---|---|
| **System** | `newagent-manage status` | Displays data root, live manifest existence, and dirty state |
| | `newagent-manage build` | Compiles static site directly into `storage/builds/` |
| | `newagent-manage publish` | Alias for `build` |
| | `newagent-manage backup [--dir DIR]` | Timestamped zip backup of live database |
| | `newagent-manage restore <zip_file>` | Restores live database atomically from verified zip |
| | `newagent-manage factory-reset` | Wipes live data and restores pristine baseline |
| **Pages** | `newagent-manage page list` | Lists all registered pages in manifest |
| | `newagent-manage page add "Title" --category "CatName" --author "Author" --body file.html` | Two-part page creation (manifest row + `pages_db/<uuid>.json`) |
| | `newagent-manage page update <uuid> "Title" [--category Cat] [--author Auth] [--image file.webp]` | Updates page title, category, author, or featured image |
| | `newagent-manage page delete <uuid>` | Removes manifest entry and deletes `pages_db/<uuid>.json` |
| | `newagent-manage page import --html file.html --title "Title" --category "CatName" [--author "Author"] [--type blog] [--featured-img file.svg]` | Imports semantic HTML file into new page/blog post |
| | `newagent-manage page import --app <app_uuid> --title "Title"` | Wires standalone web app into page route |
| **Categories** | `newagent-manage category list` | Lists categories (name and slug) |
| | `newagent-manage category add "Name" slug [--desc Desc] [--type Type]` | Adds editorial category |
| | `newagent-manage category update slug "Updated Name"` | Updates category name by slug |
| | `newagent-manage category delete slug` | Deletes category by slug (cannot delete "Uncategorized") |
| **Authors** | `newagent-manage author list` | Lists author profiles (display name, avatar, bio) |
| | `newagent-manage author add "Name" [--bio Bio] [--image avatar.jpg]` | Adds author profile |
| | `newagent-manage author update "Name" [--bio Bio]` | Updates author profile |
| | `newagent-manage author delete "Name"` | Deletes author profile |
| **Skeletons** | `newagent-manage skeleton list [--theme Theme]` | Lists registered skeletons and tag counts |
| | `newagent-manage skeleton show <theme> <name> [--draft]` | Displays raw skeleton HTML |
| | `newagent-manage skeleton edit <theme> <name>` | Opens draft copy in `$EDITOR` |
| | `newagent-manage skeleton diff <theme> <name>` | Shows unified diff between draft and live file |
| | `newagent-manage skeleton validate [--theme Theme]` | Validates all registered `{{tag}}` contracts |
| | `newagent-manage skeleton promote <theme> <name>` | Backs up live file to `_history/`, validates tags, commits draft |
| | `newagent-manage skeleton discard <theme> <name>` | Discards active draft copy |
| | `newagent-manage skeleton new-theme <name> [--from default]` | Clones skeleton set into a new theme directory |
| **Assets & Apps** | `newagent-manage asset list` | Lists registered local media assets |
| | `newagent-manage asset add <file>` | Ingests asset with SHA-256 deduplication |
| | `newagent-manage asset delete <filename>` | Deletes asset |
| | `newagent-manage asset optimize [--dry-run]` | Converts PNGs to WebP and rewrites page references |
| | `newagent-manage asset add-external "Name" <url> [--type pdf\|video]` | Adds off-host external media record |
| | `newagent-manage app list` | Lists registered standalone web apps |
| | `newagent-manage app add "Name" --entry index.html [--desc Desc]` | Registers standalone app |
| | `newagent-manage app delete <app_uuid>` | Deletes standalone app |
| **UI & Nav** | `newagent-manage navlink list` | Lists header navigation links |
| | `newagent-manage navlink add "Label" /url [--order N]` | Adds navigation link |
| | `newagent-manage navlink delete "Label"` | Deletes navigation link |
| | `newagent-manage ad list` | Lists ad units |
| | `newagent-manage ad add "Name" img_url target_url zone` | Adds advertisement unit |
| | `newagent-manage config list` | Lists global key-value configuration |
| | `newagent-manage config set key value` | Sets global config property |
| **Services** | `newagent-manage serve <admin\|publisher>` | Runs foreground Flask service for testing |
