---
name: agy-rules
description: >-
  Author, audit, structure, and enforce directory-scoped and global Antigravity CLI rules (GEMINI.md, AGENTS.md, .agents/rules/*.md). Enforces the 24 KB per-file ceiling, the 20,000-token rules budget ceiling, hierarchical upward directory traversal inheritance, automatic deduplication by resolved filesystem path, and strict negative constraint formulations. Use when crafting project rules, establishing directory boundaries, auditing rule files for token bloat, or debugging rule precedence.
---

# Skill: `agy-rules`

- **Purpose**: Authoring, auditing, and optimizing Antigravity CLI rule files (`GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`).
- **Target Platform**: Antigravity CLI (`agy`) & Antigravity 2.0 Harness
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Rule System Invariants & Budgets

Every rule file created or edited must comply with Antigravity engine limits:

1. **Per-File Size Limit**:
   - Maximum file size: **24 KB** (24,000 bytes).
   - Any file exceeding 24 KB is automatically truncated on line boundaries by the Antigravity engine.
2. **Aggregate Rules Token Ceiling**:
   - Always-on and global rules share a hard **20,000 token** limit (`defaultRulesBudget`).
   - When active rules exceed 20,000 tokens, lower-priority rules are automatically demoted from full inline text to file path pointers (`@[label](path)`), forcing the agent to read them via tool calls instead.
3. **No Frontmatter**:
   - Standalone `GEMINI.md` and `AGENTS.md` files do **not** use YAML frontmatter. They must start directly with markdown headers.
4. **Hierarchical Traversal**:
   - The engine walks up from the active file's directory to the Git root. Deeper rules inherit and extend parent rules.
5. **Path Deduplication**:
   - Rules are deduplicated by resolved canonical path. A file will never be injected twice in a single conversation.

---

## 2. Rule Authoring Standard Template

When scaffolding a new `AGENTS.md` or `GEMINI.md`:

```markdown
# Directory Title / Scope Name

## 1. Scope & Authority
- Applies to all files within this directory and child subdirectories.
- Precedence: Local negative constraints override general defaults.

## 2. Directory Architecture & Pathing
- All local dependencies must reside in `lib/`.
- Relative path preambles must be used; hardcoded absolute paths are prohibited.

## 3. Negative Constraints (Strict Absolutes)
- ❌ NEVER commit unversioned binary artifacts.
- ❌ NEVER use raw print() statements for production logging.
- ❌ NEVER generate filler content or placeholder lorem ipsum.

## 4. Verification & Testing Gate
- Before marking any task complete, execute the local test runner:
  `bash ./tests/run_tests.sh`
```

---

## 3. Auditing Existing Rules

To audit any rule file for size and budget compliance:
```bash
# Check exact byte size (must be <= 24,000 bytes)
wc -c AGENTS.md

# Scan for policy contradiction patterns
grep -iE "never|prohibited|forbidden|mandatory" AGENTS.md
```
