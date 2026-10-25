---
name: behtml-scaffold-automator
description: >-
  Automate the compilation, asset localization, BECSS Tri-Color token injection, and distribution packaging for deterministic BEHTML interfaces, web documents, and 8-lane / Ry=32px UI layouts into production staging folders. Use when compiling BEHTML layouts into static distribution builds, injecting Tri-Color CSS variables, auditing HTML documents for zero-filler compliance before shipping, or staging web assets into distribution directories. Do NOT use for raw 8-lane / 32px coordinate math (use behtml-format-core), structural schema validation (use behtml-schema-validator), or UI layout composition (use behtml-layout-builder).
---

# behtml-scaffold-automator (Layer 3 Spatial Web Scaffolder & Asset Bundler)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & Linux
- **Architectural Tier**: Layer 3 (L3) Automation & Service Pipeline
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `3b4c5d6e-7f8a-9b0c-1d2e-3f4a5b6c7d8e`
- **Version**: `1.0.0`
- **Upstream Collaborators**: `behtml-layout-builder` (L4), `behtml-templates` (L4)
- **Downstream Collaborator**: `behtml-schema-validator` (L2)

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- Compiling and bundling standalone BEHTML pages and document templates into distribution folders (`dist/`).
- Injecting canonical BECSS Tri-Color CSS variables (`--bg-primary: #000000`, `--text-primary: #FFFFFF`, `--accent-red: #DE2626`) into raw template documents.
- Validating spatial quantization adherence (8-lane 12.5% columns, 16-sublane 6.25% half-cells, $R_y = 32\text{px}$ row height).
- Enforcing the global Zero-Filler Law (rejection of lorem ipsum and conversational placeholder fluff).
- Registering compiled web builds and file checksums into structured BEJSON 104a manifests.

### When NOT to Use:
- Do NOT use for raw low-level 8-lane coordinate math and schema option sets (use `behtml-format-core`).
- Do NOT use for black-box Layer 2 schema and error code validation (use `behtml-schema-validator`).
- Do NOT use for composing 18-field BEHTMLElement layout datasets (use `behtml-layout-builder`).
- Do NOT use for authoring technical blog posts (use `publication-blog-post-writer`).

---

## 2. Architectural Pipeline Role

`behtml-scaffold-automator` bridges the presentation layer (Layer 4) with the validation layer (Layer 2):

```
[Layer 4 Layout Builder / Templates]
                 |
                 v
[Layer 3 behtml-scaffold-automator (This Skill)]
    - Injects BECSS tokens & 8-lane grid CSS
    - Strips external CDNs and localizes assets
    - Verifies Zero-Filler compliance
    - Triggers behtml-schema-validator
                 |
                 v
[Layer 2 Schema Validator Gate]
                 |
                 v
[Production Output Staged in dist/]
```

---

## 3. Tool Execution via CLI

The bundling engine is driven by `scripts/behtml_bundler.py`:

### Step 1: Bundle a Single BEHTML Document
```bash
python3 scripts/behtml_bundler.py \
    src/index.html \
    --dist-dir dist/ \
    --project-name "Admin_Dashboard"
```

### Step 2: Batch Bundle Directory with Manifest Tracking
Bundle all HTML documents in a source folder and record build records in a BEJSON 104a manifest:
```bash
python3 scripts/behtml_bundler.py \
    resources/templates/ \
    --dist-dir storage/builds/ \
    --project-name "BEJSON_CMS" \
    --manifest assets/behtml_build_manifest.104a.bejson
```

---

## 4. Headless agy Execution Protocol

When invoking via Antigravity CLI, enforce `--sandbox` isolation:

```bash
agy --sandbox -p "Bundle all BEHTML documents in resources/templates/ into storage/builds/ using behtml-scaffold-automator, inject Tri-Color tokens, and verify zero-filler compliance"
```

Negative Constraints: Zero conversational filler. Do not write output files outside designated distribution directories.

---

## 5. BEJSON Manifest Integration (Format 104a)

Build records are tracked in `assets/behtml_build_manifest.104a.bejson`:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["BEHTMLBuildRecord"],
  "Fields": [
    {"name": "build_id",             "type": "string"},
    {"name": "project_name",         "type": "string"},
    {"name": "source_html_path",     "type": "string"},
    {"name": "dist_html_path",       "type": "string"},
    {"name": "total_elements",       "type": "integer"},
    {"name": "grid_system",          "type": "string"},
    {"name": "tri_color_compliant",  "type": "boolean"},
    {"name": "validation_status",    "type": "string"},
    {"name": "sha256_hash",          "type": "string"},
    {"name": "build_timestamp",      "type": "string"}
  ],
  "Values": []
}
```

In Python operations, field indices are resolved dynamically via `field_map`:
```python
field_map = {f["name"]: idx for idx, f in enumerate(doc["Fields"])}
dist_path = row[field_map["dist_html_path"]]
```
