# Multi-MFDB Error Code Taxonomy (E30-E39)

> **Parent Skill:** `mfdb-schema-validator` (Layer 2)  
> **Release_Version:** 300 | **Format:** Reference Manual  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## Complete Error Code Specification

| Code | Constant | Category | Description & Strict Remediation Protocol |
| :--- | :--- | :--- | :--- |
| **`E30`** | `E_MFDB_MISSING_MANIFEST` | Manifest | Manifest file `104a.mfdb.bejson` or `105a.mfdb.bejson` does not exist at the target path. |
| **`E31`** | `E_MFDB_INVALID_FORMAT_VERSION` | Format | Format string is not `BEJSON` or format version is not in `['104', '104a', '104db', '105', '105a', '105db']`. |
| **`E32`** | `E_MFDB_MISSING_RECORDS_TYPE` | Manifest | Root JSON object lacks a non-empty `Records_Type` array. |
| **`E33`** | `E_MFDB_MISSING_FIELDS` | Schema | Header is missing the canonical `Fields` schema array. |
| **`E34`** | `E_MFDB_MISSING_VALUES` | Data | Payload is missing the `Values` tabular matrix. |
| **`E35`** | `E_MFDB_UNRESOLVED_PARENT_HIERARCHY` | Linkage | Entity's `Parent_Hierarchy` cannot be resolved on disk, or resolves to a manifest that does not register this entity. |
| **`E36`** | `E_MFDB_CYCLIC_DEPENDENCY` | Topology | Circular parent-child linkage detected ($A \to B \to C \to A$) via DFS DAG traversal. |
| **`E37`** | `E_MFDB_NETWORK_ROLE_MISMATCH` | Topology | Contradictory role declaration (e.g. entity declares `Network_Role: "Master"` while registered as a `Slave`). |
| **`E38`** | `E_MFDB_UNREGISTERED_ENTITY` | Partition | An entity `.bejson` file exists inside the database directory on disk but is omitted from the manifest's `Values`. |
| **`E39`** | `E_MFDB_UNRESOLVED_FK` | Relational | A foreign key pointer references a target entity or primary key UUID that does not exist in the referenced table. |
