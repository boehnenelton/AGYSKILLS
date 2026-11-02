---
name: skill-backup-manager
description: >-
  Audit, package, and back up user-created skills to dedicated Google Drive skill
  ecosystem directories whenever skills are added, modified, or on a scheduled cadence.
  Enforces clean single-tier ZIP packaging, version tracking, and synchronization across
  active and cloud backup targets. Use when the user asks to back up skills, archive
  skills, export skills to Drive, sync modified skills to the skill backup directory,
  or verify skill backup integrity. Do NOT use for general project release packaging
  (use project-delivery-packager), session initialization download sweeps (use
  file-archive-coordinator), or authoring new skill bundles (use skill-architect).
---

# skill-backup-manager (Layer 3 Services & Adapters)

## Summary

`skill-backup-manager` is the canonical Layer 3 backup coordinator for the Antigravity agent skill ecosystem. It automates the auditing, packaging, and mirroring of all installed agent skills (`~/.gemini/config/skills/`) to Elton Boehnen's dedicated external Google Drive and local consolidated backup stores (`/storage/emulated/0/Documents/AGY/skills/` and `/storage/emulated/0/Admin/Dev/Skills/agy-consolidated/`). All headless `agy` CLI invocations MUST enforce `--sandbox`.

---

## When to Use

- Backing up user-created skills to Google Drive or local redundant storage targets.
- Checking for newly added or modified skills compared to existing backup archives.
- Exporting clean single-tier ZIP archives of active skills into designated delivery folders.
- Running scheduled or automated backup sweeps across the active skill repository.
- Verifying the file integrity and completeness of mirrored skill directories.

## When NOT to Use

- Packaging general application codebases or production releases (use `project-delivery-packager`).
- Sweeping session downloads or archiving downloaded project drops (use `file-archive-coordinator`).
- Authoring, scaffolding, or linting individual skill bundles (use `skill-architect`).
- Indexing skill routing topologies or checking trigger collisions (use `skill-ecosystem-cartographer`).

---

## 1. Backup Targets & Directory Hierarchy

`skill-backup-manager` synchronizes the active skill store across two canonical backup sinks:

1. **Primary Document Mirror**:
   `/storage/emulated/0/Documents/AGY/skills/`
2. **Consolidated Development Archive**:
   `/storage/emulated/0/Admin/Dev/Skills/agy-consolidated/`

---

## 2. Backup Execution Procedure

```bash
# 1. Audit active skills directory for modifications
ls -la /data/data/com.termux/files/home/.gemini/config/skills/

# 2. Synchronize to Primary Mirror
rsync -av --delete \
  /data/data/com.termux/files/home/.gemini/config/skills/ \
  /storage/emulated/0/Documents/AGY/skills/

# 3. Synchronize to Consolidated Dev Archive
if [ -d "/storage/emulated/0/Admin/Dev/Skills/agy-consolidated" ]; then
  rsync -av \
    /data/data/com.termux/files/home/.gemini/config/skills/ \
    /storage/emulated/0/Admin/Dev/Skills/agy-consolidated/
fi
```
