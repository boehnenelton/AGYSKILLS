# Policy §10.6 Enforcement Testing & §10.7 Lifecycle Parity Standards

- **Document Identifier**: `enforcement_testing_standards.md`
- **Skill**: [`bejson-enforcement-suite-builder`](../SKILL.md)
- **Version**: 100
- **Release Version**: 300
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `c81d2f3e-4b5a-4960-8e2b-1a3c5d7f9e01`

---

## 1. Mandatory 5-Test Enforcement Suite (Policy §10.6)

Projects with a BEJSON schema registry (`schema_registry.104a.bejson` or `src/lib/lib_<Family>_taxonomy.py`) MUST implement five runtime test gates:

### Test 1: Conformance Test
- **Mandate**: Build fails on non-registry field names.
- **Verification Logic**: Passing records with unrecognized field names (e.g., `unregistered_field`) directly to an entity writer or validator must be rejected. Zero raw, unregistered keys may enter the database.

### Test 2: Manifest Integrity Test
- **Mandate**: Verifies primary keys, record counts, and field definitions.
- **Verification Logic**: Asserts that every registered entity defines exactly one immutable UUID primary key (`<entity>_uuid` or `<entity>_id`), that all field definitions match registered types (`string`, `number`, `boolean`, `any`), and that manifest counts match record counts.

### Test 3: Round-Trip Test
- **Mandate**: Write &rarr; Read Back &rarr; Verify on all read paths.
- **Verification Logic**: Generates synthetic records, writes them via owning writers, queries them back using dynamic $O(1)$ `field_map` resolution, and confirms that read values match written values verbatim with zero data truncation or loss.

### Test 4: Lifecycle Smoke Test
- **Mandate**: Reset &rarr; Create &rarr; Verify in all pickers/lists.
- **Verification Logic**: Executes a system reset, constructs a new record, and verifies that UI pickers, CLI menus, and query iterators immediately recognize and present the new entity.

### Test 5: Post-Reset Test
- **Mandate**: Zero null rows, zero duplicate hashes, exact seed count.
- **Verification Logic**: Runs factory reset, inspects the raw `Values` matrix across all entity stores, asserting:
  1. No row is `None` / `null`.
  2. Every row length equals `len(Fields)`.
  3. No duplicate primary key hashes exist.
  4. Record count matches the declared seed specification.

---

## 2. Lifecycle Parity Protocol (Policy §10.7)

1. **One Factory-Reset Routine**: Every project must expose a single unified factory reset routine (`execute_factory_reset()` in `reset_harness.py`).
2. **Unified Entry Points**: CLI `--reset`, web UI Reset buttons, and test runners must call the exact same reset routine. Divergent reset logic across entry points is strictly prohibited.
3. **Owning Writer Exclusivity**: Reseeding must utilize canonical owning writers (§10.4) rather than hand-rolled inserts.

---

*Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton*
