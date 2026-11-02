---
Name: BKS-1_Final_Schema_and_Architecture-V101.md
Description: Implementer's guide to the BEJSON Book Standard (BKS-1): every schema, rule, file format and error code, as built and tested in the reference implementation. Hand this to anyone updating a project to the standard.
Version: 1.0.1 (schema bks-1.0.0)
Date Created: 2026-10-29
Supersedes: BKS-1_Final_Schema_and_Architecture-V100.md, BEJSON_Book_Standard_BKS-1.md 0.1.0 DRAFT and BKS-1_Plan_Amendment-V020.md. 1.0.1 adds the export slug override (11.3), the BookWriter adoption notes (14.5) and the new store/export functions
Reference implementation: BookWriter-V115-PKG115.zip (the app, wired to the standard) and BKS_Standard-V115-PKG115.zip (the kit): `lib/Writing/` (Python 3.10+), 142 passing tests in the app, 71 in the kit
Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
RELATIONAL_ID: 5d66553b-1079-48ea-9b91-d9ec198c5655
---

# BKS-1 Final Schema and Architecture: Implementer's Guide

## 0. How to read this

- **Audience:** a developer updating a book-writing project (any language) so that it reads and writes books the standard way.
- **Normative words:** MUST, MUST NOT, SHOULD are used in the RFC sense. Everything in sections 3 to 12 is normative. Section 13 describes the Python reference code. Section 14 is the migration guide.
- **Format family:** BEJSON 104 only. No 105 features. The BEJSON Core libraries are frozen and MUST NOT be modified; this standard adds a new library family beside them.
- **Truth over prose:** every field table, enumeration, error table and the library reference below was generated from the reference code, so they cannot drift from it. Where this guide and the code ever disagree, the code and its tests are right; please report it.
- **Status of the parts:** section 15 lists exactly what is defined but not yet implemented. Nothing in this guide describes a feature that does not exist without saying so.

## 1. Decisions that are final

| # | Decision | Result |
|--:|---|---|
| 1 | Where a book lives | One **Book Document** per book: a single BEJSON **104db** file holding Book, Chapter, Generation and Export rows. The book is the source of truth |
| 2 | Timestamps | UTC ISO-8601 with `Z`, field names end `_at` |
| 3 | Gates | Declarative, evaluated in-process. **No shell command is ever run** for a book |
| 4 | Outline | `part` > `chapter` > `section`, plus `front` and `back` matter. Parts are structure only, never written |
| 5 | Absence | `null`, never `""`. An empty string is an error |
| 6 | Library | New family `lib/Writing/lib_bejson_Writing_bks_*` (non-AI). AI handling goes in a separate module, `lib_bejson_AI_ai_writing`, when an app is wired (not built yet) |
| 7 | Plan schema | **Exactly the JobMaker job schema** (`JobTask`, 11 fields, real arrays). A plan is a projection of the Book Document, never its source |
| 8 | Content hash | One fingerprint recipe (section 4.7) that exports are checked against |
| 9 | Editing a released book | Drops it back to `draft`, bumps the patch version and removes its Export rows |
| 10 | Arrays in plans | Plans use real JSON arrays, because JobRunner reads real arrays. This makes plan files fail Core's stage-0 validator, so plans have their own check (section 9.5) |

## 2. Architecture

### 2.1 Artifacts

| Artifact | Format | Typical location | Written by | Authority |
|---|---|---|---|---|
| Book Document | BEJSON 104db, `Records_Type ["Book","Chapter","Generation","Export"]` | `books/<slug>.bks.bejson` | the commit function only | **source of truth** |
| BookType file | BEJSON 104, `Records_Type ["BookType"]`, one row | `book_types/<slug>.bks-type.bejson` | seeding / the type editor | library |
| Plan | BEJSON 104a, JobMaker `JobTask` job | `jobs/<slug>.bejson` | `plan_from_book`, or JobMaker | derived (disposable) |
| Runner staging | Markdown files | `runs/<job slug>/<task id slug>.md` | JobRunner | scratch (disposable) |
| Export | md, md_zip, html, txt, json, bejson | `exports/<book slug>/<slug><ext>` | the export operation | derived (disposable) |
| Library entities | Author, Category, ContextAsset, RegistryEntry | the app's MFDB library | the app | library (schema defined here; storage not yet in the Writing family) |

Rules: all stored paths are **relative to the project root**, use `/`, and never contain `..`, a drive letter or a leading slash. Nothing outside the Book Document is ever read back into it except through the ingest step (9.6).

### 2.2 Data flow

```
 BookType (outline, gate profile) ──► create book ──► BOOK DOCUMENT (104db)  ◄──── commit (only writer)
                                                         │   ▲                        ▲
                                  plan_from_book         │   │ ingest (gate)          │ apply attempt (gate)
                                                         ▼   │                        │
                                       PLAN (JobMaker JobTask) ──► JobRunner ──► runs/*.md        in-process AI call
                                                                                                    (any provider)
 BOOK DOCUMENT ──► render ──► exports/*  (+ Export row, recorded at commit)
```

Two ways to write a chapter, one way to record it. Either an app calls a model itself, or a runner executes the plan and its staged text is ingested. Both end in the same gated attempt and the same commit.

### 2.3 Layers and ownership

| Layer | Module(s) | Rule |
|---|---|---|
| Frozen Core | `lib/Core/*` (field map, validator, list validator, atomic write, lock) | never edited; vendored byte-identical |
| Schema owner | `bks_registry` | the only place field names, types, enums and requirement flags are defined. Application code MUST NOT contain field-name string literals |
| Pure logic | `bks_derive`, `bks_gates`, `bks_render` | no I/O except `bks_render` returning bytes |
| State | `bks_store` | the only code that builds or edits Book Document rows; the only writer |
| Conformance | `bks_validator` | C1 to C4, plan check, library-file check |
| Bridge | `bks_plan`, `bks_export`, `bks_booktypes` | plan projection and ingest; export operation; type library |

### 2.4 Write rules

| Rule | Requirement |
|--:|---|
| W1 | The Book Document, with its full outline, exists **before the first model call**. |
| W2 | Every model attempt becomes a `Generation` row. The gate runs in-process on the staged text. Pass: chapter `accepted`. Fail: chapter `rejected` with a reason. A failed or empty attempt never overwrites an already accepted body. A provider error or empty response records a `failed` Generation and leaves the chapter as it was. |
| W3 | One commit path: recompute derived values, validate (C3; C4 when Export rows exist), lock, atomic replace. A document that fails validation is **never written**. |
| W4 | Resume needs nothing but the Book Document: the next chapter is the first writable node that is not `accepted`. |
| W5 | The Book Document wins. The plan's run-state columns are rewritten from it, never the reverse. |
| W6 | Plans, `runs/` files and exports are derived and may be deleted and rebuilt. |
| W7 | Editing a `complete` or `final` book sets it to `draft`, bumps the patch version (`0.1.0` to `0.1.1`) and deletes its Export rows (the files on disk are then unlinked and stale). |
| W8 | Writers take the file lock and write atomically (temp file, then replace). There is no second writer. |

## 3. File formats

### 3.1 Book Document (BEJSON 104db)

- `Format_Version: "104db"`. `Records_Type` is exactly `["Book","Chapter","Generation","Export"]`. No custom top-level headers (104db forbids them).
- `Fields` is **`Record_Type_Parent` followed by every Book, Chapter, Generation and Export field, in the registry order**. That is 68 columns: 1 + 25 + 16 + 16 + 10. Every field except `Record_Type_Parent` carries `"Record_Type_Parent": "<Entity>"` naming its owner. Field names are unique across the whole document (this is why every field has an entity prefix).
- Each row is full width. Column 0 is the entity name; the entity's own columns hold values; all other columns are `null`.
- Row order: the Book row, then Chapter rows by `chapter_order_index`, then Generation rows (oldest first), then Export rows.
- Exactly one Book row.
- Read through a **field map** (field name to column index). Hard-coded column positions are forbidden.
- Strip leading and trailing whitespace from keys and strings at the ingestion boundary, before building the field map.

### 3.2 BookType file (BEJSON 104)

`Format_Version: "104"`, `Records_Type ["BookType"]`, `Fields` = the BookType registry columns (name and type only, no `Record_Type_Parent`), exactly one row. Arrays are legal in 104. File name `<slug>.bks-type.bejson`. Built-in types are seeded as data files; they are not code branches.

### 3.3 Plan (BEJSON 104a, JobMaker job): see section 9.

### 3.4 Export files: see section 11.

## 4. Conventions that apply to every field

| # | Rule |
|--:|---|
| 4.1 | **Names**: `snake_case`, one entity prefix per entity (`book_`, `chapter_`, `generation_`, `export_`, `author_`, `category_`, `booktype_`, `context_`, `registry_`). Never mix prefixed and unprefixed names. |
| 4.2 | **Suffixes carry meaning**: `_uuid` primary key, `_uuid_fk` foreign key, `_at` UTC timestamp, `_text` string, `_md` Markdown string, `_flag` boolean, `_count` integer, `_index` integer, `_value` number, `_list` array, `_path_text` relative path, `_sha256_text` lowercase hex digest, `_hex` colour like `#DE2626`. |
| 4.3 | **Absence is `null`.** An empty string is an error (513). Booleans are `true`/`false`/`null`; `null` means "not evaluated". |
| 4.4 | **Timestamps**: exactly `YYYY-MM-DDTHH:MM:SSZ`, UTC. |
| 4.5 | **UUIDs**: canonical lowercase hyphenated. Primary keys are random UUIDv4, or UUIDv5 when an importer or part needs a stable id (`uuid5(book_uuid, "part:" + part title)` for parts). |
| 4.6 | **Foreign keys** point at the parent's UUID field, end `_fk`, and never dangle (521). Generations are append-only history and are never cascade-deleted. |
| 4.7 | **Content hash** (`book_content_sha256_text`): see below. |
| 4.8 | **Body normalisation**: `\r\n` and `\r` become `\n`; trailing whitespace of the whole body is stripped. Applied before storing, hashing and counting. |
| 4.9 | **Word count**: remove fenced code blocks (the text from a line starting with three backticks to the next such line), then count whitespace-separated tokens. `null` or empty body counts 0. |
| 4.10 | **Derived values are never trusted from callers**: `chapter_word_count`, `book_chapter_count` (nodes whose kind is not `part`), `book_word_count` (sum over those nodes) and `book_content_sha256_text` are recomputed on every commit. |
| 4.11 | **Schema version**: `book_schema_version_text` and `booktype_schema_version_text` are `bks-1.0.0`; a reader accepts any `bks-1.*`. |

**Content hash recipe (exact):**

```
text  = "BKS1\n" + NFC(book_title_text) + "\n"
for each Chapter row, ALL kinds including parts, in chapter_order_index order:
    text += "\x1e" + chapter_uuid + "\x1f" + (chapter_parent_uuid_fk or "") + "\x1f" + chapter_kind_text
          + "\x1f" + NFC(chapter_title_text) + "\x1f" + NFC(normalise(chapter_body_md) or "") + "\n"
book_content_sha256_text = lowercase hex of SHA-256(UTF-8(text))
```

Not hashed: status, version, timestamps, briefs, audit fields, generations, exports. **Test vector 1** is the worked example in section 16: its stored hash is `87f04e7df99c0984309d5c920a4af92bacb8fccc4a51c37533865c8c301b29bd`; a correct port reproduces it from the example's rows.

## 5. Book Document entities

### 5.1 Book (25 fields)

Primary key: `book_uuid`. Foreign keys: `book_booktype_uuid_fk`, `book_author_uuid_fk`, `book_category_uuid_fk`, `book_plan_uuid_fk`.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `book_uuid` | string | ● | Primary key, UUIDv4. |
| 2 | `book_title_text` | string | ● | Display title. |
| 3 | `book_subtitle_text` | string |  |  |
| 4 | `book_topic_text` | string | ● | What the book is about (the seed request). |
| 5 | `book_goal_text` | string |  | The measurable purpose of the book. Used in the plan's composed `Job_Goal`. |
| 6 | `book_booktype_uuid_fk` | string |  | External FK to BookType.booktype_uuid (library). |
| 7 | `book_booktype_slug_text` | string | ● | Snapshot of the type slug so the file validates without the library. |
| 8 | `book_author_uuid_fk` | string |  | External FK to Author.author_uuid. |
| 9 | `book_author_name_text` | string | ● | Byline snapshot (survives author deletion). |
| 10 | `book_category_uuid_fk` | string |  | External FK to Category.category_uuid. |
| 11 | `book_category_name_text` | string |  | Category snapshot. |
| 12 | `book_plan_uuid_fk` | string |  | `Book_Plan_ID` of the plan this book was produced from. |
| 13 | `book_language_text` | string | ● | BCP-47 tag, e.g. `en`, `en-GB`. |
| 14 | `book_audience_text` | string |  |  |
| 15 | `book_summary_text` | string |  |  |
| 16 | `book_cover_path_text` | string |  | Relative path only. Never absolute, never a URL to a secret. |
| 17 | `book_tags_list` | array |  | Array of strings (legal in 104/104db). |
| 18 | `book_version_text` | string | ● | Semver of the book CONTENT (not of the schema). |
| 19 | `book_status_text` | string | ● | `draft` · `complete` · `final` · `archived` |
| 20 | `book_chapter_count` | integer | ● | Derived: number of writable nodes (kind != part). |
| 21 | `book_word_count` | integer | ● | Derived: sum of chapter_word_count. |
| 22 | `book_content_sha256_text` | string |  | Derived: content fingerprint (see 4.7). Required when status is `final`. |
| 23 | `book_schema_version_text` | string | ● | `bks-1.0.0`. Absent/other means legacy. |
| 24 | `book_created_at` | string | ● | UTC ISO-8601 `YYYY-MM-DDTHH:MM:SSZ`. |
| 25 | `book_updated_at` | string | ● |  |

### 5.2 Chapter (16 fields)

Primary key: `chapter_uuid`. Foreign keys: `chapter_book_uuid_fk`, `chapter_parent_uuid_fk`, `chapter_generation_uuid_fk`.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `chapter_uuid` | string | ● | Primary key. Equals the plan task's `task_id`. |
| 2 | `chapter_book_uuid_fk` | string | ● | FK to Book.book_uuid (cascade). |
| 3 | `chapter_parent_uuid_fk` | string |  | FK to Chapter.chapter_uuid. Null = top level. Validated as a tree. |
| 4 | `chapter_kind_text` | string | ● | `front` · `part` · `chapter` · `section` · `back` |
| 5 | `chapter_order_index` | integer | ● | Global reading order, 1..N, unique and contiguous. |
| 6 | `chapter_title_text` | string | ● | Title only. Numbering is a render concern, never stored. |
| 7 | `chapter_brief_text` | string |  | The writing brief (the plan task's `task_description`). |
| 8 | `chapter_body_md` | string |  | The text, in Markdown. Null until drafted; always null for `part`. |
| 9 | `chapter_status_text` | string | ● | `planned` · `drafted` · `accepted` · `rejected` |
| 10 | `chapter_word_count` | integer | ● | Derived from the body (see 4.9). 0 when no body. |
| 11 | `chapter_audit_enabled_flag` | boolean | ● | Whether a gate applies to this node. |
| 12 | `chapter_audit_passed_flag` | boolean |  | Null until a gate has run. |
| 13 | `chapter_audit_fail_reason_text` | string |  | Required when status is `rejected`. |
| 14 | `chapter_generation_uuid_fk` | string |  | FK to Generation.generation_uuid of the accepted draft. |
| 15 | `chapter_created_at` | string | ● |  |
| 16 | `chapter_updated_at` | string | ● |  |

### 5.3 Generation (16 fields)

Primary key: `generation_uuid`. Foreign keys: `generation_target_uuid_fk`, `generation_author_uuid_fk`.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `generation_uuid` | string | ● | Primary key. |
| 2 | `generation_target_kind_text` | string | ● | `plan` · `chapter` |
| 3 | `generation_target_uuid_fk` | string | ● | Chapter uuid, or the plan id for `plan`. |
| 4 | `generation_provider_text` | string |  | Engine id, e.g. `gemini`, `tokenrouter`, `ollamalocal`. |
| 5 | `generation_model_text` | string |  |  |
| 6 | `generation_author_uuid_fk` | string |  | Author persona in force. |
| 7 | `generation_prompt_sha256_text` | string |  | Hash of the full prompt (never store the prompt text). |
| 8 | `generation_temperature_value` | number |  |  |
| 9 | `generation_max_tokens_count` | integer |  |  |
| 10 | `generation_input_tokens_count` | integer |  |  |
| 11 | `generation_output_tokens_count` | integer |  |  |
| 12 | `generation_attempt_index` | integer | ● | 1-based attempt for this target. |
| 13 | `generation_outcome_text` | string | ● | `accepted` · `rejected` · `failed` · `cancelled` |
| 14 | `generation_error_code` | integer |  | Family error code when failed. |
| 15 | `generation_started_at` | string | ● |  |
| 16 | `generation_finished_at` | string |  |  |

### 5.4 Export (10 fields)

Primary key: `export_uuid`. Foreign keys: `export_book_uuid_fk`.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `export_uuid` | string | ● | Primary key. |
| 2 | `export_book_uuid_fk` | string | ● | FK to Book.book_uuid (cascade). |
| 3 | `export_format_text` | string | ● | `md` · `md_zip` · `html` · `txt` · `json` · `bejson` |
| 4 | `export_renderer_text` | string | ● | `name@version` of the renderer. |
| 5 | `export_theme_text` | string |  | Renderer theme, e.g. `becss`. |
| 6 | `export_path_text` | string | ● | Relative path of the rendered file. |
| 7 | `export_size_bytes_count` | integer |  |  |
| 8 | `export_sha256_text` | string | ● | Hash of the rendered file. |
| 9 | `export_source_content_sha256_text` | string | ● | `book_content_sha256_text` at render time. Staleness = mismatch. |
| 10 | `export_created_at` | string | ● |  |

## 6. Library entities

These are defined by the registry. Their storage in the app's MFDB library is the app's responsibility today; adopters MUST use these exact column names. `BookType` is fully implemented as 104 files (section 10).

### 6.1 Author (21 fields)

Primary key: `author_uuid`. Foreign keys: none.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `author_uuid` | string | ● |  |
| 2 | `author_name_text` | string | ● | Byline. |
| 3 | `author_email_text` | string |  |  |
| 4 | `author_website_text` | string |  |  |
| 5 | `author_github_text` | string |  |  |
| 6 | `author_bio_text` | string |  |  |
| 7 | `author_avatar_path_text` | string |  | Relative path. |
| 8 | `author_archetype_text` | string |  |  |
| 9 | `author_persona_text` | string |  | Voice description. |
| 10 | `author_system_instruction_text` | string |  | Extra voice-only instructions. |
| 11 | `author_tone_list` | array |  | Array of strings. |
| 12 | `author_forbidden_topics_list` | array |  | Array of strings. |
| 13 | `author_formality_text` | string | ● | `casual` · `neutral` · `formal` |
| 14 | `author_verbosity_text` | string | ● | `concise` · `balanced` · `expansive` |
| 15 | `author_creativity_value` | number | ● | 0.0-1.0. |
| 16 | `author_max_response_tokens_count` | integer | ● |  |
| 17 | `author_thinking_enabled_flag` | boolean | ● |  |
| 18 | `author_tools_list` | array |  | Array of tool ids the persona may use. |
| 19 | `author_is_deleted_flag` | boolean | ● | Soft delete. |
| 20 | `author_created_at` | string | ● |  |
| 21 | `author_updated_at` | string | ● |  |

### 6.2 Category (7 fields)

Primary key: `category_uuid`. Foreign keys: none.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `category_uuid` | string | ● |  |
| 2 | `category_name_text` | string | ● |  |
| 3 | `category_slug_text` | string | ● | Unique among non-deleted. |
| 4 | `category_badge_color_hex` | string | ● | `#RRGGBB`. |
| 5 | `category_is_deleted_flag` | boolean | ● |  |
| 6 | `category_created_at` | string | ● |  |
| 7 | `category_updated_at` | string | ● |  |

### 6.3 BookType (19 fields)

Primary key: `booktype_uuid`. Foreign keys: none.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `booktype_uuid` | string | ● |  |
| 2 | `booktype_slug_text` | string | ● | Stable id used in plans: `technical_manual`. |
| 3 | `booktype_name_text` | string | ● |  |
| 4 | `booktype_description_text` | string |  |  |
| 5 | `booktype_family_text` | string | ● | `nonfiction` · `technical` · `analysis` · `creative` |
| 6 | `booktype_plan_instruction_text` | string | ● | What the planner must produce for this type. |
| 7 | `booktype_chapter_identity_text` | string | ● | Role/voice sentence given to the chapter writer. |
| 8 | `booktype_outline_template_list` | array |  | Array of `{title, brief, kind, part}` objects: default skeleton. |
| 9 | `booktype_required_sections_list` | array |  | Array of heading names every chapter (or the book) must contain. |
| 10 | `booktype_min_chapters_count` | integer | ● |  |
| 11 | `booktype_max_chapters_count` | integer | ● |  |
| 12 | `booktype_default_chapters_count` | integer | ● |  |
| 13 | `booktype_min_words_per_chapter_count` | integer | ● |  |
| 14 | `booktype_audit_profile_text` | string | ● | `none` · `standard` · `strict` |
| 15 | `booktype_default_exports_list` | array |  | Array of export formats rendered by default. |
| 16 | `booktype_is_builtin_flag` | boolean | ● |  |
| 17 | `booktype_schema_version_text` | string | ● | `bks-1.0.0`. |
| 18 | `booktype_created_at` | string | ● |  |
| 19 | `booktype_updated_at` | string | ● |  |

### 6.4 ContextAsset (9 fields)

Primary key: `context_uuid`. Foreign keys: none.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `context_uuid` | string | ● |  |
| 2 | `context_original_file_name_text` | string | ● |  |
| 3 | `context_file_format_text` | string | ● | `txt` · `code` · `json` · `bejson` |
| 4 | `context_source_path_text` | string | ● | Relative to the project root. Absolute paths are non-conforming. |
| 5 | `context_size_bytes_count` | integer | ● |  |
| 6 | `context_sha256_text` | string | ● |  |
| 7 | `context_study_instruction_text` | string | ● | `learn_only` · `direct_reference` |
| 8 | `context_is_active_flag` | boolean | ● |  |
| 9 | `context_uploaded_at` | string | ● |  |

### 6.5 RegistryEntry (9 fields)

Primary key: `registry_uuid`. Foreign keys: `registry_target_uuid_fk`.

| # | Field | Type | Req | Allowed values / meaning |
|--:|---|---|:-:|---|
| 1 | `registry_uuid` | string | ● |  |
| 2 | `registry_kind_text` | string | ● | `book` · `plan` · `booktype` · `author` · `category` · `template` · `schema` |
| 3 | `registry_name_text` | string | ● |  |
| 4 | `registry_slug_text` | string | ● |  |
| 5 | `registry_file_path_text` | string | ● | Relative path. |
| 6 | `registry_target_uuid_fk` | string |  | The described object's own uuid. |
| 7 | `registry_schema_version_text` | string | ● |  |
| 8 | `registry_created_at` | string | ● |  |
| 9 | `registry_updated_at` | string | ● |  |

## 7. Enumerations

| Field | Allowed values |
|---|---|
| `book_status_text` | `draft` · `complete` · `final` · `archived` |
| `chapter_kind_text` | `front` · `part` · `chapter` · `section` · `back` |
| `chapter_status_text` | `planned` · `drafted` · `accepted` · `rejected` |
| `generation_target_kind_text` | `plan` · `chapter` |
| `generation_outcome_text` | `accepted` · `rejected` · `failed` · `cancelled` |
| `export_format_text` | `md` · `md_zip` · `html` · `txt` · `json` · `bejson` |
| `author_formality_text` | `casual` · `neutral` · `formal` |
| `author_verbosity_text` | `concise` · `balanced` · `expansive` |
| `context_file_format_text` | `txt` · `code` · `json` · `bejson` |
| `context_study_instruction_text` | `learn_only` · `direct_reference` |
| `registry_kind_text` | `book` · `plan` · `booktype` · `author` · `category` · `template` · `schema` |
| `booktype_family_text` | `nonfiction` · `technical` · `analysis` · `creative` |
| `booktype_audit_profile_text` | `none` · `standard` · `strict` |

Reserved, not valid values yet: export formats `epub`, `docx`, `pdf`.

## 8. Relationships and integrity

### 8.1 Foreign keys

| From | To | Rule |
|---|---|---|
| `chapter_book_uuid_fk` | `book_uuid` | every chapter belongs to this book |
| `chapter_parent_uuid_fk` | `chapter_uuid` | the parent node; `null` for top level |
| `chapter_generation_uuid_fk` | `generation_uuid` | the accepted generation; required when accepted |
| `generation_target_uuid_fk` | `chapter_uuid` (kind `chapter`) or the plan id (kind `plan`) | chapter targets must resolve |
| `export_book_uuid_fk` | `book_uuid` | |
| `book_booktype_uuid_fk`, `book_author_uuid_fk`, `book_category_uuid_fk`, `book_plan_uuid_fk` | library / plan | external; not checked inside the Book Document |

### 8.2 Outline

- `chapter_order_index` is one global reading order **1..N over all rows, parts included**, no gaps.
- Parent rules: `part`, `front`, `back` have no parent; `chapter` has no parent or a `part`; `section` has a `chapter`.
- The parent graph must be a tree (checked by projecting `(chapter_uuid, chapter_parent_uuid_fk)` into a list with `id`/`parent_id` and running Core's list validator).
- A part row is created immediately before the first node that belongs to it.
- Writable nodes (those the model writes) are every kind except `part`.

### 8.3 Status machines

**Chapter:**

| Status | Body | Audit fields | Other |
|---|---|---|---|
| `planned` | `null` | passed `null` | no generation |
| `drafted` | present | | |
| `accepted` | present | if audit enabled: `chapter_audit_passed_flag = true` | `chapter_generation_uuid_fk` points at a Generation with outcome `accepted` that targets this chapter |
| `rejected` | present (the rejected text) | passed `false`, reason present | |

Parts are always `accepted` with no body and audit disabled. Transitions: `planned` or `rejected` or `accepted` to `accepted` (gate passed) or `rejected` (gate failed, unless already accepted, in which case nothing changes).

**Book:**

| Status | Meaning | Constraint |
|---|---|---|
| `draft` | at least one writable node not accepted, or edited since release | **no Export rows** |
| `complete` | every writable node `accepted` | exports allowed |
| `final` | complete and locked | hash required and correct; exports allowed |
| `archived` | retired, read-only | exports allowed |

Edits to a `complete` or `final` book return it to `draft` (W7).

### 8.4 Generation (provenance)

One row per model attempt. `generation_attempt_index` counts attempts per target from 1. Outcomes: `accepted`, `rejected` (gate failed), `failed` (provider error or empty response, chapter unchanged), `cancelled`. Provider, model, prompt hash, temperature, token counts and error code are recorded when known and `null` otherwise. Runner-staged text is recorded with provider `jobrunner`.

## 9. The plan (JobMaker job schema)

### 9.1 Why it is exactly JobMaker's schema

The plan is executed by JobRunner/JobMaker, so it MUST be that schema and nothing else. JobMaker rebuilds the whole file from a fixed header list on every save and keeps only `ref`, `text_based` and `chunks` on a context entry, so any extra header or key would be erased on first edit. Book data therefore lives only in the Book Document; the plan carries just what the runner needs.

### 9.2 Schema

`Format "BEJSON"`, `Format_Version "104a"`, `Format_Creator "Elton Boehnen"`, `Records_Type ["JobTask"]`.

| Header | Value for a book plan |
|---|---|
| `Schema_Name` | `Job Schema` |
| `Schema_Version` | `1.0` |
| `Schema_Description` | JobMaker's own text: "Custom job schema for the NewAgent task creation and tracking system, managing individual task states and optional auditing. Each task carries its own task_context (embedded, chunked files), task_reference (path-only refs), and task_mandatory (marks a task as a required, built-in step for the job's Job_Type/Job_Subtype). Job_Type/Job_Subtype classify the job; Contextualize_Plan/Contextualize_Last control what each task is injected with at run time. Also reused unmodified as the Template payload shape." |
| `Job_Goal` | composed text (9.3) |
| `Job_Type` / `Job_Subtype` | `writing` / `book` (book type is **not** in the plan; it is `book_booktype_slug_text`) |
| `Contextualize_Plan` / `Contextualize_Last` | `true` / `true` |
| `Job_Complete` | `true` only when every task is complete |
| `Creation_Date` | `YYYY-MM-DD` (date only, JobMaker's form) |
| `Completion_Date` | `YYYY-MM-DD` when complete, else `""` |

There is **no** `test_cmd` column, no `Target_File`, no `Execution_Traces`, and no `Book_*` header.

The 11 task fields, in this order:

| # | Field | Type |
|--:|---|---|
| 1 | `task_id` | string |
| 2 | `task_order` | integer |
| 3 | `task_name` | string |
| 4 | `task_description` | string |
| 5 | `task_completed` | boolean |
| 6 | `audit_enabled` | boolean |
| 7 | `audit_passed` | boolean |
| 8 | `audit_fail_reason` | string |
| 9 | `task_context` | array |
| 10 | `task_reference` | array |
| 11 | `task_mandatory` | boolean |

### 9.3 Projection from the Book Document

| Plan | Comes from |
|---|---|
| `task_id` | `chapter_uuid` (JobMaker preserves it on save) |
| `task_order` | 1..N over **writable** nodes only |
| `task_name` | `chapter_title_text` (title only, no numbering) |
| `task_description` | `chapter_brief_text` (or the title if the brief is null), then a blank line, then derived lines: `Part: <part title>` (node sits under a part) or `Section of: <parent title>` (section), then `Target length: about <N> words.` when a target is known |
| `task_completed` | chapter status is `accepted` |
| `audit_enabled` | `chapter_audit_enabled_flag` |
| `audit_passed` | `chapter_audit_passed_flag is true` |
| `audit_fail_reason` | the reason, or `""` |
| `task_context` / `task_reference` | the chapter's context assets (9.4) |
| `task_mandatory` | `true` |
| `Job_Goal` | `Write the book "<title>"` + ` for <audience>` (if any) + `, in <Language name> (<code>).` + ` Goal: <book_goal_text>` (if any). The only place the model sees title, audience and language |

The projection is **one way**. `task_description` is never parsed back into the book. Only `task_completed`, `audit_passed` and `audit_fail_reason` flow back, via sync (W5).

### 9.4 Context cells (real arrays)

- `task_context` is an array of entries `{"ref": "<relative path>", "text_based": true, "chunks": [{"chunk_id","chunk_label","chunk_content","chunk_index_pos","chunk_status"}]}`. Chunks are blank-line segments. The runner prints every embedded chunk to the model as study material.
- `task_reference` is an array of path strings the runner lists but never reads (use for non-text assets).
- The `learn_only` / `direct_reference` distinction of `context_study_instruction_text` cannot be represented in a plan (the runner treats all embedded context as study material). It stays on the `ContextAsset` row and is applied by whatever code drives the model.
- References written by this standard are relative. Absolute refs written by JobMaker's file browser are tolerated with a warning.

### 9.5 Plan check (`P`)

Plan files cannot pass Core's stage-0 validator, because Core rejects `array` columns inside a 104a document (this is the one scoped exception in the standard; Book Documents and BookType files still run Core stage 0). The plan check verifies: `Records_Type` and the 11 fields exactly; the header set exactly (anything extra or missing is rejected; keys starting `_` are ignored); header types and values; `task_id` is a UUID and unique; `task_order` is 1..N; the brief (first paragraph of `task_description`) is non-empty; context and reference cells have the shapes above (a JSON **string** in a cell is rejected, because the runner would silently drop it); `Job_Complete` agrees with the tasks; and, when the Book Document is supplied, that the task ids and order equal its writable chapters.

### 9.6 Reference runner behaviour and ingest

Reference runner: JobRunner 1.0.0 / JobMaker 2.8.0 (Python).

| Runner behaviour | Consequence |
|---|---|
| Builds each prompt from Job_Goal, `Job_Type / Job_Subtype`, the full plan, the previous task's full output, the task's embedded context, and its reference paths | context assets reach the model; nothing else from the book does |
| Writes each task's text to `runs/<job slug>/<task id slug>.md` and the joined text to `final.md` | `runs/` is staging only |
| `audit_enabled` runs an AI PASS/FAIL reviewer with retry; a failed mandatory task halts the run | a first check only; the BKS gate still runs at ingest |
| Never writes the Book Document | the **ingest step** records its output |

`task id slug` = the task id lowercased with each run of non-alphanumerics replaced by `_`.

**Ingest** (`plan_ingest_run`): for each plan task that is `task_completed`, whose chapter is not yet `accepted`, and whose staged file exists: read the file; run the BookType's gate on it; record a `Generation` (provider `jobrunner`) and set the chapter accepted or rejected exactly as in W2; on failure set that plan task back to `task_completed = false` so the runner redoes it; finally sync the plan from the book. The caller then commits the book and writes the plan.

### 9.7 Compatibility with JobMaker TypeScript 3.x

The TypeScript JobMaker (Job_Runner 3.1.16 inspected) uses the same `JobTask` / `Job Schema` shape and real arrays, but additionally writes a 12th column `test_cmd` and a `Target_File` header, and its `Job_Type` values are free text. The standard's plan is the 11-field subset, which the TypeScript validator already accepts (it requires only the first five fields and treats `test_cmd` as optional). To read a TypeScript plan into the standard form, use `plan_normalize_legacy`: it drops `Target_File` and an **empty** `test_cmd` column, and **refuses** a plan whose `test_cmd` holds a command (a book plan never runs shell commands).

To make the TypeScript tool produce standard book plans it MUST: (1) emit `Job_Type "writing"` / `Job_Subtype "book"` for books and omit `test_cmd` and `Target_File`; (2) preserve `task_id` on save; (3) never execute `test_cmd` for these jobs; (4) preserve array cells and the fixed header list; (5) stage each task's output where the ingest step can read it, or provide an equivalent ingest source (verify; the ingest reads `runs/<job slug>/<task id slug>.md` as the Python runner writes it).

## 10. BookTypes and gates

### 10.1 Gate vocabulary (the only gates)

| Rule | Meaning |
|---|---|
| `min_words` | word count (4.9) at least N |
| `max_words` | word count at most N |
| `must_include` | list of Markdown heading texts that must appear (case-insensitive) |
| `no_placeholders` | fails on `TODO`, `TBD`, `FIXME`, `lorem ipsum`, `[insert ...]`, `[...]` |
| `md_wellformed` | code fences are balanced |

An unknown rule or profile is refused (537). Profiles: `none` (no gate), `standard` (`min_words` + `no_placeholders`), `strict` (standard + `md_wellformed` + `must_include` the type's required sections). A chapter with `chapter_audit_enabled_flag = false` skips the gate. The failure reason lists every failed rule, e.g. `min_words=60 not met (29 words); missing heading 'Summary'`.

### 10.2 BookType rules

`1 <= min_chapters <= default_chapters <= max_chapters`; `required_sections` and `default_exports` are lists of non-empty strings; every default export is a valid export format; every outline-template item is an object with a non-empty `title` and a `kind` in `front`, `chapter`, `section`, `back` (optional `brief`, optional `part`); `booktype_plan_instruction_text` contains the placeholder `{chapter_count}` for the planner. Chapter limits apply when a plan is made, not when a book is opened. The outline template is a **starting** outline; it is truncated, never padded.

### 10.3 Built-in types

Ids are `uuid5(uuid5(URL, "https://boehnenelton2024.pages.dev/bks/booktype"), slug)` so every install derives the same id.

| Slug | Family | Chapters min/default/max | Min words | Profile | Required sections | Default exports |
|---|---|---|--:|---|---|---|
| `general_document` | nonfiction | 1/5/30 | 200 | standard | - | md, html |
| `standard_book` | nonfiction | 3/8/40 | 500 | standard | - | md, html, md_zip |
| `technical_manual` | technical | 4/8/40 | 600 | strict | Summary | md, html, md_zip |
| `readme` | technical | 3/6/12 | 80 | standard | - | md |
| `structural_report` | analysis | 3/7/20 | 250 | strict | Summary | md, html |
| `code_analysis` | analysis | 3/7/20 | 250 | strict | Summary | md, html |
| `fiction_novel` | creative | 8/20/60 | 1500 | standard | - | md, html, md_zip |
| `poetry_collection` | creative | 5/20/100 | 20 | none | - | md, html |
| `biography` | nonfiction | 5/12/40 | 800 | standard | - | md, html, md_zip |

The prompt texts (`booktype_plan_instruction_text`, `booktype_chapter_identity_text`) of the eight non-technical types are initial values and SHOULD be tuned; `technical_manual` is the standard's own text. Example row (technical_manual):

```json
{
 "booktype_uuid": "ed2ffac9-9238-529b-9f5c-cecddd23fbeb",
 "booktype_slug_text": "technical_manual",
 "booktype_name_text": "Technical Manual",
 "booktype_description_text": "A practical, example-driven manual for practitioners.",
 "booktype_family_text": "technical",
 "booktype_plan_instruction_text": "Produce a book title, a subtitle and an ordered outline of {chapter_count} chapters for a practical technical manual. Each chapter has a title (no numbering) and a 2-4 sentence brief saying what it must cover and how it connects to the previous chapter. Group chapters into at most four parts.",
 "booktype_chapter_identity_text": "You are a senior practitioner writing a precise, example-driven technical manual. Define terms on first use, show runnable examples, and end every chapter with a '## Summary' section.",
 "booktype_outline_template_list": [
  {
   "title": "Foundations",
   "brief": "Core concepts and the smallest working example.",
   "kind": "chapter",
   "part": "Foundations"
  },
  {
   "title": "Building Blocks",
   "brief": "The main components and how they compose.",
   "kind": "chapter",
   "part": "Foundations"
  },
  {
   "title": "Testing and Delivery",
   "brief": "Verifying and packaging the result.",
   "kind": "chapter",
   "part": "Delivery"
  }
 ],
 "booktype_required_sections_list": [
  "Summary"
 ],
 "booktype_min_chapters_count": 4,
 "booktype_max_chapters_count": 40,
 "booktype_default_chapters_count": 8,
 "booktype_min_words_per_chapter_count": 600,
 "booktype_audit_profile_text": "strict",
 "booktype_default_exports_list": [
  "md",
  "html",
  "md_zip"
 ],
 "booktype_is_builtin_flag": true,
 "booktype_schema_version_text": "bks-1.0.0",
 "booktype_created_at": "2026-10-25T09:00:00Z",
 "booktype_updated_at": "2026-10-25T09:00:00Z"
}
```

## 11. Rendering and export

### 11.1 Formats

| Format | Extension | Content |
|---|---|---|
| `md` | `.md` | front matter + Markdown |
| `md_zip` | `.zip` | `<slug>/book.bks.bejson`, `<slug>/metadata.json`, `<slug>/chapters/NNN-<title slug>.md`, deterministic archive |
| `html` | `.html` | one self-contained page |
| `txt` | `.txt` | plain text |
| `json` | `.bks.json` | `{"bks","book","chapters","generations"}` with registry field names |
| `bejson` | `.bks.bejson` | the Book Document itself, canonical dump |

### 11.2 Renderer rules

| Rule | Requirement |
|--:|---|
| R1 | **Deterministic**: the same document and options produce identical bytes (zip entries sorted, fixed timestamps). No clock or random value is written into output. |
| R2 | A renderer reads **only** the Book Document, which must conform at C3. |
| R3 | A `draft` book is refused (539) unless a **preview** is requested; a preview carries a visible DRAFT marker and writes no Export row. |
| R4 | The renderer owns headings and numbering. A first body heading that duplicates the node title (ignoring a numbering prefix and emphasis) is dropped. |
| R5 | HTML escapes **all** text before adding markup. Only headings, paragraphs, lists, blockquotes, fenced code, `**bold**`, `*italic*` and `` `code` `` are rendered. Links are never made live; there are no scripts and no external resources. |
| R6 | An export is rendered, written atomically, recorded as an Export row and the book committed at C4 as one operation. |

Numbering: parts `Part I:`, `Part II:`; chapters `1.`, `2.`; sections `1.1`; front and back matter unnumbered. Node heading level = tree depth + 1 (book title is `#`, a top-level node `##`, a chapter under a part `###`), capped at 6. Body headings are shifted under their node: a body heading with *n* hashes becomes `node_hashes + n - 1` (fence-aware, capped at 6). Markdown front matter keys: `title`, `author`, `language`, `version`, `status`, `content_sha256`. Text and Markdown end with the credit line `Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton` unless disabled. HTML themes: `becss` (white/black with `#DE2626` accent, dark mode by `prefers-color-scheme`) and `plain` (no accent).

### 11.3 Export rows

`export_path_text` is `exports/<book slug>/<book slug><extension>`; `book slug` is the title lowercased, ASCII-folded, non-alphanumerics to `-`. `export_renderer_text` is `<format>@<renderer version>`; `export_theme_text` is set for `html` only; `export_sha256_text` is the digest of the file; `export_source_content_sha256_text` is the book hash at render time. An application that holds several books with the same title MAY pass its own `slug` to the export operation (BookWriter uses `<title slug>-<first 8 characters of its library id>`), which replaces the title slug in the folder and file names. Re-exporting the same format and path **replaces** that row. A row whose source hash differs from the book's hash is **stale** (C4, 531); the library view can show "needs re-render" from the rows alone.

## 12. Conformance and error codes

### 12.1 Levels

| Level | Checks |
|---|---|
| **C1 Structure** | Core validator passes; `Fields`/`Records_Type` equal the registry; one Book row; schema version; required fields; enumerations; timestamps, UUIDs, relative paths; no empty strings |
| **C2 Integrity** | primary keys unique; foreign keys resolve; order 1..N; parent graph is a tree; parent kinds; derived values correct |
| **C3 Lifecycle** | statuses agree with data; audit gate passed for accepted audited chapters; accepted chapters have an accepted Generation; hash correct (required when final) |
| **C4 Release** | exports only on complete, final or archived books; no export rendered from older content |
| **P Plan** | section 9.5 |
| **L Library file** | Core validator; BEJSON 104 with the registry columns; per-row rules; BookType rules (10.2) |

Levels stack: C2 runs only if C1 passed, and so on. Everything the system **stores** must pass C3 (C4 once it has exports).

### 12.2 Error codes

Family 500 to 549. Codes 550 to 579 are reserved for application-layer errors. Compared with the 0.1.0 draft: names were aligned to its §13.2 table, 532/535/536 were renamed for the JobTask plan, 534 is retired, and 541 is new.

| Code | Name | Level | Meaning |
|--:|---|:-:|---|
| 500 | `E_BKS_STRUCTURE` | C1 | Core validator rejected the document (structure, types, null padding). |
| 501 | `E_BKS_SCHEMA_MISMATCH` | C1 | Fields / Records_Type differ from the registry (or a library file is not BEJSON 104 with the registry columns). |
| 502 | `E_BKS_VERSION_UNSUPPORTED` | C1 | `book_schema_version_text` is not `bks-1.*`. |
| 503 | `E_BKS_BOOK_COUNT` | C1 | A Book Document must hold exactly one Book row. |
| 510 | `E_BKS_REQUIRED_NULL` | C1 | A required field is null. |
| 511 | `E_BKS_ENUM_INVALID` | C1 | A value is outside its enumeration. |
| 512 | `E_BKS_TIMESTAMP_INVALID` | C1 | A `*_at` field is not a UTC `YYYY-MM-DDTHH:MM:SSZ` timestamp. |
| 513 | `E_BKS_EMPTY_STRING` | C1 | An empty string was stored (use null). |
| 514 | `E_BKS_UUID_INVALID` | C1 | A `*_uuid` / `*_uuid_fk` field is not a canonical lowercase UUID. |
| 515 | `E_BKS_PATH_INVALID` | C1 | A `*_path_text` field is not a relative, forward-slash path (no drive letter, no `..`). |
| 520 | `E_BKS_PK_DUPLICATE` | C2 | Duplicate primary key within an entity. |
| 521 | `E_BKS_FK_DANGLING` | C2 | A foreign key does not resolve. |
| 522 | `E_BKS_ORDER_INVALID` | C2 | `chapter_order_index` is not 1..N without gaps or repeats. |
| 523 | `E_BKS_OUTLINE_INVALID` | C2 | The chapter parent graph is not a valid tree (cycle or orphan), checked with Core's list validator. |
| 524 | `E_BKS_PARENT_KIND` | C2 | A node's kind does not fit its parent's kind. |
| 525 | `E_BKS_DERIVED_MISMATCH` | C2 | A derived value (word count, chapter count, book word count) is wrong. |
| 526 | `E_BKS_STATUS_INCONSISTENT` | C3 | Status contradicts data (e.g. planned with a body, complete with an unaccepted chapter). |
| 527 | `E_BKS_GATE_NOT_PASSED` | C3 | An accepted chapter with audit enabled has not passed its gate. |
| 528 | `E_BKS_PROVENANCE_MISSING` | C3 | An accepted chapter has no matching accepted Generation. |
| 529 | `E_BKS_HASH_MISMATCH` | C3 | `book_content_sha256_text` does not match the content (or is missing on a final book). |
| 530 | `E_BKS_EXPORT_NOT_ALLOWED` | C4 | An Export row exists on a book whose status does not allow exports. |
| 531 | `E_BKS_EXPORT_STALE` | C4 | An Export row was rendered from older content than the book now holds. |
| 532 | `E_BKS_PLAN_NOT_JOBTASK` | P | A plan is not the 11-field JobMaker `JobTask` schema. |
| 533 | `E_BKS_PLAN_HEADER` | P | A plan header is missing, extra or mistyped, or Job_Type/Job_Subtype is not `writing`/`book`. |
| 534 | `E_BKS_TEST_CMD_FORBIDDEN (retired)` | - | RETIRED (was `E_BKS_TEST_CMD_FORBIDDEN`). Never reused. |
| 535 | `E_BKS_PLAN_CELL_SHAPE` | P | A plan `task_context` / `task_reference` cell is not an array of the runner shapes. |
| 536 | `E_BKS_PLAN_LINK` | P | Plan task ids/order do not match the writable chapters of the Book Document. |
| 537 | `E_BKS_GATE_UNKNOWN` | gate | A gate uses an unknown rule or profile. |
| 538 | `E_BKS_IMPORT_UNSUPPORTED` | - | Import source not supported (reserved; importers not built). |
| 539 | `E_BKS_RENDER_FAILED` | render | A renderer refused or failed (draft book, bad format/theme, non-conforming document). |
| 540 | `E_BKS_MIGRATION_FAILED` | - | Migration failed (reserved). |
| 541 | `E_BKS_BOOKTYPE_LIMITS` | L | BookType limits, outline template or default exports are inconsistent (addition to the draft). |

## 13. Reference library (Python)

Package `lib/Writing/`. Python 3.10 or newer, standard library only, logging module only (no `print`), no hard-coded paths. Needs the frozen Core family plus `lib_bejson_Core_bejson_list_validator.py` (vendor it unmodified).

### `lib_bejson_Writing_bks_booktypes.py`

BookType library: the nine built-in types as data, BEJSON 104 files, gate rules, outline templates and new-book creation from a type.

| Function | Purpose |
|---|---|
| `bks_booktypes_builtin_rows()` | built-in types are data, not code branches. One function builds each registry row. |
| `bks_booktypes_doc(row)` | a BookType file is BEJSON 104 with the registry columns and one row. |
| `bks_booktypes_write_builtin(directory, overwrite)` | first-run seeding writes the nine built-ins to book_types/<slug>.bks-type.bejson (atomic; existing files are left alone). |
| `bks_booktypes_load(path)` | read one BookType file through the field map. |
| `bks_booktypes_list(directory)` | the library view lists every type in the folder. |
| `bks_booktypes_gate_rules(row)` | the audit profile plus floors become the in-process gate. No shell is ever involved. |
| `bks_booktypes_check_chapter_count(row, n)` | chapter limits apply when a plan is made, not when a book is opened. |
| `bks_booktypes_outline_nodes(row, chapter_count)` | the type's starting outline becomes the node list of a new book. |
| `bks_booktypes_new_book(row, chapter_count, nodes)` | one call makes a new book from a type: slug, id, outline and gate-ready metadata. |

### `lib_bejson_Writing_bks_derive.py`

Derived values: body normalisation, word count, content hash, UTC timestamps, UUID helpers.

| Function | Purpose |
|---|---|
| `bks_derive_normalize_body(text)` | every body is stored and hashed in one canonical form. |
| `bks_derive_count_words(text)` | word_count is a derived field; one rule everywhere (whitespace tokens, fenced code excluded). |
| `bks_derive_content_hash(book_title, chapter_rows)` | the book content hash is the fingerprint exports are checked against. Only structure, titles and text are hashed. |
| `bks_derive_now_utc()` | all timestamps are UTC ISO-8601 with a Z suffix. |
| `bks_derive_is_timestamp(value)` | the validator and the store share one strict timestamp test. |
| `bks_derive_new_uuid()` | primary keys are random UUIDs; importers mint deterministic ones from a book scope. |
| `bks_derive_scoped_uuid(book_uuid, label)` | parts and importer rows need stable ids so re-imports do not create duplicates. |
| `bks_derive_is_uuid(value)` | ids must be canonical lowercase hyphenated UUIDs. |
| `bks_derive_is_relative_path(value)` | stored paths are always relative and portable. |
| `bks_derive_runner_slug(value)` | JobRunner names its output files from the task id with this exact rule (JobRunner._slug). |
| `bks_derive_slugify(text, fallback)` | file and folder names for exports come from the title, never from user-typed paths. |

### `lib_bejson_Writing_bks_errors.py`

Bookstd error family (codes 500-549): constants, names and the BKSError exception.

| Function | Purpose |
|---|---|
| `bks_errors_name_for(code)` | one place maps a numeric code to its name, so messages and tests never repeat string literals. |

### `lib_bejson_Writing_bks_export.py`

Export operation: render, atomic file write, Export row (renderer, theme, path, hashes) and C4 commit; staleness listing and preview.

| Function | Purpose |
|---|---|
| `bks_export_write(project_root, book_path, doc, fmt, theme, credit, now, slug)` | R6 - an export is rendered, written atomically, recorded as an Export row, and the book is committed at C4, all as one operation. |
| `bks_export_stale(doc)` | the library view shows "needs re-render" from the rows alone. |
| `bks_export_preview(doc, fmt, theme)` | R3 preview - render a draft with a DRAFT stamp and write no Export row. |
| `bks_export_clear(project_root, book_path, doc)` | removing a book from a library must remove its export files and rows, or C4 would flag rows pointing at nothing. |

### `lib_bejson_Writing_bks_gates.py`

Declarative in-process chapter gates (min_words, max_words, must_include, no_placeholders, md_wellformed). Never runs shell commands.

| Function | Purpose |
|---|---|
| `bks_gates_rules_for_profile(profile, min_words, required_sections)` | BookType audit profiles expand to a fixed rule set so a gate never depends on a shell. |
| `bks_gates_check_rules(rules)` | reject gate vocab typos loudly instead of silently passing text. |
| `bks_gates_evaluate(body, rules)` | the one in-process audit applied to staged text before a chapter may be committed. |

### `lib_bejson_Writing_bks_plan.py`

Plan projection and runner bridge: plan_from_book, plan_sync, and ingest of JobRunner output into the Book Document.

| Function | Purpose |
|---|---|
| `bks_plan_job_goal(book)` | Job_Goal is the only place the model sees title, audience and language. |
| `bks_plan_task_description(chapter, by_id, target_words)` | task_description = brief + derived lines for the model; it is never parsed back. |
| `bks_plan_from_book(doc, context_by_chapter, target_words, creation_date)` | the plan is a projection of the Book Document. Result is exactly what JobMaker writes. |
| `bks_plan_sync(plan, doc)` | the Book Document always wins (W5); the plan's run-state columns are rewritten from it. |
| `bks_plan_ingest_run(doc, plan, runs_dir, gate_rules, provider, model, author_uuid, now)` | JobRunner never writes the Book Document. This reads its staged output (runs/<job slug>/<task id slug>.md), gates it, and records it. |
| `bks_plan_normalize_legacy(plan)` | JobMaker TypeScript 3.x still writes plans with an optional 12th column `test_cmd` and a `Target_File` header. Both are outside the standard; this reads such a plan into the standard form. |

### `lib_bejson_Writing_bks_registry.py`

Single schema owner for BKS-1: every entity, field, type, requirement and enumeration, plus the 104db Fields generator and a generated entity reference.

| Function | Purpose |
|---|---|
| `bks_registry_fields(entity)` | callers read the schema through this accessor so no field name is ever typed as a literal in app code. |
| `bks_registry_field_defs(entity)` | lookups by field name are needed by the validator on every row; build once per entity. |
| `bks_registry_book_document_fields()` | the 104db Fields array (Record_Type_Parent first, then every Book Document field, each carrying its owning entity) must come from the registry only. |
| `bks_registry_primary_key(entity)` | manifest primary keys and FK checks derive from naming rules, not a second table. |
| `bks_registry_foreign_keys(entity)` | foreign keys are declared by the _fk suffix. |
| `bks_registry_self_check()` | self-test used by the conformance suite: names are snake_case, prefixed per entity, and unique across all entities (104db needs unique names). |
| `bks_registry_markdown()` | handwritten schema docs are prohibited (10.8); the entity reference is generated from the registry. |

### `lib_bejson_Writing_bks_render.py`

Pure renderers (md, md_zip, html, txt, json, bejson): deterministic bytes from a validated Book Document; refuses drafts except preview; escapes all body text.

| Function | Purpose |
|---|---|
| `bks_render_strip_duplicate_heading(body, title)` | R4 - models usually repeat the title as a leading heading; the renderer owns headings and numbering. |
| `bks_render_shift_headings(body, node_hashes)` | body headings are shifted under the node heading so the document outline stays a tree (fence-aware). |
| `bks_render_markdown_to_html(body, node_hashes)` | R5 - every character of body text is escaped before any markup is added; only a small safe subset of Markdown is rendered and links are never made live. |
| `bks_render_book(doc, fmt, theme, preview, credit)` | R1-R5 in one pure function: same document and options give the same bytes; it reads only the Book Document; a draft is refused unless preview. |

### `lib_bejson_Writing_bks_store.py`

Book Document access through the Field Map Cache: create, read rows, apply a chapter attempt, refresh derived values, and the one gated commit that atomically writes the file.

| Function | Purpose |
|---|---|
| `bks_store_new_doc()` | a new Book Document starts from the registry Fields and no rows. |
| `bks_store_rows(doc, entity)` | every read goes through the Field Map Cache; no positional index is ever used. |
| `bks_store_tables(doc)` | the editing helpers work on all entities at once, then write back in canonical order. |
| `bks_store_set_tables(doc, tables)` | the single writer of Values. Rows are null-padded and grouped Book, Chapter, Generation, Export; chapters by order index. |
| `bks_store_book(doc)` | most callers want the single Book row. |
| `bks_store_chapters(doc)` | reading order of the outline (parts included). |
| `bks_store_is_writable(chapter_row)` | nodes the model writes. Parts are structure only. |
| `bks_store_create_book(title, topic, booktype_slug, author_name, language, nodes, goal, audience, subtitle, summary, tags, author_uuid, booktype_uuid, category_uuid, category_name, plan_uuid, book_uuid, now)` | a new book is created with its full outline before any model call. |
| `bks_store_refresh_derived(doc, now)` | derived values are never trusted from callers; they are recomputed from bodies on every commit. |
| `bks_store_apply_attempt(doc, chapter_uuid, body_md, rules, provider, model, author_uuid, prompt_sha256, temperature, max_tokens, input_tokens, output_tokens, started_at, now)` | the single path that records one model attempt: stage text, run the gate, record a Generation, and set the chapter state. |
| `bks_store_apply_failure(doc, chapter_uuid, error_code, provider, model, author_uuid, now, outcome)` | a provider error (no text) is still history; the chapter is left exactly as it was. |
| `bks_store_update_chapter(doc, chapter_uuid, title, brief, now)` | titles and briefs are edited after planning; a chapter whose wording changed is no longer accepted, but its text is kept for the author (status "drafted"). |
| `bks_store_update_book(doc, updates, now)` | catalog metadata (category, author, language...) changes without touching content, so it never drops a released book to draft or changes the hash. |
| `bks_store_update_title(doc, title, now)` | the title is part of the content hash, so changing it is a content edit (W7). |
| `bks_store_body_by_position(doc, position)` | later chapters are drafted with the previous chapter's text as context. |
| `bks_store_mark_complete(doc, now)` | "complete" is only true when every writable node is accepted. |
| `bks_store_finalize(doc, now)` | final locks the content hash that exports must match. |
| `bks_store_load(path)` | reading a book never validates implicitly; callers choose a level. |
| `bks_store_commit(path, doc, level, now)` | the one write path: recompute derived values, validate, then atomic replace under a lock. A document that fails is never written. |

### `lib_bejson_Writing_bks_validator.py`

Conformance levels C1-C4 for Book Documents and the plan check P for JobMaker plans.

| Function | Purpose |
|---|---|
| `bks_validate_book(doc, level)` | one entry point for Book Document conformance. Levels stack: C2 only runs when C1 passed, and so on. |
| `bks_validate_plan(plan, book_doc)` | a plan is the JobMaker job schema exactly. It deliberately does not run Core stage 0, because JobMaker types two columns as array inside a 104a document. |
| `bks_validate_library_doc(doc, entity)` | library entity files (BookType today) are BEJSON 104 with the registry columns and no Record_Type_Parent. |
| `bks_validate_booktype(doc)` |  |


Access pattern for adopters in any language: build the registry's `Fields`, create a field map, read rows into `{field: value}` dicts, edit dicts, write them back in canonical order, validate, then atomic-replace. Never index by position.

## 14. Migration guide for existing projects

### 14.1 Checklist

1. Vendor the Core family unmodified; add the Writing family (or port it, section 14.4).
2. Delete every raw field-name literal; resolve names through the registry.
3. Make the Book Document the system of record. Create it (with the full outline) before the first model call (W1).
4. Route every write through the one commit path (W3). Remove hand-rolled inserts and any second writer.
5. Replace `""` with `null`; rename timestamps to `<entity>_created_at` / `<entity>_updated_at` in UTC.
6. Record each model call as a `Generation` row and gate it in-process (W2). Remove any shell-based checks.
7. Generate plans with `plan_from_book`; stop reading plans as a source of book data.
8. Render and export through the export operation; stop hand-building archives.
9. Run the conformance checks (C1 to C3, plus C4 where exports exist) over every stored book and the plan check over every plan; add the negative tests (one violation per error code).
10. Bump versions and keep a change log as your own project rules require.

### 14.2 Field maps from existing systems

**BookWriter 1.1.x to BKS** (names as found in BookWriter 1.1.2):

| BookWriter | BKS |
|---|---|
| `plan_book_title_text`, `session_prompt_input_text` | `book_title_text`, `book_topic_text` |
| `session_target_chapter_count` | not stored; `book_chapter_count` is derived |
| `session_author_uuid_fk` | `book_author_uuid_fk` (and `book_author_name_text`) |
| `chapter_uuid`, `chapter_sequence_index` | `chapter_uuid` (= plan `task_id`), `chapter_order_index` (1..N over all rows) |
| `chapter_title_text`, `chapter_generation_prompt_text` | `chapter_title_text`, `chapter_brief_text` |
| `chapter_is_drafted_flag` | `chapter_status_text` (`planned` / `accepted`) |
| `session_gemini_model_name`, `session_provider_name_text` | `generation_model_text`, `generation_provider_text` on Generation rows |
| `book_chapter_count_total`, `book_export_zip_file_path` | `book_chapter_count` (derived); an `Export` row of format `md_zip` |
| `*_created_utc_timestamp` | `*_created_at` (add `*_updated_at`) |
| `author_creativity_score`, `author_max_response_tokens` | `author_creativity_value`, `author_max_response_tokens_count` |
| `context_source_file_path`, `context_file_size_bytes_metric`, `context_*_type` | `context_source_path_text`, `context_size_bytes_count`, `context_*_text`; add `context_sha256_text` |
| `session_execution_status`, `ui_*`, `provider_*`, `config_*` | stay app-local |
| `""` meaning "no value" | `null` |

**Cli_Bookwriter plan to BKS:**

| Legacy | BKS |
|---|---|
| `Writing_Title` | `book_title_text`, `book_topic_text` |
| `Writing_Type` (e.g. `standard book`) | `book_booktype_slug_text` (lowercase, `_`) |
| `Writing_Category` | `book_category_name_text` (then `book_category_uuid_fk` after lookup) |
| `Book_Goal` | `book_goal_text` (and the composed `Job_Goal`) |
| `Section_Count` (string) | derived `book_chapter_count` |
| `Task_ID` (`TASK1`) | `chapter_uuid` = plan `task_id` (UUIDv5 scoped to the book) |
| `Task_Name` (`Chapter 1: Title`) | `chapter_title_text` = `Title` (number stripped) |
| *(none)* | `chapter_brief_text` (synthesised from the goal; report it as a loss) |
| `Is_Audit` | `chapter_audit_enabled_flag` / `audit_enabled` |
| `Is_Ready` | dropped (inert) |
| `Author_ID` | `book_author_uuid_fk` only if it is a UUID, else `null` (report) |

**Bookmaker book to BKS:** `Book.entry_id` becomes a tag `legacy-import:<id>` in `book_tags_list` and `book_uuid` is the UUIDv5 of it; `Book.topic`/`Book.title` to `book_topic_text`/`book_title_text`; `Book.plan_name` dropped (`book_plan_uuid_fk` null unless the plan is imported); `Book.generation_date` to `book_created_at` and `book_updated_at` (else import time); `Chapter.chapter_number` to `chapter_order_index`; `Chapter.chapter_title`/`Chapter.content` to `chapter_title_text`/`chapter_body_md`.

**Specified, importers not built:** BookCMS V304 (`Book.chapters` JSON string of HTML bodies to Chapter rows with HTML converted to Markdown and tag `converted-from-html`; `authorId`/`categoryId` to the `_uuid_fk` fields when UUIDs, else looked up by name; a data-URL cover is written to a relative file first; writing types `general`/`structural`/`code`/`readme`/`book` to `book_booktype_slug_text`), AuthorCMS (`Book.bookType` `Fiction Novel`/`Technical Guide`/`Poetry Collection`/`Biography` to `fiction_novel`/`technical_manual`/`poetry_collection`/`biography`; base64 cover written to a relative file), and `book_builder.py` input (replace the positional `v[0] == "Chapter"` test with a field-map lookup of `Record_Type_Parent`).

### 14.3 Definition of done

An adopter is conformant when: (a) every book it stores validates at C3 and, with exports, at C4; (b) its plans pass the plan check and load, save and run unchanged in JobMaker/JobRunner; (c) a failed gate never overwrites an accepted chapter; (d) a draft book cannot be exported; (e) editing a released book drops it to draft and removes its exports; (f) its renderers are deterministic; and (g) it reproduces **test vector 1** (the hash in section 16) from the example rows.

### 14.4 Porting to another language

Port, in this order: registry tables and enums; body normalisation, word count and the hash recipe (check against test vector 1); field-map reads and the single writer; C1 to C4 and the plan check (check against the example and one deliberately broken document per error code); gates; the plan projection; renderers. Keep the Core validator as stage 0 for Book Documents and BookType files.

### 14.5 Worked adoption: BookWriter 1.1.5

BookWriter (Flask, MFDB for app state) was wired to the standard without changing its web UI. The decisions are a template for other apps.

| Concern | What it does |
|---|---|
| Split of storage | The MFDB keeps sessions, chapter prompts, authors, categories, context assets, provider settings and the library catalog. The Book Document holds chapter text, status and provenance. |
| Identity | `book_uuid` = the app's plan id; `chapter_uuid` = the app's PlanChapter id (so it is also the plan `task_id`). File `data/books/<plan_uuid>.bks.bejson`. |
| Creation (W1) | Generating a plan creates the Book Document with the full outline before any chapter is drafted. Regenerating a plan or deleting the session deletes the old file. |
| Drafting (W2) | Every model call goes through one attempt function: gate in-process, record a Generation (provider, model, temperature, max tokens, attempt number), set the chapter state, commit. A provider error or empty reply is a `failed` Generation and leaves the chapter alone. A failed audit returns an error carrying the reason and never overwrites an accepted body. |
| Edits | Changing a title or brief keeps the text and sets the chapter `drafted`; the app's own "needs redraft" flag stays in step. Editing a complete book returns it to draft (W7). |
| Catalog | Cataloging requires every writable chapter accepted, marks the book `complete` and mirrors category and author onto the Book row. Removing a book from the library deletes its export files and Export rows. |
| Export | The standard export operation renders the book type's default formats (always including `md_zip`, which is the download) under `exports/<slug>-<id8>/`. The reader page is the standard HTML renderer. |
| Settings | `book_language` (en), `default_book_type` (standard_book), `audit_profile` (none, standard, strict; default `none` so behaviour is unchanged) and `audit_min_words`. Audit flags are fixed per chapter when a plan is created. |
| Errors | A BKS refusal is wrapped in the app's own typed error (code 497) with the BKS code and name in its context; nothing invalid is ever written. |
| Legacy data | A pre-standard Bookmaker file `<plan_uuid>.bejson` is imported on first access (chapters become `accepted`, provider `legacy-import`, not audited), then moved to `backups/legacy_books/`. |
| JobMaker | `GET /api/plans/<plan_uuid>/jobmaker-plan` returns the one-way projection (section 9). Context assets are not embedded. |

## 15. Defined but not yet implemented

- Storage of the Author, Category, ContextAsset and RegistryEntry entities inside the Writing family (schemas are final; the app's existing MFDB library is where they live today).
- Importers (error 538), the legacy-to-BKS migration runner (540), and MFDB pack/unpack of a book into a library.
- `lib_bejson_AI_ai_writing` (prompt assembly and generation provenance capture); to be created when an app is wired.
- Wiring into Cli_Bookwriter (BookWriter is wired, section 14.5); application-layer error codes 550 to 579 (BookWriter keeps its own 480 to 497 and maps BKS errors to 497).
- Reserved export formats `epub`, `docx`, `pdf`.

## 16. Worked example (generated by the reference code, passes C3 and the plan check)

Rows are shown as objects with `null` fields omitted; in the file each is a full-width positional row, null-padded.

**Book row**

```json
{
 "book_uuid": "a75483f3-bbcc-5a9b-8e5f-a8e292fa668f",
 "book_title_text": "Headless CLI",
 "book_topic_text": "CLI pipelines",
 "book_goal_text": "A practical manual.",
 "book_booktype_slug_text": "technical_manual",
 "book_author_name_text": "Elton Boehnen",
 "book_language_text": "en",
 "book_audience_text": "developers",
 "book_version_text": "0.1.0",
 "book_status_text": "final",
 "book_chapter_count": 2,
 "book_word_count": 34,
 "book_content_sha256_text": "87f04e7df99c0984309d5c920a4af92bacb8fccc4a51c37533865c8c301b29bd",
 "book_schema_version_text": "bks-1.0.0",
 "book_created_at": "2026-10-29T10:00:00Z",
 "book_updated_at": "2026-10-29T10:11:00Z"
}
```

**Chapter rows (first two: a part and a chapter)**

```json
{
 "chapter_uuid": "92d6c9ae-c5b4-5e7f-ba7b-5ce69be7d8dc",
 "chapter_book_uuid_fk": "a75483f3-bbcc-5a9b-8e5f-a8e292fa668f",
 "chapter_kind_text": "part",
 "chapter_order_index": 1,
 "chapter_title_text": "Basics",
 "chapter_status_text": "accepted",
 "chapter_word_count": 0,
 "chapter_audit_enabled_flag": false,
 "chapter_created_at": "2026-10-29T10:00:00Z",
 "chapter_updated_at": "2026-10-29T10:00:00Z"
}
{
 "chapter_uuid": "756310a3-e679-5391-8103-4637a78d8a8d",
 "chapter_book_uuid_fk": "a75483f3-bbcc-5a9b-8e5f-a8e292fa668f",
 "chapter_parent_uuid_fk": "92d6c9ae-c5b4-5e7f-ba7b-5ce69be7d8dc",
 "chapter_kind_text": "chapter",
 "chapter_order_index": 2,
 "chapter_title_text": "Foundations",
 "chapter_brief_text": "Explain pipes and exit codes.",
 "chapter_body_md": "# Foundations\n\nA short example body used only to illustrate the schema.\n\n## Summary\n\nPipes compose tools.",
 "chapter_status_text": "accepted",
 "chapter_word_count": 17,
 "chapter_audit_enabled_flag": true,
 "chapter_audit_passed_flag": true,
 "chapter_generation_uuid_fk": "0565ee51-5866-490e-bc6f-5fa617a6c69a",
 "chapter_created_at": "2026-10-29T10:00:00Z",
 "chapter_updated_at": "2026-10-29T10:01:00Z"
}
```

**Generation row**

```json
{
 "generation_uuid": "0565ee51-5866-490e-bc6f-5fa617a6c69a",
 "generation_target_kind_text": "chapter",
 "generation_target_uuid_fk": "756310a3-e679-5391-8103-4637a78d8a8d",
 "generation_provider_text": "gemini",
 "generation_model_text": "gemini-2.5-flash",
 "generation_temperature_value": 0.7,
 "generation_attempt_index": 1,
 "generation_outcome_text": "accepted",
 "generation_started_at": "2026-10-29T10:01:00Z",
 "generation_finished_at": "2026-10-29T10:01:00Z"
}
```

**Plan projected from it**

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Schema_Name": "Job Schema",
  "Schema_Version": "1.0",
  "Schema_Description": "Custom job schema for the NewAgent task creation and tracking system, managing individual task states and optional auditing. Each task carries its own task_context (embedded, chunked files), task_reference (path-only refs), and task_mandatory (marks a task as a required, built-in step for the job's Job_Type/Job_Subtype). Job_Type/Job_Subtype classify the job; Contextualize_Plan/Contextualize_Last control what each task is injected with at run time. Also reused unmodified as the Template payload shape.",
  "Job_Goal": "Write the book \"Headless CLI\" for developers, in English (en). Goal: A practical manual.",
  "Job_Type": "writing",
  "Job_Subtype": "book",
  "Contextualize_Plan": true,
  "Contextualize_Last": true,
  "Job_Complete": true,
  "Creation_Date": "2026-10-29",
  "Completion_Date": "2026-11-01",
  "Records_Type": [
    "JobTask"
  ],
  "Fields": [
    {
      "name": "task_id",
      "type": "string"
    },
    {
      "name": "task_order",
      "type": "integer"
    },
    {
      "name": "task_name",
      "type": "string"
    },
    {
      "name": "task_description",
      "type": "string"
    },
    {
      "name": "task_completed",
      "type": "boolean"
    },
    {
      "name": "audit_enabled",
      "type": "boolean"
    },
    {
      "name": "audit_passed",
      "type": "boolean"
    },
    {
      "name": "audit_fail_reason",
      "type": "string"
    },
    {
      "name": "task_context",
      "type": "array"
    },
    {
      "name": "task_reference",
      "type": "array"
    },
    {
      "name": "task_mandatory",
      "type": "boolean"
    }
  ],
  "Values": [
    [
      "756310a3-e679-5391-8103-4637a78d8a8d",
      1,
      "Foundations",
      "Explain pipes and exit codes.\n\nPart: Basics",
      true,
      true,
      true,
      "",
      [],
      [],
      true
    ],
    [
      "87ab5418-b52e-5d36-a29f-69352dc20523",
      2,
      "Packaging",
      "Ship the tool as one archive.\n\nPart: Basics",
      true,
      true,
      true,
      "",
      [],
      [],
      true
    ]
  ],
  "_bejson_field_map": {
    "task_id": 0,
    "task_order": 1,
    "task_name": 2,
    "task_description": 3,
    "task_completed": 4,
    "audit_enabled": 5,
    "audit_passed": 6,
    "audit_fail_reason": 7,
    "task_context": 8,
    "task_reference": 9,
    "task_mandatory": 10
  }
}
```

---

*Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton*
