# Naming Conventions and Taxonomy Heuristics

This reference guide establishes the architectural standards for codebase variable naming and entity taxonomy design per Policy §6.1, §10.1, §10.2, §10.3, and §10.4.

---

## 1. Long Self-Describing Variable Standard (Policy §6.1)

All application code, scripts, and templates must employ long, self-describing variable identifiers that communicate semantic meaning without ambiguity.

### 1.1 The Hierarchy-Group-Purpose Triad Formula

$$\text{VariableName} = \langle\text{hierarchy\_or\_scope}\rangle\_\langle\text{group\_or\_domain}\rangle\_\langle\text{purpose\_or\_role}\rangle$$

1. **Hierarchy / Scope**: Architectural level, container, or parent scope.
   - Examples: `session_`, `manifest_`, `table_row_`, `canvas_`, `audit_`, `config_`.
2. **Group / Domain**: Component, domain entity, or library subsystem.
   - Examples: `entity_record_`, `field_map_`, `finding_entry_`, `telemetry_stream_`.
3. **Purpose / Semantic Role**: Specific data payload, operational unit, or flag.
   - Examples: `_count_metric`, `_is_active_flag`, `_lookup_cache`, `_file_path`, `_summary_text`.

### 1.2 Prohibited Naming Anti-Patterns
- **Single-Letter Variables**: `i`, `j`, `k`, `x`, `y`, `d`, `p`, `r`, `n`, `c` (forbidden in application logic and loops; use `column_index`, `row_counter`, `coordinate_x_px`).
- **Abbreviated / Cryptic Variables**: `tmp`, `val`, `res`, `arr`, `obj`, `item`, `data`, `rec`, `col`, `row`, `elem` (prohibited; replace with `temporary_buffer_text`, `entity_row_payload`).
- **Vague Functions**: `process()`, `handle()`, `run_all()`, `do_stuff()`, `work()`.

---

## 2. Entity Prefixing & Taxonomy Standard (Policy §10.1 - §10.4)

### 2.1 Entity Field Snake-Case Prefixes
Schema fields should always carry an explicit snake_case entity prefix:
- **Non-Compliant (Naked Fields)**:
  - `id`, `name`, `status`, `created_at`, `email`
- **Compliant (Entity-Prefixed Fields)**:
  - `user_id`, `user_display_name`, `user_account_status`, `user_created_at_iso`, `user_email_address`

### 2.2 Foreign Key Conventions (`_fk`)
Foreign key references across entity models must specify the target entity followed by `_fk`:
- Example: `tenant_account_fk`, `project_owner_fk`, `manifest_batch_fk`.
- Cross-entity relationships must declare explicit on-delete behavior (`cascade`, `null`, `default`, `restrict`).

### 2.3 Write-Owner Module Isolation (Policy §10.4)
Every BEJSON entity schema must have exactly one designated Write-Owner module (e.g., `src/data/user_account_writer.py`). Any upper-layer service wishing to mutate that entity must call the Write-Owner module rather than performing uncoordinated atomic writes directly.

---

Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
