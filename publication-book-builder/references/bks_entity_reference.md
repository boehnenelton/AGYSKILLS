# BKS-1 Entity Reference (generated, schema bks-1.0.0)

Generated from `lib_bejson_Writing_bks_registry.py`. Do not edit by hand.

## Book (Book Document, 25 fields)

Primary key: `book_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `book_uuid` | string | yes |  |
| `book_title_text` | string | yes |  |
| `book_subtitle_text` | string | no |  |
| `book_topic_text` | string | yes |  |
| `book_goal_text` | string | no |  |
| `book_booktype_uuid_fk` | string | no |  |
| `book_booktype_slug_text` | string | yes |  |
| `book_author_uuid_fk` | string | no |  |
| `book_author_name_text` | string | yes |  |
| `book_category_uuid_fk` | string | no |  |
| `book_category_name_text` | string | no |  |
| `book_plan_uuid_fk` | string | no |  |
| `book_language_text` | string | yes |  |
| `book_audience_text` | string | no |  |
| `book_summary_text` | string | no |  |
| `book_cover_path_text` | string | no |  |
| `book_tags_list` | array | no |  |
| `book_version_text` | string | yes |  |
| `book_status_text` | string | yes | draft, complete, final, archived |
| `book_chapter_count` | integer | yes |  |
| `book_word_count` | integer | yes |  |
| `book_content_sha256_text` | string | no |  |
| `book_schema_version_text` | string | yes |  |
| `book_created_at` | string | yes |  |
| `book_updated_at` | string | yes |  |

## Chapter (Book Document, 16 fields)

Primary key: `chapter_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `chapter_uuid` | string | yes |  |
| `chapter_book_uuid_fk` | string | yes |  |
| `chapter_parent_uuid_fk` | string | no |  |
| `chapter_kind_text` | string | yes | front, part, chapter, section, back |
| `chapter_order_index` | integer | yes |  |
| `chapter_title_text` | string | yes |  |
| `chapter_brief_text` | string | no |  |
| `chapter_body_md` | string | no |  |
| `chapter_status_text` | string | yes | planned, drafted, accepted, rejected |
| `chapter_word_count` | integer | yes |  |
| `chapter_audit_enabled_flag` | boolean | yes |  |
| `chapter_audit_passed_flag` | boolean | no |  |
| `chapter_audit_fail_reason_text` | string | no |  |
| `chapter_generation_uuid_fk` | string | no |  |
| `chapter_created_at` | string | yes |  |
| `chapter_updated_at` | string | yes |  |

## Generation (Book Document, 16 fields)

Primary key: `generation_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `generation_uuid` | string | yes |  |
| `generation_target_kind_text` | string | yes | plan, chapter |
| `generation_target_uuid_fk` | string | yes |  |
| `generation_provider_text` | string | no |  |
| `generation_model_text` | string | no |  |
| `generation_author_uuid_fk` | string | no |  |
| `generation_prompt_sha256_text` | string | no |  |
| `generation_temperature_value` | number | no |  |
| `generation_max_tokens_count` | integer | no |  |
| `generation_input_tokens_count` | integer | no |  |
| `generation_output_tokens_count` | integer | no |  |
| `generation_attempt_index` | integer | yes |  |
| `generation_outcome_text` | string | yes | accepted, rejected, failed, cancelled |
| `generation_error_code` | integer | no |  |
| `generation_started_at` | string | yes |  |
| `generation_finished_at` | string | no |  |

## Export (Book Document, 10 fields)

Primary key: `export_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `export_uuid` | string | yes |  |
| `export_book_uuid_fk` | string | yes |  |
| `export_format_text` | string | yes | md, md_zip, html, txt, json, bejson |
| `export_renderer_text` | string | yes |  |
| `export_theme_text` | string | no |  |
| `export_path_text` | string | yes |  |
| `export_size_bytes_count` | integer | no |  |
| `export_sha256_text` | string | yes |  |
| `export_source_content_sha256_text` | string | yes |  |
| `export_created_at` | string | yes |  |

## Author (library file, 21 fields)

Primary key: `author_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `author_uuid` | string | yes |  |
| `author_name_text` | string | yes |  |
| `author_email_text` | string | no |  |
| `author_website_text` | string | no |  |
| `author_github_text` | string | no |  |
| `author_bio_text` | string | no |  |
| `author_avatar_path_text` | string | no |  |
| `author_archetype_text` | string | no |  |
| `author_persona_text` | string | no |  |
| `author_system_instruction_text` | string | no |  |
| `author_tone_list` | array | no |  |
| `author_forbidden_topics_list` | array | no |  |
| `author_formality_text` | string | yes | casual, neutral, formal |
| `author_verbosity_text` | string | yes | concise, balanced, expansive |
| `author_creativity_value` | number | yes |  |
| `author_max_response_tokens_count` | integer | yes |  |
| `author_thinking_enabled_flag` | boolean | yes |  |
| `author_tools_list` | array | no |  |
| `author_is_deleted_flag` | boolean | yes |  |
| `author_created_at` | string | yes |  |
| `author_updated_at` | string | yes |  |

## Category (library file, 7 fields)

Primary key: `category_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `category_uuid` | string | yes |  |
| `category_name_text` | string | yes |  |
| `category_slug_text` | string | yes |  |
| `category_badge_color_hex` | string | yes |  |
| `category_is_deleted_flag` | boolean | yes |  |
| `category_created_at` | string | yes |  |
| `category_updated_at` | string | yes |  |

## BookType (library file, 19 fields)

Primary key: `booktype_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `booktype_uuid` | string | yes |  |
| `booktype_slug_text` | string | yes |  |
| `booktype_name_text` | string | yes |  |
| `booktype_description_text` | string | no |  |
| `booktype_family_text` | string | yes | nonfiction, technical, analysis, creative |
| `booktype_plan_instruction_text` | string | yes |  |
| `booktype_chapter_identity_text` | string | yes |  |
| `booktype_outline_template_list` | array | no |  |
| `booktype_required_sections_list` | array | no |  |
| `booktype_min_chapters_count` | integer | yes |  |
| `booktype_max_chapters_count` | integer | yes |  |
| `booktype_default_chapters_count` | integer | yes |  |
| `booktype_min_words_per_chapter_count` | integer | yes |  |
| `booktype_audit_profile_text` | string | yes | none, standard, strict |
| `booktype_default_exports_list` | array | no |  |
| `booktype_is_builtin_flag` | boolean | yes |  |
| `booktype_schema_version_text` | string | yes |  |
| `booktype_created_at` | string | yes |  |
| `booktype_updated_at` | string | yes |  |

## ContextAsset (library file, 9 fields)

Primary key: `context_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `context_uuid` | string | yes |  |
| `context_original_file_name_text` | string | yes |  |
| `context_file_format_text` | string | yes | txt, code, json, bejson |
| `context_source_path_text` | string | yes |  |
| `context_size_bytes_count` | integer | yes |  |
| `context_sha256_text` | string | yes |  |
| `context_study_instruction_text` | string | yes | learn_only, direct_reference |
| `context_is_active_flag` | boolean | yes |  |
| `context_uploaded_at` | string | yes |  |

## RegistryEntry (library file, 9 fields)

Primary key: `registry_uuid`

| Field | Type | Required | Values |
|---|---|---|---|
| `registry_uuid` | string | yes |  |
| `registry_kind_text` | string | yes | book, plan, booktype, author, category, template, schema |
| `registry_name_text` | string | yes |  |
| `registry_slug_text` | string | yes |  |
| `registry_file_path_text` | string | yes |  |
| `registry_target_uuid_fk` | string | no |  |
| `registry_schema_version_text` | string | yes |  |
| `registry_created_at` | string | yes |  |
| `registry_updated_at` | string | yes |  |


Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
