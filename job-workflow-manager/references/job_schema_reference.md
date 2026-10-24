# JobMaker Schema & Contract Reference Guide

Authoritative specification for Elton Boehnen's JobMaker BEJSON 104a Job Schema, 104db Registry Schema, and Task Context Chunk structures.

## 1. BEJSON 104a Job Schema Specification

Job documents are stored in `jobs/<slug>.bejson` or `templates/<slug>.bejson`.

### Schema Header Structure
```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Schema_Name": "Job Schema",
  "Schema_Version": "1.0",
  "Schema_Description": "Custom job schema for the NewAgent task creation and tracking system, managing individual task states and optional auditing. Each task carries its own task_context (embedded, chunked files), task_reference (path-only refs), and task_mandatory (marks a task as a required, built-in step for the job's Job_Type/Job_Subtype). Job_Type/Job_Subtype classify the job; Contextualize_Plan/Contextualize_Last control what each task is injected with at run time. Also reused unmodified as the Template payload shape.",
  "Job_Goal": "High level description of job objective",
  "Job_Type": "writing",
  "Job_Subtype": "book",
  "Contextualize_Plan": true,
  "Contextualize_Last": true,
  "Job_Complete": false,
  "Creation_Date": "2026-08-25",
  "Completion_Date": "",
  "Records_Type": ["JobTask"],
  "Fields": [
    {"name": "task_id", "type": "string"},
    {"name": "task_order", "type": "integer"},
    {"name": "task_name", "type": "string"},
    {"name": "task_description", "type": "string"},
    {"name": "task_completed", "type": "boolean"},
    {"name": "audit_enabled", "type": "boolean"},
    {"name": "audit_passed", "type": "boolean"},
    {"name": "audit_fail_reason", "type": "string"},
    {"name": "task_context", "type": "array"},
    {"name": "task_reference", "type": "array"},
    {"name": "task_mandatory", "type": "boolean"}
  ],
  "Values": [
    [
      "6e91d4a7-3f28-4c65-b8a0-9d2e1c7f4b56",
      1,
      "Draft Chapter 1 Outline",
      "Produce comprehensive chapter outline based on worldbuilding notes.",
      false,
      true,
      false,
      "",
      [],
      ["/storage/emulated/0/Notes/worldbuilding.md"],
      true
    ]
  ]
}
```

## 2. Task Context Embedded Chunk Format

Each entry in `task_context` contains an embedded file structure chunked Doc_Chunker-style:

```json
{
  "ref": "/storage/emulated/0/docs/guidelines.md",
  "text_based": true,
  "chunks": [
    {
      "chunk_id": "a1b2c3d4",
      "chunk_label": "Chunk_1",
      "chunk_content": "Verbatim paragraph text extracted from source file.",
      "chunk_index_pos": 1,
      "chunk_status": "draft"
    }
  ]
}
```

- If file could not decode as UTF-8, `text_based` is `false` and `chunks` is empty `[]`.
- Read cap is 2 MB (`CONTEXT_MAX_READ_BYTES = 2097152`).

## 3. BEJSON 104db Registry Schema (`registry.bejson`)

Stored at project root: `registry.bejson`.

```json
{
  "Format": "BEJSON",
  "Format_Version": "104db",
  "Format_Creator": "Elton Boehnen",
  "Schema_Name": "Job Registry Schema",
  "Schema_Version": "1.0",
  "Schema_Description": "Tracks every entry saved by JobMaker and classifies it as a Job Schema or a Template, independent of the payload files themselves.",
  "Records_Type": ["JobRegistryEntry"],
  "Fields": [
    {"name": "entry_id", "type": "string"},
    {"name": "entry_name", "type": "string"},
    {"name": "entry_slug", "type": "string"},
    {"name": "entry_type", "type": "string"},
    {"name": "file_path", "type": "string"},
    {"name": "created_date", "type": "string"},
    {"name": "modified_date", "type": "string"}
  ],
  "Values": [
    [
      "fdddc559-f389-4981-b01c-737d93bf1aea",
      "Book Writing Pipeline",
      "book_writing_pipeline",
      "template",
      "templates/book_writing_pipeline.bejson",
      "2026-08-25",
      "2026-08-25"
    ],
    [
      "eb05d9cd-333d-4fff-8e7b-44f7775892ca",
      "Refactor Chunker CLI",
      "refactor_chunker_cli",
      "schema",
      "jobs/refactor_chunker_cli.bejson",
      "2026-08-22",
      "2026-08-25"
    ]
  ]
}
```

## 4. Invariants & Rules
- `entry_type`: Strictly `"schema"` or `"template"`.
- Slugs: Generated via `re.sub(r'[^a-zA-Z0-9]+', '_', name.strip()).strip('_').lower()`.
- Atomic Writes: Writes must write to `.tmp` file, flush, and rename via `os.replace`.
- Field Map Caching: Mandatory dynamic field index resolution on every read and write.
