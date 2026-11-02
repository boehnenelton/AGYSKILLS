---
name: bejson-cms-admin-scout
description: >-
  Recursively scan the user's /storage/emulated/0/Admin directory across repos,
  libraries (104 and 105), skills, templates, and specs to discover active development
  artifacts and suggest structured blog post subject matter ideas. Enables numerical
  topic selection, extraction of Graphics 105 visual component briefs (4 peripheral nodes
  and telemetry subtitle), and interactive tuning of the 5-part plan prompt and configuration
  in BEJSON 104a, generating turnkey builder prompts and context paths for direct handoff
  to bejson-cms-blog-writer and bejson-cms-canvas-illustrator. Use when brainstorming topics
  from real Admin codebases or configuring blog drafting pipelines. Do NOT use for drafting the
  4-part blog content itself (use bejson-cms-blog-writer), compiling CMS static sites (use
  bejson-cms-publish-automator), or generating SVG banners (use bejson-cms-canvas-illustrator).
---

# bejson-cms-admin-scout (Layer 5 Discovery & Plan Configuration)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & POSIX Linux
- **Architectural Tier**: Layer 5 (L5) Discovery & Plan Configuration
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `9e012f34-5678-4abc-def9-0123456789ab`
- **Version**: `1.3.0`
- **Domain**: Topic Discovery & Visual Briefing (`BEJSON_CMS`)

## Summary

`bejson-cms-admin-scout` is the recursive discovery, plan-prompt tuning, and visual briefing skill for Elton Boehnen's BEJSON CMS ecosystem. It audits `/storage/emulated/0/Admin` (`Dev/Repos`, `Libraries/libraries_104`, `Libraries/libraries_105`, `Dev/Skills`, `Dev/Templates`, `Dev/Policy`, and `Resources`) to identify real, active codebases, tooling engines, and architectural specifications.

It categorizes these systems into structured, sequentially numbered (1..N) blog post topic proposals, extracts **Graphics 105 visual briefing nodes** (4 peripheral subsystem components and telemetry subtitle), tunes plan parameters in a canonical **BEJSON 104a configuration file** (`config/plan_config.104a.bejson`), and outputs turnkey execution commands for both [`bejson-cms-blog-writer`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/SKILL.md) and [`bejson-cms-canvas-illustrator`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-canvas-illustrator/SKILL.md).

---

## When to Use

- Recursively scanning `/storage/emulated/0/Admin` to discover active projects and technical subject matter.
- Generating a sequentially numbered catalog of blog post ideas grounded in real codebases.
- Extracting the 4 peripheral subsystem components and telemetry subtitle needed for the 1280x640 Policy §8.1 Tri-Color hero banner.
- Selecting a topic and tuning the plan prompt parameters (target minimum lines per section, category, author, hero nodes).
- Writing and preserving plan tuning records in standardized BEJSON 104a (`config/plan_config.104a.bejson`).
- Automatically generating the turnkey execution commands to launch the 5-part drafting workflow.

## When NOT to Use

- Do NOT use for general ungrounded brainstorming without scanning the Admin filesystem (use [`ideation-feature-composer`](file:///data/data/com.termux/files/home/.gemini/config/skills/ideation-feature-composer/SKILL.md)).
- Do NOT use for conducting deep single-repo AST forensic research (use `cms_context_researcher.py`).
- Do NOT use for drafting the actual blog post content sections (use [`bejson-cms-blog-writer`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/SKILL.md)).

---

## 1. Architectural Guardrails & BEJSON 104a Configuration

- **Assigned Skill Tier**: Layer 5 (`L5`) Discovery & Plan Configuration
- **Codebase Layer Mapping**: `L3_Use_Cases_Cross_Layer_Blueprinting`
- **Configuration Format**: BEJSON 104a with canonical Fields: `setting_name`, `setting_value`, `description`.
- **Author Crediting**: Elton Boehnen per Policy §9.2 (`boehnenelton2024`).
- **Minimum Line Discipline**: Defaults to $\ge 120$ lines per section ($\ge 480$ total lines).
- **Visual Briefing Discipline**: Must formulate 4 specific peripheral component cards and 1 telemetry subtitle for seamless handoff to `cms_canvas_illustrator.py`.

---

## 2. CLI Tooling & Execution

The skill is powered by [`scripts/admin_topic_scout.py`](./scripts/admin_topic_scout.py).

### Command-Line Arguments

```text
usage: admin_topic_scout.py [-h] [--scan-root SCAN_ROOT] [--max-depth MAX_DEPTH]
                            [--topics-output TOPICS_OUTPUT]
                            [--select-topic SELECT_TOPIC]
                            [--tune-config TUNE_CONFIG] [--min-lines MIN_LINES]
                            [--generate-plan-prompt] [--version] [--register]
                            [--config] [--reset]
```

### Standard Workflow

```bash
# 1. Scan Admin directory and produce topic catalog with visual briefs
python3 ~/.gemini/config/skills/bejson-cms-admin-scout/scripts/admin_topic_scout.py \
  --scan-root "/storage/emulated/0/Admin" \
  --topics-output "suggested_topics.md"

# 2. Select chosen topic index, tune plan configuration, and emit turnkey CLI commands
python3 ~/.gemini/config/skills/bejson-cms-admin-scout/scripts/admin_topic_scout.py \
  --select-topic 1 \
  --min-lines 120 \
  --tune-config "config/plan_config.104a.bejson" \
  --generate-plan-prompt
```
