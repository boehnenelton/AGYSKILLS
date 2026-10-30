---
name: ideation-macro-composer
description: >-
  Compose massive, multi-dimensional conceptual frameworks, macro systems, and expansive domain architectures from small, abstract, or vague seed concepts. Use when starting from an abstract vision and needing deep speculative expansion before feature cataloging. Do NOT use for granular numbered feature lists (use ideation-feature-composer) or technical database schemas (use mfdb-python/javascript/typescript-planner).
---
---
name: ideation-feature-composer
description: "Given a vague concept or one-line description of a tool/app/script (e.g. \"file indexer\", \"task manager\", \"log viewer\", \"image resizer\"), generate an exhaustive markdown checkbox list of every possible feature, UI option, and configuration that type of tool could have. Think broadly: research real-world examples, common patterns, power-user features, edge cases, and advanced capabilities. Output a massive, categorized, checkbox-formatted feature menu the user can check off and hand back. Trigger on: \"what features could X have\", \"give me a feature list for\", \"I want to build a [tool]\", \"what should a [app/script] do\", \"feature brainstorm\", \"plan a [tool]\", or any vague tool concept the user wants to spec out before building. Always go wide  -  err on the side of too many features, not too few."

---

# Composer

The **inverse of the Decomposition Recipe Builder**. Where the Deideation-feature-composer takes something that exists and breaks it down, the Composer takes a vague concept and **explodes it outward** into every possible feature it could have.

## Purpose

User gives you: `"a file indexer"` or `"a log viewer"` or `"a task manager"`  
You give them: **the longest possible checkbox list of features, UI options, behaviors, and config settings** that type of tool could ever have.

They check what they want. They hand it back. You build it.

---

## Core Behavior

### Step 1  -  Interpret the Concept

Extract the **tool archetype** from the user's input, even if vague:
- `"file indexer"` → a tool that scans and catalogs files
- `"something for notes"` → a note-taking/management tool
- `"manage my tasks"` → task manager / to-do app
- `"watch logs"` → log viewer / tail tool

If the concept is too vague to even categorize (e.g. "make a thing for stuff"), ask one clarifying question: *"What does this tool primarily do?"*

Otherwise  -  **proceed immediately**. Do not ask unnecessary questions.

### Step 2  -  Research & Enumerate

Think across **all of these axes** for the given tool type:

**Real-world examples:** What do the best-in-class tools of this type do? (e.g. for file indexers: Everything, Recoll, DocFetcher, Windows Search, macOS Spotlight, `locate`, `find`)

**Feature surface areas to always consider:**
- Core functionality (the main job the tool does)
- Input / data sources (what it reads, watches, imports)
- Output / export (what it produces, saves, sends)
- Search & filtering (how users find things)
- Display / UI layout options
- Sorting & ordering
- Grouping & categorization
- Configuration & settings
- Notifications & alerts
- Scheduling & automation
- Integration with other tools
- Performance options
- Security & access control
- Logging & audit trails
- Import / export formats
- Keyboard shortcuts
- CLI interface options
- Theming & appearance
- Help & documentation
- Mobile / responsive behavior
- Multi-user / sharing
- Undo / history
- Backup & restore
- Offline / sync behavior
- Plugin / extension system
- Accessibility

### Step 3  -  Output the Feature Menu

Produce a **categorized markdown checkbox and numeric list entry document**. Rules:
- ✅ Every item is a `- [ ]` checkbox and a # numbered item
- ✅ Group items into logical named categories with `##` or `###` headers
- ✅ Aim for **100+ items minimum**, more is always better
- ✅ Sub-items use indented `  - [ ]` checkboxes for variants/options
- ✅ Include a brief inline description after each item where it adds clarity
- ✅ Do not pad with generic filler  -  every item must be a real, distinct, implementable feature
- ❌ Do not ask the user to confirm the list before producing it  -  just produce it
- ❌ Do not truncate or summarize  -  the value is in the exhaustive length

### Step 4  -  Close with Instructions

End the list with:
```
---
**Check everything you want, then paste this back.**
```

---

## Output Template

```markdown
# [Tool Name]  -  Feature Menu
**Concept:** [One-line description]
**Total options:** [N]

Check everything you want, then paste it back.

---

## [Category 1: Core Functionality]

NUMBER: - [ ] Feature  -  brief description
- [ ] Feature  -  brief description
  - [ ] Sub-option
  - [ ] Sub-option
- [ ] Feature  -  brief description

## [Category 2: ...]

...

---
**Check everything you want, then paste this back.**
I'll scope, plan, and build what you've selected.
```

---

## Calibration by Tool Archetype

These are **starter seeds**  -  always go beyond them.

### File / Directory Tools
Core: scan, index, watch for changes, hash files, detect duplicates, track moves/renames  
Search: full-text, filename, regex, date range, size range, MIME type, extension filter  
Output: JSON/CSV export, tree view, flat list, summary stats, diff reports  
UI: file preview, breadcrumb path, sort columns, group by type/date/size  

### Task / Project Managers
Core: create/edit/delete tasks, subtasks, priorities, due dates, tags/labels  
Views: list, kanban, calendar, timeline/gantt, table  
Filters: by status, assignee, tag, date, project  
Automation: recurring tasks, reminders, dependency blocking  

### Log / Stream Viewers
Core: tail live, load file, parse structured logs (JSON/CSV), highlight patterns  
Filters: severity level, timestamp range, keyword, regex, source  
Display: color coding, line wrapping, column extraction, stats panel  
Export: filtered subset, report generation  

### Text / Note Tools
Core: create/edit/delete notes, markdown support, tags, search  
Organization: folders, notebooks, pinning, archiving  
Sync: local save, cloud backup, version history  
Export: PDF, HTML, plaintext, copy-to-clipboard  

### Media / Asset Tools
Core: scan/catalog media, thumbnail generation, metadata display  
Filters: by resolution, duration, format, codec, date, tags  
Batch ops: rename, convert, resize, tag in bulk  
Preview: inline viewer, slideshow, audio waveform  

### API / Network Tools
Core: send requests, save presets, history, env variables  
Display: response formatting, diff view, headers inspector  
Auth: Basic, Bearer, OAuth, API Key, cookie jar  
Testing: assertions, chained requests, load test, mock server  

### CLI / Script Runners
Core: run scripts, capture output, stdin piping, arg builder  
Scheduling: cron-like triggers, watch-and-run on file change  
History: command log, re-run, favorite/pin commands  
Environment: env var manager, profile switching  

---

## Length Principle

**The feature list should feel intimidating.** The user is using this to discover features they didn't know they wanted. A list of 30 items is a failure. A list of 150 items is the floor. A list of 200+ items for a complex tool is correct.

When in doubt, add more. Add the obvious things. Add the obscure power-user things. Add the "nice to have someday" things. Add the things only enterprise tools have. The user is curating  -  your job is to make the catalog as complete as possible.

---

## After the User Returns the Checked List

When the user pastes back their selections: **build immediately.**

- ❌ No summary of what they picked
- ❌ No conflict or dependency checks
- ❌ No build plan proposal
- ❌ No clarifying questions

The checked list is the spec. Start writing code.



