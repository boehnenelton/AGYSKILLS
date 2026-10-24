# Subfolder Architecture & Tracking Migration Specification

* System: Layer 3 Scaffolding & Architecture
* Policy Grounding: GEMINI.md — §1.1, §1.3, §4.1/§4.2, §4.4
* Component: `file-subfolder-automator`
* CLI Tool: `scripts/scaffold_subfolder_architecture.py`
* Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
* Date Created: 2026-10-22

---

## 1. Policy §1.1 Standardized Subfolder Architecture

All scripts and projects must operate portably and relatively from their own `$SCRIPT_PATH`, keeping project root directories clean by organizing components into standardized subdirectories:

| Subdirectory | Canonical Purpose | Policy Mandate |
| :--- | :--- | :--- |
| **`lib/`** | Local script dependencies and vendor libraries. | Policy §1.1, §4.3 |
| **`config/`** | BEJSON 104a configuration files (`config.json`). | Policy §1.1, §4.4 |
| **`data/`** | Local persistent records, working stores, runtime caches. | Policy §1.1 |
| **`exports/`** | Generated output artifacts, reports, exports. | Policy §1.1 |
| **`backups/`** | Snapshots, rollbacks, automated file backups. | Policy §1.1 |
| **`dev/`** | Active development tracking notes (`dead_code.md`, `variable_naming_issues.md`, `security-notes.md`). | Policy §1.1, §1.3 |
| **`docs/`** | Technical overviews (`technical_overview.md`) and architectural maps. | Policy §1.1, §1.3 |

---

## 2. Policy §1.3 Tracking File Migration Protocol

Policy §1.3 mandates:
> **Folder Migration**: If tracking files (`dead_code.md`, `variable_naming_issues.md`, `security-notes.md`) exist in `docs/`, move them to `dev/` upon directory creation and continue in `dev/`.

### Migration Logic:
1. If `docs/<file>.md` exists, move it atomically to `dev/<file>.md`.
2. If `dev/<file>.md` is missing, instantiate an initial tracking table skeleton.
3. Keep `docs/` reserved exclusively for `technical_overview.md` and user-facing architectural documentation.

---

## 3. Policy §1.3 Technical Overview Formatting

Function signatures in `docs/technical_overview.md` must follow the format:
```text
File_Name / Function_Name (var1, var2, var3)
```

The embedded tool automatically parses the project's root Python AST to discover function definitions, parameter lists, and class identifiers to populate this document.

---

## 4. Policy §4.1 / §4.2 Self-Locating Preambles

Every generated or modified script must declare a self-locating path resolution function:

### Python (Policy §4.1):
```python
from pathlib import Path

def get_script_path() -> Path:
    return Path(__file__).resolve().parent

SCRIPT_PATH = get_script_path()
```

### Bash (Policy §4.2):
```bash
get_script_path() {
    local source="${BASH_SOURCE[0]}"
    while [ -h "$source" ]; do
        local dir="$( cd -P "$( dirname "$source" )" >/dev/null 2>&1 && pwd )"
        source="$(readlink "$source")"
        [[ $source != /* ]] && source="$dir/$source"
    done
    echo "$( cd -P "$( dirname "$source" )" >/dev/null 2>&1 && pwd )"
}
SCRIPT_PATH=$(get_script_path)
```
