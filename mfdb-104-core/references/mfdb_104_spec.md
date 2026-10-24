# Reference Specification: Multi-File Database (MFDB v1.31)

> **Parent Skill:** `mfdb-104-core` (Layer 1)  
> **Source Authority:** `CRASH_COURSE_23_OFFICIAL.md` (Part 2)  
> **MFDB Spec Version:** `1.31`  
> **Format Creator:** Elton Boehnen · [https://boehnenelton2024.pages.dev](https://boehnenelton2024.pages.dev)  
> **Author Credit:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Effective Date:** October 2026  
> **RELATIONAL_ID:** `8a7d4210-9b3f-4e65-bc28-1f59e0a72d31`

---

## 1. Architectural Concept

MFDB is a multi-file database architecture layered on top of BEJSON. It does not introduce a new format version; it orchestrates BEJSON 104 and 104a formats into a cohesive relational database system:
* **The Manifest (`104a.mfdb.bejson`)**: A BEJSON 104a document located at the root of the database acting as the entity registry.
* **The Entity Files (`data/<entity_name_lowercase>.bejson`)**: Individual BEJSON 104 documents holding dense records for exactly one entity type.
* **`Parent_Hierarchy`**: Built-in exception key in each entity file containing a relative path back to the owning manifest (e.g., `"../104a.mfdb.bejson"`).

```text
mydb/
  104a.mfdb.bejson        ← manifest (root)
  data/
    user.bejson           ← entity file (BEJSON 104)
    order.bejson          ← entity file (BEJSON 104)
    product.bejson        ← entity file (BEJSON 104)
```

---

## 2. The Manifest Specification (`104a.mfdb.bejson`)

* **Mandatory Keys**:
  * `Format`: `"BEJSON"`
  * `Format_Version`: `"104a"`
  * `Format_Creator`: `"Elton Boehnen"`
  * `Records_Type`: `["mfdb"]`
* **Standard Headers (`PascalCase`)**:
  * `MFDB_Version`: `"1.31"` (Required)
  * `DB_Name`: Human-readable database name (Required)
  * `DB_Description`, `Schema_Version`, `Author`, `Created_At` (Optional)
  * `Network_Role`: `"Master"` or `"Slave"` (Federation role)
* **Required Fields**:
  * `entity_name` (`string`): Unique entity name in PascalCase (e.g. `"User"`). Cannot be `null`.
  * `file_path` (`string`): Relative path from manifest to entity (e.g. `"data/user.bejson"`). Cannot be `null`. Unique across all records.
* **Optional Standard Fields**:
  * `description` (`string`), `record_count` (`integer`), `schema_version` (`string`), `primary_key` (`string`).

---

## 3. Entity File Specification

* **Format**: Pure BEJSON 104.
* **`Records_Type`**: Exactly one string matching `entity_name` in the manifest.
* **`Parent_Hierarchy`**: Mandatory relative path back to the manifest file from the entity's own directory (`"../104a.mfdb.bejson"`).
* **Records**: Dense tabular records. Zero cross-entity null padding.

---

## 4. Discovery Algorithm

A tool encountering any `.bejson` file identifies its role natively via a 5-step file-local check:
1. Parse file as JSON. If invalid $\rightarrow$ Not MFDB.
2. Read `Format_Version` and filename.
3. If `Format_Version == "104a"` AND filename ends in `".mfdb.bejson"` $\rightarrow$ **Manifest**.
4. If `Format_Version == "104"` AND `"Parent_Hierarchy"` is present $\rightarrow$ **Entity File**.
5. Otherwise $\rightarrow$ **Standalone BEJSON**.

---

## 5. Three-Level Validation Rules & Error Codes (30–49)

| Level | Scope | Enforced Criteria |
| :--- | :--- | :--- |
| **Level 1** | **Manifest** | Valid 104a, `Records_Type == ["mfdb"]`, non-null unique `entity_name` and `file_path`, all file paths resolve on disk. |
| **Level 2** | **Entity** | Valid 104, `Parent_Hierarchy` resolves to manifest, `Records_Type` matches manifest, bidirectional path agrees. |
| **Level 3** | **Database** | Level 1 + Level 2 pass for all entities. `record_count` drift (Warning), unresolved FKs (Warning). |

### Error Code Registry (MFDB Validator):
* **30**: Not a manifest
* **31**: Not an entity file
* **32**: Manifest `Records_Type` invalid
* **33**: Entity file not found (path resolution)
* **34**: Entity name mismatch (`Records_Type` vs manifest)
* **35**: Duplicate entry (`entity_name` or `file_path`)
* **36**: Missing `Parent_Hierarchy`
* **37**: Manifest file not found
* **38**: Bidirectional path check failed
* **39**: FK unresolved (strict mode warning/error)
* **40**: Missing required field in manifest
* **41**: Null in required field

---

## 6. Master-Slave Federation (`Network_Role`)

MFDB v1.31 splits databases into tiered nodes for AI context efficiency:
* **Master Node (`Network_Role: "Master"`)**: Administrative authority holding global registries and policy distribution.
* **Slave Node (`Network_Role: "Slave"`)**: High-performance operational workspace. "Structurally blind" without hardcoded paths to Master.
* **Communication Protocols**:
  * **One-Way Push**: Slaves push distilled metrics/logs to Master polling drop-zones.
  * **Inverse Drop-Zone Polling**: Master pushes updates as BEJSON 104a docs directly into Slave directories using atomic POSIX swaps (`os.replace`).

---

## 7. Master Federation Topology & Sub-Taxonomies

As formalized in the system master architecture (`SYSTEM_MASTER_DRAFT.md`), large-scale MFDB systems structure domain persistence into a hierarchical federation:

```
system_root/
  ├── 104a.mfdb.bejson                    # Master Manifest (Network_Role: "Master")
  ├── data/                               # Master Governance Entities (BEJSON 104)
  │     ├── AppConfig.bejson              # Global constants & runtime config (app_config_)
  │     ├── Routes.bejson                 # Dynamic routing rules & regexes (route_)
  │     ├── Templates.bejson              # Presentation template registry (template_)
  │     ├── Stylesheets.bejson            # CSS token bundles & cache hashes (stylesheet_)
  │     ├── Metrics.bejson                # Write-heavy build telemetry (metric_)
  │     └── MasterKeyMap.bejson           # The Key Holder referential index (keymap_)
  ├── taxonomies/                         # Domain Sub-Taxonomies (Network_Role: "Slave")
  │     ├── pages/ (104a.mfdb.bejson + data/)
  │     ├── videos/ (104a.mfdb.bejson + data/)
  │     └── documents/ (104a.mfdb.bejson + data/)
  └── storage/mfdb/
        ├── site_master/                  # Platform Master Catalog (14 entities)
        └── pages_db/                     # Two-tier detached 104db records
```

---

## 8. MasterKeyMap: The Referential Key Holder (`keymap_`)

In federated architectures, entities in decoupled sub-taxonomies (e.g. `Video001` in `taxonomies/videos/` and `Document002` in `taxonomies/documents/`) must link without hardcoding foreign keys across disparate manifest boundaries.

The **MasterKeyMap** acts as the central referential key holder:
- `keymap_edge_identifier_key`: Unique relational link ID (e.g. `"lnk_01"`).
- `keymap_source_entity_id_fk`: Origin entity ID (e.g. `"vid_001"`).
- `keymap_source_taxonomy_type_fk`: Origin taxonomy category (`"videos"`).
- `keymap_target_entity_id_fk`: Destination entity ID (`"doc_002"` or `null`).
- `keymap_target_taxonomy_type_fk`: Destination taxonomy category (`"documents"` or `null`).
- `keymap_relational_edge_kind`: Semantic link relationship (`"companion_pdf"`, `"featured_video"`, `"route"`).
- `keymap_compiled_destination_route_path`: Fully compiled destination URL route.
- `keymap_assigned_presentation_template_fk`: Target presentation template ID (`"tmpl_video_watch"`).

---

## 9. Two-Tier Content Store Pattern (`pages_db/<uuid>.json`)

To prevent multi-megabyte prose bodies and code snippets from degrading $O(1)$ tabular scan speeds in entity tables:
1. **Tier 1 (Tabular Index)**: Lightweight metadata (`page_title`, `page_slug`, `page_cat_name`, `page_created_at`, `page_excerpt`) resides in `data/pagerecord.bejson`.
2. **Tier 2 (Detached Store)**: Deep content resides in individual `104db` records inside `storage/mfdb/pages_db/<page_uuid>.json`:
   - `Record_Type_Parent`: Header discriminator (`"PageMeta"` vs `"Content"`).
   - `html_body`: Pre-compiled sanitized HTML body.
   - `markdown_body`: Raw markdown source.
   - `source_files`: Array of code file objects `[{"filename", "code"}]`.
   - `eval_pros` / `eval_cons`: Structured evaluation bullet points.
   - `verdict_score`: Numerical rating benchmark (0.0–10.0).

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

