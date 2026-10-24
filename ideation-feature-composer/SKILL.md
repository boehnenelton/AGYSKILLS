---
name: ideation-feature-composer
description: >-
  Formulate 25-50 point sequentially numbered feature catalogs. Use when brainstorming product feature menus, authoring comprehensive CLI command trees, or structuring feature roadmaps. Do NOT use for interactive interview Q&A (use ideation-interview-composer).
  Given a vague concept or description of a tool, app, or script, generates an exhaustive numbered list of every possible feature, UI option, and configuration. Output a categorized, sequentially numbered 25-50 point feature menu for user selection. Trigger on feature brainstorm, plan a tool, compose features for, what features could X have. Do NOT use for high-level macro concept expansion (use ideation-macro-composer).
---
# Composer

The inverse of a decomposition recipe. Where a decomposer takes an existing artifact and breaks it down, the Composer takes a vague concept and explodes it outward into an exhaustive catalog of every possible feature, option, behavior, and configuration setting.

## Summary

Generates an exhaustive, sequentially numbered feature catalog for any tool, application, or script concept. Instead of checkboxes, every feature is assigned a unique sequential number so the user can easily select features by listing numbers or number ranges (e.g., "1, 5, 12, 20-35, 88") for planning and building.

## When to Use

Use this skill whenever the user wants to brainstorm, spec out, explore, or plan features for a concept before building:

- User asks "What features could [X] have?" or "Give me a feature list for [X]".
- User states "I want to build a [tool/app/script]" or "Plan a [tool/app/script]".
- User provides a vague or one-line tool idea (e.g., "a clipboard manager", "a csv cleaner", "a markdown editor").
- User asks for a feature brainstorm or wants a complete feature menu to select from using numbers.

## Core Workflow

### Step 1: Interpret the Concept

Extract the core tool archetype from the user input, even if brief:

- "file indexer" -> tool that scans, hashes, watches, and catalogs files
- "something for notes" -> note-taking, organization, and search app
- "manage my tasks" -> task manager, kanban, or project tracker
- "watch logs" -> log viewer, parser, stream filter, and tail utility

If the concept is completely indiscernible (e.g., "make a thing for stuff"), ask one concise clarifying question: "What is the primary function of this tool?" Otherwise, proceed immediately without asking preliminary questions.

### Step 2: Research and Enumerate

Exhaustively explore every functional and architectural dimension of the tool type. Consider real-world state-of-the-art tools and cover all key surface areas:

- Core functionality (primary workflows, processing logic, operations)
- Input and data sources (file systems, streams, APIs, user input, imports)
- Output and export (file formats, reports, data feeds, exports)
- Search, query, and filtering (full-text, regex, fuzzy, criteria filters)
- Display, views, and UI layout (tables, trees, graphs, splits, toolbars)
- Sorting, grouping, and categorization (multi-column, tags, hierarchies)
- Configuration and settings (profiles, config files, flags, defaults)
- Automation, triggers, and scheduling (cron, watchers, hooks, pipelines)
- Integrations and ecosystem (APIs, CLI utilities, third-party connectors)
- Performance and scaling (caching, indexing, threading, memory limits)
- Security, privacy, and permissions (encryption, auth, access controls)
- Logging, metrics, and audit trails (event logs, diagnostics, telemetry)
- Shortcuts and power-user tools (keybindings, command palette, scripting)
- CLI and headless options (arguments, flags, daemon mode, stdout pipes)
- Theming and visual presentation (dark mode, density, font sizing)
- Sync, backup, and state management (snapshots, cloud sync, local state)
- Extensibility and plugins (scripting API, webhooks, custom themes)
- Accessibility, localization, and error recovery (undo/redo, recovery)

### Step 3: Output the Sequentially Numbered Menu

Format the response as a clean, categorized, markdown numbered list adhering to these formatting rules:

1. Maintain a single continuous sequential numbering scheme (1, 2, 3, ... N) across all categories. Do not restart numbering at 1 for each new category. Continuous numbering allows the user to reference any feature globally without specifying category headers.
2. Group items under logical category headers (H2 `##` or H3 `###`).
3. Aim for 100+ items minimum. Complex tools should reach 150 to 200+ distinct items.
4. Each entry must follow the format: `[Number]. **Feature Name**: Concise description of functionality or behavior.`
5. Sub-options or variants should also receive their own distinct numbers or clearly indexed decimal numbers (e.g., `12a`, `12b` or sequential integer numbers) so every option is directly selectable by number.
6. Every item must be a concrete, implementable feature. Avoid vague filler items.
7. Do not truncate, abbreviate, or omit sections.

### Step 4: Close with Selection Instructions

Always end the list with clear instructions explaining how to select features:

```markdown
---
**Reply with the numbers or ranges of the features you want to plan and build (e.g., "1, 4, 12, 18-25, 60, 92-105").**
```

## Output Template

```markdown
# [Tool Name] - Feature Menu
**Concept:** [One-line summary of archetype]
**Total Features Listed:** [N]

Select features by replying with their numbers or ranges (e.g., "1, 5, 12-18, 44").

---

## 1. Core Operations

1. **Quick Scan**: Perform fast initial indexing of designated directory paths.
2. **Deep Content Indexing**: Extract and index raw text within supported document types.
3. **Hash Calculation**: Generate SHA-256 and MD5 checksums for duplicate detection.
4. **File Watcher**: Monitor directories in real time for creation, modification, and deletion.

## 2. Search & Filtering

5. **Filename Wildcard Matching**: Support glob patterns (*.ts, test_??.py) for filename search.
6. **Regular Expression Engine**: Full regex support across filenames and indexed text.
7. **Size Range Filter**: Filter files by minimum and maximum byte/megabyte thresholds.
8. **Date Range Filter**: Filter by creation, modification, or last-accessed timestamps.

...

## [Category N: ...]

[N]. **Feature Name**: Description of capability.

---
**Reply with the numbers or ranges of the features you want to plan and build (e.g., "1, 4, 12, 18-25, 60, 92-105").**
```

## Calibration by Tool Archetype

Use these starter seeds to expand into deep feature menus:

- **File and Directory Tools**: Deep metadata extraction, duplicate finders, batch renamers, directory tree visualizers, diff engines, archive introspection, tag managers, permission auditors.
- **Task and Project Management**: Kanban boards, timeline/Gantt charts, priority matrices, recurrence rules, dependency trees, burndown stats, time tracking, subtask nesting, markdown descriptions.
- **Log and Stream Analyzers**: Real-time tailing, regex highlighting, severity categorization, log aggregation, anomaly detection, JSON/structured log parsing, trace ID correlation.
- **Text and Note Tools**: Markdown editor, bidirectional linking, graph visualization, outline sidebars, distraction-free mode, local-first AES encryption, version history, daily notes.
- **Media and Asset Managers**: Automated thumbnailing, EXIF/ID3 metadata inspector, format transcoding, batch resizing, color palette extraction, waveform view, tag filtering.
- **API and Network Utilities**: Request builder, environment variable vaults, mock servers, assertion runners, curl importer/exporter, SSL cert inspectors, rate limiters.
- **CLI and Automation Runners**: Subprocess execution, cron/interval triggers, piping support, profile switching, history replay, exit code monitoring, alert webhooks.

## Handling Returned Numbers

When the user replies with selected numbers or ranges:

1. Map each selected number back to its exact feature name and description from the menu.
2. Group the selected features into cohesive architectural layers or development milestones.
3. Proceed directly to the requested action (drafting technical specifications, generating system architectures, creating implementation roadmaps, or writing code) without asking redundant confirmation questions.

## Gotchas

- Do not use checkbox lists (`- [ ]`). The primary requirement is numbered entries so users do not need to manually check boxes.
- Do not reset item numbering inside each category. Global continuous numbering (1 through N) ensures unambiguous selection.
- Do not deliver a brief 20-30 item summary. An effective ideation-feature-composer menu provides breadth and exhaustiveness (100+ items) so the user discovers unexpected, high-value capabilities.
- Ensure blank lines precede every list and code block for clean markdown rendering.
