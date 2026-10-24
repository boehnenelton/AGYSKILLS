# BEJSON CMS - Entity Schema Registry & Taxonomy Specification

Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Effective Date: 2026-10-21
RELATIONAL_ID: 1f2e3d4c-5b6a-7081-92a3-b4c5d6e7f809
Version: 100
Release_Version: 300

---

## 1. Schema Overview

All 10 entity tables conform to BEJSON Format 104 (`.104.bejson`), requiring explicit `Fields` and `Values` arrays. Dynamic O(1) field map indexing is mandatory across all reader/writer operations:

```python
field_map = {field_def["name"]: idx for idx, field_def in enumerate(doc["Fields"])}
```

---

## 2. The 10 Entity Schemas

### 1. PageRecord (`pages.104.bejson`)
- **Primary Key**: `page_uuid` (string, UUIDv4)
- **Prefix**: `page_`
- **Fields**:
  - `page_uuid`: Unique immutable identifier
  - `page_title`: Article display title
  - `page_slug`: URL-friendly identifier
  - `page_content`: Markdown or HTML body text
  - `page_summary`: Brief excerpt for feed cards
  - `page_cat_name`: Category display name
  - `page_cat_uuid`: Foreign key referencing Category `cat_uuid`
  - `page_author_name`: Author display name
  - `page_author_uuid`: Foreign key referencing Author `author_uuid`
  - `page_featured_image`: Main header image path or URL
  - `page_status`: Publication status (`published`, `draft`, `archived`)
  - `page_created_at`: UTC ISO-8601 creation timestamp
  - `page_updated_at`: UTC ISO-8601 update timestamp

### 2. Category (`categories.104.bejson`)
- **Primary Key**: `cat_uuid` (string, UUIDv4)
- **Prefix**: `cat_`
- **Fields**:
  - `cat_uuid`: Unique identifier
  - `cat_name`: Category title (case-insensitively deduplicated)
  - `cat_slug`: Unique URL slug
  - `cat_description`: Brief taxonomy summary
  - `cat_feed_type`: Layout archetype (`blog`, `portfolio`, `docs`, `feed`)

### 3. AuthorProfile (`authors.104.bejson`)
- **Primary Key**: `author_uuid` (string, UUIDv4)
- **Prefix**: `author_`
- **Fields**:
  - `author_uuid`: Unique identifier
  - `author_display_name`: Public author name (case-insensitively deduplicated)
  - `author_bio`: Biographical summary
  - `author_avatar_url`: Avatar image link
  - `author_contact_email`: Public email or placeholder
  - `author_social_links`: JSON or delimited social handle list

### 4. MediaAsset (`media_assets.104.bejson`)
- **Primary Key**: `asset_uuid` (string, UUIDv4)
- **Prefix**: `asset_`
- **Fields**:
  - `asset_uuid`: Unique identifier
  - `asset_filename`: Stored file basename
  - `asset_mime_type`: Content MIME type (e.g., `image/webp`, `image/png`)
  - `asset_filesize_bytes`: Integer byte count
  - `asset_sha256`: Cryptographic payload fingerprint
  - `asset_created_at`: Upload timestamp

### 5. ExternalMedia (`external_media.104.bejson`)
- **Primary Key**: `extmedia_uuid` (string, UUIDv4)
- **Prefix**: `extmedia_`
- **Fields**:
  - `extmedia_uuid`: Unique identifier
  - `extmedia_title`: Display label
  - `extmedia_url`: External resource URL (PDF, CDN video)
  - `extmedia_type`: Resource kind (`pdf`, `video`, `audio`)
  - `extmedia_created_at`: Registration timestamp

### 6. SiteConfig (`site_config.104.bejson`)
- **Primary Key**: `sys_uuid` (string, UUIDv4)
- **Prefix**: `sys_`
- **Fields**:
  - `sys_uuid`: Unique identifier
  - `sys_key`: Unique configuration setting name
  - `sys_value`: Setting value
  - `sys_description`: Context and usage documentation

### 7. NavLink (`navigation.104.bejson`)
- **Primary Key**: `nav_uuid` (string, UUIDv4)
- **Prefix**: `nav_`
- **Fields**:
  - `nav_uuid`: Unique identifier
  - `nav_label`: Display title in header/drawer
  - `nav_url`: Destination URL or relative route
  - `nav_display_order`: Integer sorting weight

### 8. Advertisement (`advertisements.104.bejson`)
- **Primary Key**: `ad_uuid` (string, UUIDv4)
- **Prefix**: `ad_`
- **Fields**:
  - `ad_uuid`: Unique identifier
  - `ad_name`: Campaign or unit descriptor
  - `ad_image_url`: Banner creative path
  - `ad_target_url`: Click-through link
  - `ad_zone`: Placement slot (`header`, `sidebar`, `footer`, `in-feed`)
  - `ad_is_active`: Boolean flag indicating active status

### 9. StandaloneApp (`standalone_apps.104.bejson`)
- **Primary Key**: `app_uuid` (string, UUIDv4)
- **Prefix**: `app_`
- **Fields**:
  - `app_uuid`: Unique identifier
  - `app_name`: Application title
  - `app_description`: Overview of mini-app functionality
  - `app_entry_path`: Relative entrypoint path (`index.html` or executable)
  - `app_image_url`: Application thumbnail
  - `app_created_at`: Creation timestamp

### 10. PersonaRecord (`personas.104.bejson`)
- **Primary Key**: `persona_uuid` (string, UUIDv4)
- **Prefix**: `persona_`
- **Fields**:
  - `persona_uuid`: Unique identifier
  - `persona_name`: Persona title
  - `persona_role`: Functional role definition
  - `persona_prompt`: System prompt instructions for AI authoring
  - `persona_author_fk`: Linked author UUID
