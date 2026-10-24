# Chained-Context Architecture & Prompt Templates

Reference specifications and prompt structures derived directly from Elton Boehnen's `Cli_Bookwriter` (v1.5.0).

## The Chained-Context Flow Diagram

```
       +-------------------------------------------------------+
       |                 Attached Context Bubble               |
       +-------------------------------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------------+
|                           Chapter Prompt (N)                            |
+-------------------------------------------------------------------------+
| 1. Current Chapter Assignment: Title & Objective                       |
| 2. Complete Book Plan Scope (Outline for situational awareness)         |
| 3. Attached Context Reference Text (Background research)                |
| 4. Chapter (N-1) Full Text Output (Continuity buffer)                   |
+-------------------------------------------------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------------+
|                       Writing Generation Engine                         |
+-------------------------------------------------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------------+
|                       Brand & Text Sanitization                         |
+-------------------------------------------------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------------+
|                   Single Chapter Output & Progress Gate                 |
+-------------------------------------------------------------------------+
```

## Plan Schema Specification (BEJSON 104a)

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Writing_Title": "Title of the Book",
  "Writing_Type": "Non-Fiction Guide",
  "Writing_Category": "Technology",
  "Book_Goal": "Comprehensive introduction to the subject.",
  "Section_Count": 5,
  "Records_Type": ["PlanTask"],
  "Fields": [
    {"name": "Task_ID", "type": "string"},
    {"name": "Task_Name", "type": "string"},
    {"name": "Task_Goal", "type": "string"}
  ],
  "Values": [
    ["TASK1", "Chapter 1: Title", "Goal and scope of chapter 1"],
    ["TASK2", "Chapter 2: Title", "Goal and scope of chapter 2"]
  ]
}
```

## Chapter Prompt Structure

When composing the prompt or internal context for Chapter N:

```text
You are writing a book titled "{book_title}" on the topic of "{topic}".

*** CRITICAL INSTRUCTION ***
Your CURRENT ASSIGNMENT is to ONLY write the content for the single chapter titled: "{chapter_title}".
Do NOT write the entire book. Do NOT write other chapters. Focus exclusively on delivering a complete,
high-quality draft of this one chapter, in Markdown.

--- ATTACHED CONTEXT (reference material) ---
{attached_context}

--- DOCUMENT PLAN SCOPE (for reference ONLY, so you understand the whole book's structure) ---
{plan_scope}

--- PREVIOUS CHAPTER (for continuity ONLY - do not rewrite this) ---
{previous_chapter_content}
```
