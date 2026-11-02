# Multi-File Database (MFDB) Format 105 Specification

> **Parent Skill:** `mfdb-105-core` (Layer 1)  
> **Release_Version:** 300 | **Era:** Integrity Era (libraries_105)  
> **Author:** Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton

---

## 1. Structural Schema Specifications

### 1.1 Manifest Document (`105a.mfdb.bejson`)
```json
{
  "Format": "BEJSON",
  "Format_Version": "105a",
  "Format_Creator": "Elton Boehnen",
  "MFDB_Version": "1.40",
  "Network_Role": "Master",
  "DB_Name": "ENTERPRISE_CORE",
  "Schema_Version": "1.0.0",
  "Author": "Elton Boehnen",
  "Created_At": "2026-11-02T00:00:00Z",
  "Records_Type": ["mfdb"],
  "Fields": [
    {"name": "entity_name", "type": "string", "field_uuid": "f1010001-0000-4000-8000-000000000001"},
    {"name": "file_path", "type": "string", "field_uuid": "f1010001-0000-4000-8000-000000000002"},
    {"name": "description", "type": "string", "field_uuid": "f1010001-0000-4000-8000-000000000003"},
    {"name": "record_count", "type": "integer", "field_uuid": "f1010001-0000-4000-8000-000000000004"},
    {"name": "table_sha256", "type": "string", "field_uuid": "f1010001-0000-4000-8000-000000000005"},
    {"name": "primary_key", "type": "string", "field_uuid": "f1010001-0000-4000-8000-000000000006"}
  ],
  "Values": []
}
```

### 1.2 Entity Table Document (`data/<entity>.105.bejson`)
```json
{
  "Format": "BEJSON",
  "Format_Version": "105",
  "Format_Creator": "Elton Boehnen",
  "Parent_Hierarchy": "../105a.mfdb.bejson",
  "Network_Role": "Slave",
  "Records_Type": ["UserEntity"],
  "Fields": [
    {"name": "record_uuid", "type": "string", "field_uuid": "f2020002-0000-4000-8000-000000000001"},
    {"name": "usr_username", "type": "string", "field_uuid": "f2020002-0000-4000-8000-000000000002"},
    {"name": "usr_role", "type": "string", "field_uuid": "f2020002-0000-4000-8000-000000000003"},
    {"name": "usr_created_at", "type": "string", "field_uuid": "f2020002-0000-4000-8000-000000000004"}
  ],
  "Values": []
}
```

---

## 2. Cryptographic Checksum Recalculation

When rows are appended or mutated in an entity table:
1. Every row $r_i$ computes:
   $$\text{Checksum}(r_i) = \text{SHA256}\left(\sum_{j=0}^{k-1} \text{SanitizeStr}(r_i[j])\right)$$
2. The entity table hash is recomputed as:
   $$\text{TableDigest} = \text{SHA256}(\text{HeaderCanonicalBytes} \mathbin{\Vert} \text{RowChecksums})$$
3. The parent manifest's row corresponding to this entity updates:
   - `record_count` $\to \text{len}(\mathcal{V})$
   - `table_sha256` $\to \text{TableDigest}$
