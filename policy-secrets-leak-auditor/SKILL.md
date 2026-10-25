---
name: policy-secrets-leak-auditor
description: >-
  Audit codebases, configuration files, BEJSON caches, and session logs for unmasked API credentials, raw tokens, and private keys per Policy Section 4.5. Enforces the pointer-only persistence standard (ENV:<var_name>) before release packaging or git commits. Use when auditing repositories for exposed secrets, verifying zero-leakage credential compliance in BEJSON key caches, inspecting session logs prior to distribution, or validating pre-commit security gates. Do NOT use for static AST BEJSON field-map validation (use policy-bejson-auditor), policy conflict analysis (use policy-conflict-auditor), or single-file Flask endpoint security reviews (use adversarial-code-reviewer).
---

# policy-secrets-leak-auditor (Layer 2 Policy Section 4.5 Zero-Leakage Credential Gate)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc) & Linux
- **Architectural Tier**: Layer 2 (L2) Verification & Validation Gate
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d`
- **Version**: `1.0.0`
- **Policy Grounding**: Policy Section 4.5 (Zero-Leakage Security & Sourcing Standards)
- **Downstream Collaborator**: `project-delivery-packager` (Layer 6 Release Gate)

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- Auditing software repositories, configuration stores, and git worktrees for leaked API keys (Gemini, Groq, OpenRouter, OpenAI, GitHub, AWS, private keys).
- Verifying strict adherence to Policy Section 4.5: ensuring that all `keys*.bejson` and `config*.json` files store abstract pointers (`ENV:<var_name>`) rather than raw secret values.
- Executing a Layer 2 pre-delivery security stage gate before invoking `project-delivery-packager` or committing release ZIP archives.
- Sanitizing session transcripts (`session_*.bejson`, `session_*.md`) to ensure no bearer tokens or authorization headers leaked into conversational turns.
- Generating deterministic structured security reports with pass/fail exit codes.

### When NOT to Use:
- Do NOT use for static AST BEJSON field-map cache compliance auditing (use `policy-bejson-auditor`).
- Do NOT use for detecting logical contradictions between policy directives (use `policy-conflict-auditor`).
- Do NOT use for auditing single-file Flask endpoint routes and API logic (use `adversarial-code-reviewer`).
- Do NOT use for packaging or registering project release ZIP deliverables (use `project-delivery-packager`).

---

## 2. Security Invariants & Policy Grounding

Under Policy Section 4.5 and the NewAgent v3.45+ security model:

1. **The Pointer-Only Persistence Standard**:
   - Physical configuration files and disk caches MUST NEVER store raw secret values.
   - Values must strictly resolve to abstract pointers formatted as `ENV:<var_name>`.
   - Real secret values are loaded dynamically into volatile RAM from `/storage/emulated/0/.env/secure/secureenv_file.json` and are wiped from memory upon process termination.
2. **Deterministic Exit Codes**:
   - Exit `0`: Repository is completely clean. All configuration stores comply with pointer-only persistence.
   - Exit `1`: Unmasked credentials or non-pointer values discovered. Blocks automated release packaging.
3. **Log & Report Redaction**:
   - The scanner never logs full secret strings in plaintext; all discovered tokens are masked (`AIza...1234`).

---

## 3. Tool Execution via CLI

The secrets audit engine is driven by `scripts/secrets_leak_auditor.py`:

### Step 1: Audit an Active Repository
```bash
python3 scripts/secrets_leak_auditor.py \
    /storage/emulated/0/Admin/Dev/Repos/NewAgent \
    --output-report reports/secrets_audit.json \
    --manifest assets/secrets_audit_registry.104a.bejson
```

### Step 2: Single-File Inspection
Inspect a specific configuration cache or session export:
```bash
python3 scripts/secrets_leak_auditor.py \
    config/keys_openrouter.bejson
```

---

## 4. Headless agy Execution Protocol

When invoking via Antigravity CLI, enforce `--sandbox` isolation:

```bash
agy --sandbox -p "Audit the entire codebase in /storage/emulated/0/Admin/Dev/Repos/NewAgent for credential leaks and verify pointer-only compliance using policy-secrets-leak-auditor"
```

Negative Constraints: Zero conversational filler. Do not print unmasked secret values to stdout.

---

## 5. BEJSON Manifest Integration (Format 104a)

Audit runs are logged to `assets/secrets_audit_registry.104a.bejson`:

```json
{
  "Format": "BEJSON",
  "Format_Version": "104a",
  "Format_Creator": "Elton Boehnen",
  "Records_Type": ["SecretsAuditRecord"],
  "Fields": [
    {"name": "audit_id",                 "type": "string"},
    {"name": "target_directory",         "type": "string"},
    {"name": "scanned_files_count",      "type": "integer"},
    {"name": "leaks_detected_count",     "type": "integer"},
    {"name": "pointer_compliance_pct",   "type": "number"},
    {"name": "audit_verdict",            "type": "string"},
    {"name": "report_path",              "type": "string"},
    {"name": "audit_timestamp",          "type": "string"}
  ],
  "Values": []
}
```

In runtime operations, fields are accessed dynamically via `field_map`:
```python
field_map = {f["name"]: idx for idx, f in enumerate(doc["Fields"])}
verdict = row[field_map["audit_verdict"]]
```
