---
name: user:skills-backup-manager
description: Audit, package, and back up user-created skills to the dedicated Google Drive skill ecosystem folders whenever skills are added, modified, or on a scheduled cadence. Use when the user asks to back up skills, archive skills, export skills to Drive, sync modified skills to the skill backup directory, or verify skill backup integrity.
allowed-tools: drive Do NOT use for general project release packaging (use project-delivery-packager) or session initialization download sweeps (use file-archive-coordinator).
---
# skills-backup-manager

Audits, bundles, and archives user-created skills to Elton Boehnen's Google Drive skill ecosystem directories whenever skills are updated or changed.

## When to Use

- Back up user-created skills to Google Drive.
- Check for newly added or modified skills compared to existing backup archives.
- Export clean single-tier zip archives of active skills to designated backup folders.
- Scheduled or automated backup sweeps of the skills repository.

## Target Backup Locations

All backups route to the `04_SKILLS_ECOSYSTEM` catalog in Google Drive:
- **Active Skills**: `Active_Skills_Bundle` (for delta and incremental snapshots).
- **All Installed Skills**: `All_Installed_Skills_Backup` (for full cumulative repository archives).

## Steps

1. **Inspect Installed User Skills**:
   - Enumerate all active user-created skills (excluding system-internal skills).
   - Collect their names, descriptions, triggers, and full markdown bodies.

2. **Check for Changes**:
   - Compare the current inventory against the most recent backup zip in Google Drive (`skills_backup_YYYYMMDD.zip` or `all_installed_skills_backup_YYYYMMDD.zip`).
   - Identify newly created skills, modified instructions, or deleted skills.

3. **Package Skills Archive**:
   - Generate individual `SKILL.md` files for each skill under their respective kebab-case directory (`skills/<skill-name>/SKILL.md`).
   - Bundle into a clean zip archive using standardized naming:
     - Full archive: `all_installed_skills_backup_<YYYYMMDD>.zip`
     - Changed delta: `new_and_changed_skills_backup_<YYYYMMDD>.zip`

4. **Upload to Google Drive**:
   - Upload the resulting zip file to `Active_Skills_Bundle` or `All_Installed_Skills_Backup`.
   - Verify upload integrity and report a summary table of backed-up skills with Drive links.

## Gotchas

- **System Skill Isolation**: Never export or expose internal `system:` skills. Only package `user:` namespace skills.
- **Single-Tier Wrapper**: Ensure the zip archive contains clean skill folders directly at the root without redundant nested wrapper directories.
- **Deduplication**: Do not upload a new backup if no skills have changed since the previous backup date.
