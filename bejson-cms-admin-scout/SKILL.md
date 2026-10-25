---
name: bejson-cms-admin-scout
description: >-
  Recursively scan the user's /storage/emulated/0/Admin directory across repos,
  libraries (104 and 105), skills, templates, and specs to discover active development
  artifacts and suggest structured blog post subject matter ideas. Enables numerical
  topic selection and interactive tuning of the 5-part plan prompt and configuration
  in BEJSON 104a, generating turnkey builder prompts and context paths for direct handoff
  to bejson-cms-blog-writer. Use when brainstorming topics from real Admin codebases
  or configuring blog drafting pipelines.
---

# bejson-cms-admin-scout (Layer 5 Discovery & Plan Configuration)

## Summary

`bejson-cms-admin-scout` is the recursive discovery and plan-prompt tuning skill for Elton Boehnen's BEJSON CMS ecosystem. It recursively audits `/storage/emulated/0/Admin` (`Dev/Repos`, `Libraries/libraries_104`, `Libraries/libraries_105`, `Dev/Skills`, `Dev/Templates`, `Dev/Policy`, `Core/Projects_Archive`, and `Resources`) to identify real, active codebases, tooling engines, and architectural specifications.

It categorizes these systems into structured, sequentially numbered (1..N) blog post topic proposals, allows selecting and tuning the plan parameters in a canonical **BEJSON 104a configuration file** (`config/plan_config.104a.bejson`), and outputs the finalized builder prompt that drives the 5-part pipeline in [`bejson-cms-blog-writer`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/SKILL.md).

---

## When to Use

- Recursively scanning `/storage/emulated/0/Admin` to discover active projects and technical subject matter.
- Generating a sequentially numbered catalog of blog post ideas grounded in real codebases.
- Selecting a topic and tuning the plan prompt parameters (target minimum lines per section, category, author, hero nodes).
- Writing and preserving plan tuning records in standardized BEJSON 104a (`config/plan_config.104a.bejson`).
- Automatically generating the turnkey execution commands to launch the 5-part drafting workflow.

## When NOT to Use

- Do NOT use for general ungrounded brainstorming without scanning the Admin filesystem (use [`ideation-feature-composer`](file:///data/data/com.termux/files/home/.gemini/config/skills/ideation-feature-composer/SKILL.md)).
- Do NOT use for conducting deep single-repo AST forensic research (use [`cms_context_researcher.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/scripts/cms_context_researcher.py)).
- Do NOT use for drafting the actual blog post content sections (use [`bejson-cms-blog-writer`](file:///data/data/com.termux/files/home/.gemini/config/skills/bejson-cms-blog-writer/SKILL.md)).

---

## 1. Architectural Guardrails & BEJSON 104a Configuration

- **Assigned Skill Tier**: Layer 5 (`L5`) Discovery & Plan Configuration
- **Codebase Layer Mapping**: `L3_Use_Cases_Cross_Layer_Blueprinting`
- **Configuration Format**: BEJSON 104a with canonical Fields: `setting_name`, `setting_value`, `description`.
- **Author Crediting**: Elton Boehnen per Policy §9.2 (`boehnenelton2024`).
- **Minimum Line Discipline**: Defaults to $\ge 120$ lines per section ($\ge 480$ total lines) per user mandate.

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

options:
  --scan-root SCAN_ROOT         Root path to scan (default: /storage/emulated/0/Admin)
  --max-depth MAX_DEPTH         Maximum directory recursion depth (default: 4)
  --topics-output TOPICS_OUTPUT File path to save topics catalog (default: suggested_topics.md)
  --select-topic SELECT_TOPIC   Numerical index (1..N) of topic to select and tune
  --tune-config TUNE_CONFIG     Destination path for BEJSON 104a config file
  --min-lines MIN_LINES         Target minimum lines per section (default: 120)
  --generate-plan-prompt        Output finalized builder prompt for bejson-cms-blog-writer
  --version                     Show version identifier and exit
  --register                    Register utility with central database
  --config                      Display operational configuration parameters
  --reset                       Verify execution environment state
```

### Standard Workflow

```bash
# 1. Scan Admin directory and produce topic catalog
python3 ~/.gemini/config/skills/bejson-cms-admin-scout/scripts/admin_topic_scout.py \
  --scan-root "/storage/emulated/0/Admin" \
  --topics-output "suggested_topics.md"

# 2. Select chosen topic index and tune the 5-part plan configuration
python3 ~/.gemini/config/skills/bejson-cms-admin-scout/scripts/admin_topic_scout.py \
  --select-topic 1 \
  --min-lines 120 \
  --tune-config "config/plan_config.104a.bejson" \
  --generate-plan-prompt
```

---

## 3. Deterministic Exit Codes

| Exit Code | Semantic Meaning | Recovery Action |
|:---:|---|---|
| `0` | **Success** &mdash; Admin scanned, topics cataloged, or plan config tuned. | Proceed to select topic or run builder prompt. |
| `10` | **Path Failure** &mdash; Scan root directory or config output folder not found. | Verify specified Admin directory path. |
| `20` | **Environment Failure** &mdash; Python < 3.10 or missing dependencies. | Ensure execution under Python 3.10+. |
| `30` | **Validation Failure** &mdash; Selected topic index out of bounds. | Check available topic numbers in catalog. |
