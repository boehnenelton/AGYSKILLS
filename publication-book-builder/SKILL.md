---
name: publication-book-builder
description: >-
  Author, structure, gate, and compile long-form books, technical manuals,
  structural reports, and multi-chapter publications using the BEJSON Book
  Standard (BKS-1 kit v1.1.5). Unifies BEJSON 104db Book Documents, nine
  canonical BookType templates, in-process declarative quality gates, multi-turn
  chained-context generation, and multi-format exports (HTML with BECSS styling,
  Markdown, plaintext, JSON, BEJSON, ZIP). Replaces legacy Bookmaker with the
  BKS-1 standard. Use when writing multi-chapter technical books, generating
  publications from BookTypes, executing chapter quality gates, or compiling
  standalone HTML manuals. Do NOT use for single-document editorial publication
  HTML formatting without chapters (use publication-html-builder), 4-part
  technical blog drafting (use publication-blog-post-writer), general task job
  execution (use job-workflow-manager), or pre-planning database schemas
  (use planning-schema-planner).
---

# Skill: `publication-book-builder` (Layer 5 BKS-1 Book Author & Compiler)

- **Version**: `115`
- **Release_Version**: `300`
- **Architectural Layer**: `Layer 5 (System Architecture & Long-Form Composition)`
- **Format Standard**: `BKS-1 (BEJSON Book Standard, kit v1.1.5 / PKG115)`
- **Storage Substrate**: `BEJSON 104db ("Book", "Chapter", "Generation", "Export")`
- **Embedded Tool**: [`scripts/bks_tool.py`](./scripts/bks_tool.py)
- **Reference Guide**: [`references/bks1_architecture_guide.md`](./references/bks1_architecture_guide.md)
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Summary & Architectural Scope

`publication-book-builder` is the canonical Layer 5 skill for authoring, structuring, gating, and rendering long-form books and technical publications adhering strictly to the **BEJSON Book Standard (BKS-1)**. It supersedes legacy `book-writer` ("bookmaking") paradigms by grounding all book data in a single, authoritative BEJSON 104db Book Document (`books/<slug>.bks.bejson`).

Every book is governed by:
1. **The Single Source of Truth**: One BEJSON 104db document holding Book, Chapter, Generation, and Export rows.
2. **The Nine Canonical BookTypes**: Pre-seeded structural blueprints defining chapter counts, outline nodes, and gate profiles.
3. **Four Conformance Levels (C1-C4)**: Structural validity (C1), outline integrity (C2), content gates (C3), and export parity (C4).
4. **Declarative In-Process Gates**: Strict word count floors, required section headers, and forbidden pattern checks executed without shell commands.
5. **Multi-Format Compilation**: Deterministic export rendering to BECSS-styled HTML, clean Markdown, plaintext, JSON, or ZIP archives.

---

## 2. When to Use

- Writing complete multi-chapter technical books, structural reports, engineering manuals, or fiction manuscripts.
- Initializing fresh book documents from canonical BookType blueprints (`technical_manual`, `structural_report`, `code_analysis`, etc.).
- Enforcing in-process chapter quality gates (`bks_gates`) before accepting model generations.
- Projecting JobMaker `JobTask` execution plans from Book Documents for headless runner automation.
- Exporting fully compiled publications to self-contained, accessible HTML documents with Tri-Color styling (`#000000`, `#FFFFFF`, `#DE2626`).

---

## 3. The Nine Canonical BookTypes

Built-in BookTypes reside in [`book_types/`](./book_types/) as standalone BEJSON 104 data documents (`.bks-type.bejson`):

| BookType Slug | Default Chapters | Gate Profile | Best For |
| :--- | :---: | :--- | :--- |
| **`technical_manual`** | 10 | Strict (1,200 min words, required sections) | Software manuals, library guides, protocol specs |
| **`structural_report`** | 8 | Strict (1,000 min words) | Architectural analyses, security audits, gap reports |
| **`code_analysis`** | 6 | Code-first (800 min words, syntax blocks) | Deep AST inspections, refactoring walkthroughs |
| **`readme`** | 5 | Fast (300 min words) | Multi-part repository documentation portals |
| **`standard_book`** | 12 | Standard (1,500 min words) | Comprehensive non-fiction works and reference texts |
| **`fiction_novel`** | 20 | Narrative (2,000 min words) | Character-driven fiction and creative writing |
| **`poetry_collection`** | 15 | Stanza (150 min words) | Structured verse and anthologies |
| **`biography`** | 10 | Historical (1,200 min words) | Chronological retrospectives and technical biographies |
| **`general_document`** | 4 | Flexible (500 min words) | Turnkey multi-section documents and proposals |

---

## 4. Operational Workflow & CLI Reference

All BKS-1 operations can be conducted via the embedded [`scripts/bks_tool.py`](./scripts/bks_tool.py) utility:

### Step 1: Initialize Book Document
```bash
python3 scripts/bks_tool.py \
  --create \
  --type "technical_manual" \
  --title "Architecting Multi-MFDB Systems" \
  --topic "Multi-File Database Topologies" \
  --author "Elton Boehnen" \
  --out "books/multi_mfdb_guide.bks.bejson"
```

### Step 2: Validate Conformance (C1-C4)
```bash
python3 scripts/bks_tool.py \
  --book "books/multi_mfdb_guide.bks.bejson" \
  --validate \
  --level 3
```

### Step 3: Project JobMaker Execution Plan
```bash
python3 scripts/bks_tool.py \
  --book "books/multi_mfdb_guide.bks.bejson" \
  --plan \
  --out "jobs/multi_mfdb_guide.bejson"
```

### Step 4: Export Publication
```bash
python3 scripts/bks_tool.py \
  --book "books/multi_mfdb_guide.bks.bejson" \
  --export html \
  --theme "becss" \
  --out "exports/multi_mfdb_guide"
```

---

## 5. Execution & Subagent Containment Contract (Level 3 Guardrail)

When invoking subagents or automated writers from `publication-book-builder`, always enforce `--sandbox` containment and deterministic exit codes (`0` = OK, `10` = Path Failure, `20` = Env Failure, `30` = Schema/Validation Failure):

```bash
agy --sandbox -p "Write Chapter 1 for books/my_book.bks.bejson using publication-book-builder."
```

---

## When NOT to Use

Do NOT use `publication-book-builder` for out-of-scope tasks. Route immediately to the designated sibling skill:

- **Formatting single standalone publication HTML pages without chapter structures**: Redirect immediately to `publication-html-builder`.
- **Authoring 4-part or 5-part technical blog posts for CMS import**: Redirect immediately to `publication-blog-post-writer`.
- **Executing general JobMaker task workflows outside books**: Redirect immediately to `job-workflow-manager`.
- **Pre-planning backend database entity schemas**: Redirect immediately to `planning-schema-planner`.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
