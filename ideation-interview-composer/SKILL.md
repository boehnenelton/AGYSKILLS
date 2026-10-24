---
name: ideation-interview-composer
description: Iteratively interviews the user through predefined baseline questions (document vs codebase, sub-types, subjects) and dynamic follow-up inquiries, researches domain capabilities, presents sequentially numbered feature and interface menus (1..N) for easy numerical selection, and compiles selected items into an all-in-one build instruction prompt. Use when the user asks to plan, spec, or iteratively interview for a project, build a tool or doc with an interactive questionnaire, or generate a tailored builder prompt from numbered feature choices. Do NOT use for standalone 25-50 point feature cataloging without interactive interview Q&A (use ideation-feature-composer) or high-level macro system ideation (use ideation-macro-composer).
---
# Ideation Interview Composer

An interactive interview and specification engine. It guides the user through structured baseline questions, conducts domain research, composes sequentially numbered menus for UI and functional features, and synthesizes selections into an all-in-one prompt ready for an autonomous builder.

## Summary

Where the standard composer produces a single exhaustive catalog, the Ideation Interview Composer conducts an iterative, multi-stage dialogue:

1. Baseline preset interview to establish artifact category and type.
2. Dynamic contextual interview tailored to the answers.
3. Phase 1 Interface and layout composition (for codebases) or structural chapter composition (for documents) with global numerical selection.
4. Phase 2 Feature research and exhaustive numbered feature composition with global numerical selection.
5. Synthesis into a self-contained all-in-one instruction set for builder agents.

## When to Use

Use this skill when:

- The user wants an interactive questionnaire or guided interview to spec out a tool, app, script, or document.
- The user states "interview me for a project", "help me spec an app step-by-step", or "compose features through questions".
- The user wants to select interface elements and application features by entering numbers from a generated menu.
- The user needs an all-in-one instruction prompt or specification document to feed into an implementation agent or coding assistant.

## Core Workflow

### Step 1: Baseline Preset Interview

Begin with the predefined baseline inquiry. Present the options cleanly and wait for the user response.

```markdown
### Project Initialization

What are we building?

1. Document
   > Document Type:
     a. Book
     b. Guide / Manual
     c. README
     d. Technical Documentation / Architecture Spec
   * What is the subject of your selection?

2. Codebase Project
   > Project Type:
     a. Python
     b. JavaScript / Web Application
     c. Bash / Shell Utility
     d. User-Defined (Custom Language / Stack)
   * What is the core concept and purpose of your project?
```

Rules for Step 1:

- Do not overload the initial turn with extraneous questions.
- If the user has already provided some baseline answers in their opening query (e.g., "I want to build a Python CLI for file syncing"), acknowledge what was provided, lock those selections in, and only ask the remaining baseline questions.

### Step 2: Branch Execution

#### Branch A: Codebase Projects

When the user selects a Codebase Project, execute two distinct composition phases:

##### Phase 1: Interface and Layout Composition

1. Ask targeted dynamic questions regarding the visual and physical interface:
   - Form factor: CLI / Terminal, Desktop Web, Mobile Web, or Hybrid.
   - Layout components: Sidebar, header / horizontal toolbar, mobile hamburger menu, accordion panels, footer, tabs.
   - Visual constraints: Color scheme (e.g., strict palettes), typography, light/dark themes, density.

2. Present a sequentially numbered Interface & Layout Menu (items 1 through M).
   - Format: `[Number]. **Component Name**: Concrete layout behavior and styling.`
   - Ensure continuous numbering across all interface categories.

3. Instruct the user: "Reply with the numbers or ranges of the layout and interface components you want to include (e.g., '1, 3, 5-8')."

4. Once the user replies with their numbers, acknowledge and lock in the interface choices.

##### Phase 2: Feature Research and Exhaustive Feature Composition

1. Research domain standards and real-world tools matching the user concept and technology stack.

2. Generate an exhaustive, sequentially numbered Feature Menu (items M+1 through N, or freshly numbered 1 through N).
   - Aim for 30 to 60+ concrete, implementable capabilities covering core logic, data handling, validation, error handling, automation, shortcuts, and exports.
   - Format: `[Number]. **Feature Name**: Clear functional description.`
   - Maintain continuous numbering across all categories.

3. Instruct the user: "Reply with the numbers or ranges of the features you want to build (e.g., '2, 5, 12-18, 32')."

4. Map the user's selected numbers back to the specific feature titles and descriptions.

#### Branch B: Documents

When the user selects a Document, execute structural and content composition:

##### Phase 1: Structural Outline Composition

1. Ask targeted dynamic questions regarding target audience, depth, tone, and delivery format (Markdown, PDF, HTML).

2. Present a sequentially numbered Structural Blueprint Menu (items 1 through M) detailing potential sections, chapters, executive summaries, and appendices.

3. Have the user select structural modules by number.

##### Phase 2: Content Modules and Topical Features

1. Research topic depth and key subject matter areas.

2. Present an exhaustive, sequentially numbered Content & Topics Menu (items 1 through N) covering specific technical topics, diagrams, walkthroughs, reference tables, and exercises.

3. Have the user select desired modules by number.

### Step 3: Synthesis and All-in-One Instruction Set Generation

After the user selects their numbered items from both phases:

1. Validate selections: Map all selected numbers to their exact titles and functional specifications.

2. Resolve conflicts: If any selected features or layout items conflict, resolve them cleanly with a single clarifying sentence.

3. Produce the All-in-One Build Prompt: Assemble a comprehensive, self-contained markdown specification block enclosed in a code block. The instruction set must include:
   - Project Identity and High-Level Architecture.
   - Technology Stack and Environment Constraints.
   - Interface and Layout Blueprint (explicitly detailing selected UI components).
   - Feature Implementation Manifest (itemizing every selected feature by name with full behavioral specs).
   - Data Structures and Persistence Model.
   - File Organization and Directory Hierarchy.
   - Step-by-Step Implementation and Verification Protocol.

Close by instructing the user that the generated prompt is ready to be provided directly to their builder LLM or execution agent.

## Formatting Rules

- Numbering format: Always use continuous sequential numbers (`1.`, `2.`, `3.`) across all categories. Never restart numbering at 1 within a subcategory.
- No checkboxes: Use pure numbers so the user can easily reply with lists or ranges like "1, 4, 7-12, 25".
- Clean markdown: Ensure a blank line precedes every list and code block.
- Punctuation constraint: Do not use em-dashes or en-dashes; use hyphens, double hyphens, or periods.

## Gotchas

- Do not jump straight to building code or generating full document text during the interview; the objective of this skill is structured scoping, feature selection, and builder prompt synthesis.
- Do not skip Phase 1 interface composition for visual or web codebase projects; UI structure determines data flow and state architecture.
- Keep the baseline questions focused on the predefined choices before branching into dynamic questions.
