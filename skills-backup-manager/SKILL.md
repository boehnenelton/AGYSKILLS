---
name: skills-backup-manager
description: >-
  Audit, package, and back up user-created skills to the dedicated Google Drive
  skill ecosystem folders whenever skills are added, modified, or on a scheduled
  cadence. Use when the user asks to back up skills, archive skills, export skills
  to Drive, sync modified skills to the skill backup directory, or verify skill
  backup integrity. Do NOT use for general project release packaging (use
  project-delivery-packager) or session initialization download sweeps (use
  file-archive-coordinator).
---
# skills-backup-manager

Audits, bundles, and archives user-created skills to Elton Boehnen's Google Drive skill ecosystem directories whenever skills are updated or changed.

## When to Use

- Back up user-created skills to Google Drive.
- Check for newly added or modified skills compared to existing backup archives.
- Export clean single-tier zip archives of active skills to designated backup folders.
- Scheduled or automated backup sweeps of the skills repository.
