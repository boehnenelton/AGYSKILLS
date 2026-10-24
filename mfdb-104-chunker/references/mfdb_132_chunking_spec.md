# Reference Specification: MFDB-132 Chunked-104a Packaging & Sticky Mounts

> **Parent Skill:** `mfdb-104-chunker` (Layer 2)  
> **Source Authority:** `CRASH_COURSE_23_OFFICIAL.md` (MFDB-132 Specification)  
> **Packaging Spec Version:** `1.32` (`MFDB_CHUNK_SCHEMA_VERSION = "1.32"`)  
> **Format Creator:** Elton Boehnen · [https://boehnenelton2024.pages.dev](https://boehnenelton2024.pages.dev)  
> **Author Credit:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton  
> **Effective Date:** October 2026  
> **RELATIONAL_ID:** `3e9a71b4-2c5d-4f80-9a3b-7d0e1f48c925`

---

## 1. Overview & Architectural Role

MFDB-132 collapses an entire multi-file database—including the central root manifest (`104a.mfdb.bejson`) and all entity files (`data/*.bejson`)—into a single, portable, self-describing **Chunked-104a container** (`.mfdb132.bejson`).

It serves as the transport, distribution, and session-mounting layer without altering the underlying v1.31 disk layout when extracted into an active workspace.

---

## 2. Chunked-104a Container Schema

The packaging document is a valid BEJSON 104a document with fixed fields:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `File_Name` | `string` | Base filename (e.g. `104a.mfdb.bejson`, `user.bejson`) |
| `File_Extension` | `string` | Extension without leading dot (e.g. `bejson`, `json`) |
| `File_Content` | `string` | Serialized content (UTF-8 text or Base64 binary) |
| `File_Version` | `string` | Version of the individual file payload |
| `File_Hash` | `string` | SHA-256 hex digest of `File_Content` |
| `Relative_Path` | `string` | Path relative to DB root (e.g. `data/user.bejson`) |
| `Is_Binary` | `boolean` | Flag indicating whether content is Base64 encoded |
| `Is_Mounted` | `boolean` | Flag indicating if file is currently projected to disk |

---

## 3. Cryptographic Sticky Mount Protocol (`.mfdb132_lock`)

When mounting an MFDB-132 container via `MFDB132Archive.mount`:
1. The engine checks for a `.mfdb132_lock` file in the target workspace.
2. If `.mfdb132_lock` exists, the engine computes the SHA-256 hash of the `.mfdb132.bejson` container.
3. If current hash matches `original_hash` in `.mfdb132_lock` and the schema validates:
   $$\rightarrow$$ **Reuse existing workspace immediately (Sticky Mount)**, bypassing re-extraction.
4. If hash diverges or lock is absent:
   $$\rightarrow$$ Perform full extraction, validate Level 1 and Level 2 rules, and write an updated `.mfdb132_lock`.

---

## 4. Pre-Write Validation Gates

Before committing modifications back to the single-file `.mfdb132.bejson` container:
- Complete Level 1 (Manifest) and Level 2 (Entity) validation runs as an atomic gate.
- If any entity fails structural integrity or bidirectional path checks, the commit aborts before modifying the package archive.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
