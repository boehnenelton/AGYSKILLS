---
name: book-writer
description: >-
  Emulate Elton Boehnen's Cli_Bookwriter multi-turn chained-context book generation engine with an embedded SEO-ready publication HTML template. Guides the user through a disciplined chapter-by-chapter book writing workflow: Turn 1 creates the comprehensive multi-chapter plan outline from attached context; subsequent turns write exactly one chapter per turn maintaining plan scope and preceding chapter continuity; the final turn compiles all chapters into a standalone, SEO-optimized HTML publication using the embedded template. Use when writing long-form books, technical guides, manuals, or comprehensive documentation requiring multi-turn chapter execution and HTML compilation. Do NOT use for single-turn summary articles (use publication-html-builder), general task job tracking (use job-workflow-manager), or pre-planning database schemas (use planning-schema-planner).
---
# Book Writer

Emulates Elton Boehnen's `Cli_Bookwriter` architecture to execute state-persistent, multi-turn, chapter-by-chapter book writing, culminating in an SEO-optimized, publication-ready standalone HTML document.

## Summary

Standard single-turn LLM generation degrades beyond 2,000 words by rushing, compressing technical depth, or hallucinating summaries. `book-writer` enforces the proven AuthorCMS / `Cli_Bookwriter` chained-context workflow. In Turn 1, the AI ingests attached context and constructs a structured chapter plan. In each subsequent turn, the AI writes exactly ONE chapter at a time, injecting the full book plan outline for global situational awareness and the complete text of Chapter N-1 for seamless narrative and stylistic continuity. In the final turn, it injects all chapters into the embedded SEO-optimized HTML template (`assets/book_template.html`), outputting a fully styled, indexed, and accessible single-file book.

## When to Use

- Writing complete multi-chapter books, technical guides, reference manuals, or deep investigative documentation.

- The user attaches reference notes, research documents, or topic context and requests a comprehensive book written step by step.

- A writing project requires multi-turn execution where each chapter is generated, reviewed, and persisted individually.

- Compiling the final output into a standalone HTML file equipped with SEO metadata, Open Graph cards, Twitter cards, and Schema.org JSON-LD microdata.

- Emulating `Cli_Bookwriter` workflows, AuthorCMS chained-context generation, or persistent author personas.

## When NOT to Use

- Single-turn editorial articles, standalone essays, or quick formatting into publication HTML without chapter-by-chapter generation (use `publication-html-builder`).

- General task orchestration or headless command-line job scripts (use `job-workflow-manager` or `agy-prompt-automator`).

- Pre-planning database schemas or entity models (use `planning-schema`).

- High-level speculative macro concept generation without structured chapters (use `ideation-macro-composer`).

## The Chained-Context Book Writing Protocol

The core architecture emulates `Cli_Bookwriter` using three persistent context inputs for every chapter pass:

1. **Attached Context Bubble**:
   The user's reference notes, background facts, source code, or documentation files. Kept active across all chapters.

2. **Full Book Plan Scope**:
   The complete structural outline (Chapters 1 through M with titles and specific goals). Injected into every chapter pass so the model understands where the current chapter fits and avoids prematurely covering future chapters.

3. **Preceding Chapter Continuity Buffer**:
   The complete text of Chapter N-1 is injected into the prompt for Chapter N. This guarantees stylistic consistency, prevents repeated introductions, and maintains terminological continuity.

## Multi-Turn Operational Lifecycle

### Turn 1: Ingestion, Context Attachment & Plan Generation

1. Acknowledge the project scope and context:
   Inspect all user-provided reference texts, documents, or research notes.

2. Formulate Book Metadata:
   - `Writing_Title`: Official title of the book.
   - `Writing_Type`: Non-fiction guide, technical manual, reference, or narrative.
   - `Writing_Category`: Technology, engineering, architecture, etc.
   - `Book_Goal`: Detailed thesis and target educational outcome.
   - `Section_Count`: Number of planned chapters (typically 5 to 10 chapters).

3. Construct Chapter Plan Tasks:
   For each chapter, define:
   - `Task_ID`: Sequential task token (`TASK1`, `TASK2`, ...).
   - `Task_Name`: Exact chapter title (e.g., `Chapter 1: Foundational Architecture`).
   - `Task_Goal`: Explicit chapter scope, key technical sections, and boundaries.

4. Turn 1 Gate & Handoff:
   Present the full book plan and chapter outline to the user.
   Explicitly halt without writing Chapter 1. Ask for confirmation or outline adjustments before starting the first chapter in Turn 2.

### Turns 2 through M+1: Sequential Chapter Writing (One Task at a Time)

Each turn executes exactly ONE chapter:

1. Setup Context Window for Chapter N:
   - Identify active chapter assignment: `Chapter N: [Title]`.
   - Mount attached reference context.
   - Mount full book plan outline for global scope.
   - Mount full text of Chapter N-1 (if N > 1) as the continuity buffer.

2. Core Chapter Writing Invariants:
   - **Strict Chapter Isolation**: Write exclusively the content for Chapter N. Never start writing Chapter N+1 early.
   - **No Duplicate Headings**: Never repeat the chapter title as a secondary heading inside the chapter body.
   - **Technical Depth & Wrapping**: Write complete, thorough prose. Format code blocks with language tags, create Markdown tables for matrix data, and avoid superficial placeholders.
   - **Brand & Terminology Sanitization**: Ensure BEJSON expands to "Boehnen Elton JSON", avoid corporate fluff or marketing adjectives ("seamless", "revolutionary"), and maintain matter-of-fact technical precision.

3. State Tracking and Handoff:
   - Present Chapter N in full.
   - State progress clearly: `Chapter N of M Completed`.
   - Preview Chapter N+1 title and goal.
   - Prompt the user to confirm to proceed to Chapter N+1.

### Final Turn (Turn M+2): Compilation to Standalone SEO HTML

Once all M chapters are written, the final turn generates the completed publication HTML file using the embedded template (`assets/book_template.html`):

1. **Populate SEO & Social Metadata**:
   - `PAGE_TITLE`, `META_DESCRIPTION`, `META_KEYWORDS`, `CANONICAL_URL`.
   - Open Graph tags (`og:title`, `og:description`, `og:type` = `book`).
   - Twitter Cards (`twitter:card` = `summary_large_image`, `twitter:title`, `twitter:description`).
   - Generate Schema.org JSON-LD microdata for `Book` with all chapter nodes in `hasPart`.

2. **Generate Table of Contents (TOC)**:
   - Build `<ol>` list with anchor links to `#chapter-1` through `#chapter-M`.

3. **Format Chapters into Articles**:
   - Each chapter wrapped in `<article id="chapter-N" role="article" aria-labelledby="chapter-N-title">`.
   - Wrap code blocks in `.bw-code-wrap` (or `.bw-schema-box` for BEJSON/schemas).
   - Wrap tables in `.bw-table-wrap`.

4. **Output and Deliver**:
   - Write the compiled HTML file to disk or export it to Google Drive.
   - Report publication metrics: total words, chapter count, and download links.

## Author Persona Integration

`book-writer` can optionally adopt persistent author personas while maintaining core book-writing rules:

- **Documentation Specialist ("PR Agent")**: Matter-of-fact, precise, direct, honest about limitations, zero corporate-speak or marketing fluff.

- **Scannable Technical Writer ("README Writer")**: Direct, concise, structured, lead with working code examples, state limitations clearly.

- **Deep Technical Rebel ("Leethaxor69")**: Informal, highly technical, exhaustive, 100% fact-based deep-dive explanations.

- **Default Core Voice**: Structured, neutral, professional, authoritative technical prose.

Rule: The core book-writing instructions (single chapter scope, outline fidelity, chained continuity) always take strict precedence over any selected persona.

## Step-by-Step Execution Workflow

Follow this sequence when executing the skill:

### Step 1: Initialize Book Session

Examine user prompt and attached context. Declare Turn 1:
```markdown
### [Book Writer: Turn 1 of Plan & Setup]

**Title**: [Proposed Title]
**Goal**: [Target Objective]
**Planned Chapters**: [M Chapters]
```

### Step 2: Present Structured Outline

Output the full chapter breakdown with explicit task goals for each chapter. Conclude Turn 1 inviting user approval.

### Step 3: Write Single Chapter per Turn

Upon confirmation, write Chapter 1. In subsequent turns, write Chapter 2 through Chapter M sequentially, always bridging from the previous chapter's text.

### Step 4: Final Compilation to SEO HTML

Upon completing Chapter M, merge all chapters into the embedded template and output the final HTML file.

## Gotchas and Anti-Patterns

- **Writing Ahead**: Never write multiple chapters in a single turn. Generating more than one chapter in a single pass causes context degradation.

- **Double Titles**: Never begin chapter content with `# Chapter Title` if the chapter title is already rendered in the section wrapper.

- **Losing Continuity**: Never generate Chapter N without referencing the exact text and terminology established in Chapter N-1.

- **Missing SEO Tags**: Always populate all meta tags, Open Graph cards, and JSON-LD structured data during final HTML compilation.
