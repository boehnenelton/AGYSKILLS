# Specification: The Literal Placeholder Rule & Zero-Filler Skeleton Law

> **Parent Skill:** `template-literal-skeleton` (Layer 4)  
> **Policy Enforcement:** Policy §12 (GEMINI.md)  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Effective Date:** October 2026

---

## 1. Principles & Rationale

When creating templates or scaffolds, developers and agents frequently inject arbitrary filler content:
- Pseudo-Latin `Lorem ipsum` blocks.
- Fictional blog articles, marketing jargon, or placeholder stories.
- Conversational comments explaining obvious HTML tags.

This practice introduces "template clutter", increases mental friction, obscures layout architecture, and requires downstream cleanup.

The **Zero-Filler Skeleton Law** eradicates this practice completely. A template must be a **pure structural skeleton**, with elements identified only by the literal name of the slot.

---

## 2. Literal Label Standard Map

| Structural Component | Literal Label Standard | Forbidden Patterns |
| :--- | :--- | :--- |
| **Document / Page Title** | `Title` | `"My Awesome Blog"`, `"Dashboard v1"`, `"Welcome"` |
| **Section Headings** | `Section Heading 1`, `Section Heading 2` | `"About Us"`, `"Latest News"`, `"Why Choose Us"` |
| **Main Content Container** | `Content Body` | `Lorem ipsum...`, fabricated paragraphs |
| **Sub-paragraph** | `Content Body` or `Content Snippet` | Fictional story copy |
| **Table Column Headers** | `Column 1`, `Column 2`, `Column 3` | `"Product"`, `"Price"`, `"User"` (unless explicitly specified) |
| **Table Data Cells** | `Cell 1-1`, `Cell 1-2`, `Cell 2-1` | Mock financial numbers, dummy addresses |
| **Terminal Menu Header** | `Menu Header` | `"=== ELTON'S TOOLBOX ==="` |
| **Terminal Menu Items** | `1. Menu Item 1`, `2. Menu Item 2` | `"1. Fix My Wi-Fi"`, `"2. Check Weather"` |
| **Terminal Prompt** | `Select an option [1-N]: ` | Multi-paragraph instructions |
| **Card / Box Title** | `Card Title 1`, `Card Title 2` | `"Breaking News!"`, `"Special Feature"` |
| **Card / Box Content** | `Card Content Body 1` | Sample sales pitches |
| **Buttons / Actions** | `Action 1`, `Action 2`, `Submit`, `Cancel` | `"Click here to learn more!"` |
| **Metadata Dates** | `Date Placeholder` | Hardcoded mock dates |
| **Metadata Authors** | `Author Placeholder` | Fictional persona names |
| **Status Indicators** | `Status Placeholder` | Random states |

---

## 3. Strict Prohibitions

1. **NO Lorem Ipsum**: Any presence of `lorem`, `ipsum`, `dolor`, `sit`, `amet`, or `consectetur` causes immediate test rejection.
2. **NO Conversational Fluff**: No `<!-- Here is where you put your text -->` or conversational preamble.
3. **NO Fabricated Scenarios**: Do not invent products, stories, or news articles inside templates.
4. **Architectural Purity**: Only the exact requested architecture, styled with literal labels.
