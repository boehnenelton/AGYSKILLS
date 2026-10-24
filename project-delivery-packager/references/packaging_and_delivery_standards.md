# Packaging & Delivery Protocols Reference (GEMINI.md Policy §3, §4.6, §4.7, §9)

- **Document Identifier**: `packaging_and_delivery_standards.md`
- **Skill**: [`project-delivery-packager`](../SKILL.md)
- **Version**: 100
- **Release Version**: 300
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `b94c1e2a-7f30-4e5b-91d8-3a2b5c0d1e4f`

---

## 1. Solid Numeric Versioning & Mapping Rule (Policy §3.1)

All deliverable packages must strictly adhere to the Solid Numeric Versioning specification:
1. Version numbers must be solid integers without dots in filename tokens:
   - `1.0.0` &rarr; `100`
   - `1.0.1` &rarr; `101`
   - `1.1.16` &rarr; `10116` or `1116`
2. Every modification to a deliverable payload increments the Package Version sequentially by `+1` (e.g. `PKG100` &rarr; `PKG101`).
3. Deliverable ZIP archive naming pattern:
   ```text
   (PROJECT_NAME)-V(VERSION)-PKG(PACKAGE_VERSION).zip
   Example: Bookwriter-V100-PKG101.zip
   ```

---

## 2. Dual-Version Tracking Standard (Policy §3.2)

1. **Project Version**: Tracks the application/script runtime state (e.g., `1.0.0`).
2. **Package Version**: Tracks the physical exchange/archive distribution state (e.g., `100`, `101`).
3. Both versions must be accurately reflected inside `bejson_project.json` and in script file headers.

---

## 3. Mandatory .beignore Exclusion Rules (Policy §3.4)

When bundling project directories into release ZIP deliverables, the following directories, lockfiles, and transient working caches MUST be strictly excluded:

```text
# Python bytecode & cache
__pycache__/
*.pyc
*.pyo
.pytest_cache/

# Runtime locks & temporary storage
*.lock
*.tmp
.tmp*
.bejson_*
data/temp/

# Git history & VCS artifacts
.git/
.gitignore
.gitattributes

# OS metadata
.DS_Store
Thumbs.db

# Output artifacts & previous snapshots
exports/
backups/
*.bak
```

---

## 4. Manifest Update Lifecycle & GUID Governance (Policy §4.6)

Upon executing release packaging:
1. **Strict GUID Governance**: The AI must NEVER generate or assign a global `Project_GUID` if it is missing. Retain `"GUID_PLACEHOLDER"` until assigned by dedicated registration tooling.
2. **Versioned_UUID Scope**: The AI generates and updates `Versioned_UUID` (and file-level `RELATIONAL_ID`) whenever incrementing package versions or modifying payloads.
3. **Change_Log Appending**: The changelog entry format:
   ```text
   <Project_Version> | <YYYY-MM-DD> | <Description of changes>
   ```
4. **Package_Checksum_SHA256**: The SHA-256 hash of the generated ZIP archive is calculated and written into `bejson_project.json`.

---

## 5. Master Index Registration Protocol (Policy §4.7)

After packaging, projects are registered with the central master index:
```bash
python3 $PROJECT_INDEX_ROOT/cli_project_register.py --register "$SCRIPT_PATH"
```
If `$PROJECT_INDEX_ROOT` or `cli_project_register.py` is not found, the tool logs the status and records `Is_Registered: false` without crashing.

---

*Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton*
