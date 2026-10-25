---
name: bejson-tui-menu-builder
description: >-
  Build high-density 57-column terminal user interfaces (TUIs) and daemon status menus enforcing the BEJSON Positional Telemetry Discipline: strict separation of schema Fields from positional Values, zero JSON-style inline key repetition, single-source telemetry strips, decoupled 3-column action hotkeys (max 18 chars), and fixed-width printf rendering. Use when designing, auditing, or refactoring interactive Bash terminal menus, CLI daemon dashboards, or Termux portrait-mode TUIs. Do NOT use for rendering tabular BEHTML web views (use behtml-104-builder), instantiating full BEHTML web documents (use behtml-document-template), or mutating BEJSON data records on disk (use bejson-104-core).
---

# Skill: `bejson-tui-menu-builder` (Layer 4 Presentation)

- **Purpose**: High-density 57-column terminal interface and daemon status menu design enforcing the BEJSON Positional Telemetry Discipline.
- **Embedded Script**: `scripts/render_bejson_tui.sh`
- **Reference Spec**: `references/bejson_positional_telemetry_discipline.md`
- **Primary Runtime**: Bash (Termux / Linux POSIX) / Python 3.10+
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `3e68a063-6f03-4c16-b2a8-b86060fbe830`
- **Version**: `1.0.0`

---

## Summary

`bejson-tui-menu-builder` eliminates visual entropy in terminal interfaces by applying the core architectural insight of BEJSON (104 / 104a) - the strict separation of schema `Fields` from positional `Values` - directly to terminal screens. It establishes a hard 57-column viewport ceiling tailored for mobile portrait Termux displays, strips away redundant multi-line prose, decouples dynamic runtime state from hotkey button labels, and formats telemetry into high-density positional strips via fixed-width `printf` engines.

## When to Use

- Designing new interactive CLI daemons, status dashboards, and terminal control menus.
- Refactoring legacy menus that suffer from 70-110 column line wrapping on mobile portrait Termux.
- Eliminating repetitive `Key: Value |` inline serialization overhead across process and record tables.
- Building 3-column action hotkey grids with decoupled labels (max 18-19 chars per column).
- Auditing daemon menus against the Domain Completeness Checklist (Discovery, Overrides, Verification, Ordering, Lifecycle).

## When NOT to Use

- Building or styling browser-based tabular HTML templates or web CMS views (use `behtml-104-builder`).
- Instantiating full-canvas standalone web documents or publication specifications (use `behtml-document-template`).
- Directly inserting, updating, or validating `.104.bejson` records on disk (use `bejson-104-core`).
- Validating schema structural constraints against E01-E12 errors (use `bejson-104-validator`).
- Generating single-file flat text archives of projects (use `chunking-core`).

---

## 1. Theoretical Foundation: The BEJSON Separation Law in Text

Standard JSON repeats every key identifier inside every object record. In terminal menus, ad-hoc inline printing mimics this JSON anti-pattern:
```text
PID: 13319 | Scan: 5s | GPS: 30s | Mode: termux
```
Repeating labels on every row scales overhead linearly: $O(N \times K)$, where $N$ is row count and $K$ is field count.

The **BEJSON Separation Law** decouples the static **Field Header Strip** ($O(K)$ rendered once) from compact **Positional Value Rows** ($O(1)$ overhead per row). Applying this law packs 8 daemon metrics and 4 network state attributes into under 56 columns with zero wrapping:

```text
 PID    PORT  STATE        MODE    SCAN  GPS   ROWS  FIX
 13319  8080  PAUSED(WEB)  termux  5s    30s   0     --
```

---

## 2. The Five Pillars of the Discipline

| Pillar | Problem Eliminated | Architectural Rule |
| :--- | :--- | :--- |
| **1. BEJSON Key/Value Separation** | Repeating `Key: Value \|` labels on every line | Declare uppercase `Fields` once per strip; align `Values` positionally underneath via deterministic `printf` widths. |
| **2. 57-Column Viewport Ceiling** | 70-110 char lines wrapping jaggedly on mobile portrait screens | Cap all dividers (`===` / `---`), headers, and data rows at <= 57 columns (`70 - 13` reduction). |
| **3. Single-Source Telemetry** | Repeating connection state in headers, status banners, prose sentences, and buttons | Display each metric exactly once in dedicated top telemetry strips; eliminate explanatory prose paragraphs. |
| **4. Hotkey Label Decoupling** | Stuffing `(5s)`, `(30s)`, `(true)`, `(termux)` into button text | Keep hotkeys strictly to concise `[K] Verb Noun` actions (max 18 chars) to unlock a balanced 3-column grid. |
| **5. Operational Control Parity** | Forcing manual typing or dropping to shell for common overrides | Ensure every daemon TUI covers Discovery (`[W]`), Override (`[C]`/`[X]`/`[F]`), Ordering (`[R]`), Probe (`[B]`), and Lifecycle (`[E]`/`[Q]`). |

---

## 3. Standard Layout Blueprint (57 Columns)

```text
=========================================================
 WI-FI + GPS DAEMON [104a]   ~/.../wifi_allowlist.bejson
---------------------------------------------------------
 PID    PORT  STATE        MODE    SCAN  GPS   ROWS  FIX
 13319  8080  PAUSED(WEB)  termux  5s    30s   0     --
---------------------------------------------------------
 LINK   IP_ADDR          RSSI    SSID
 UP     10.183.119.245   -58dBm  Lowes-Guest-WiFi
---------------------------------------------------------
 ID  PRI  AUTO  SECURITY  BSSID              SSID
 01  1    Y     WPA2      a4:2b:8c:11:09:f0  Home-5G
 02  2    Y     OPEN      *                  Lowes-Guest
 03  3    N     WPA3      7c:10:c9:44:22:10  Phone-Hotsp
=========================================================
 [W] Scan & Pick AP   [A] Add Manual   [D] Delete Row
 [C] Connect Now      [X] Disconnect   [R] Priority Ord
 [F] Force GPS+Scan   [S] Scan Timer   [G] GPS Interval
 [T] Auto-Connect     [P] PauseOnWeb   [M] Mode Cycle
 [B] Portal Probe     [E] Export 104a  [Q] Quit & Kill
=========================================================
Action (5s refresh) >
```

---

## 4. Reference Implementation Pattern (printf Engine)

Always render strips using fixed-width `printf` formats to guarantee columns never drift when string lengths fluctuate:

```bash
#!/usr/bin/env bash
DIV_MAIN="========================================================="
DIV_SUB="---------------------------------------------------------"

render_bejson_tui() {
    local pid="${1:-13319}"
    local port="${2:-8080}"
    local state="${3:-PAUSED(WEB)}"
    local mode="${4:-termux}"
    local scan="${5:-5s}"
    local gps="${6:-30s}"
    local rows="${7:-0}"
    local fix="${8:---}"
    local link="${9:-UP}"
    local ip="${10:-10.183.119.245}"
    local rssi="${11:--58dBm}"
    local ssid="${12:-Lowes-Guest-WiFi}"

    printf "%s\n" "$DIV_MAIN"
    printf " %-27s %27s\n" "WI-FI + GPS DAEMON [104a]" "~/.../wifi_allowlist.bejson"
    printf "%s\n" "$DIV_SUB"

    # Strip 1: Daemon Telemetry (Fields -> Values)
    printf " %-6s %-5s %-12s %-7s %-5s %-5s %-5s %-3s\n" \
        "PID" "PORT" "STATE" "MODE" "SCAN" "GPS" "ROWS" "FIX"
    printf " %-6s %-5s %-12.12s %-7.7s %-5s %-5s %-5s %-3s\n" \
        "$pid" "$port" "$state" "$mode" "$scan" "$gps" "$rows" "$fix"
    printf "%s\n" "$DIV_SUB"

    # Strip 2: Active Network Telemetry (Fields -> Values)
    printf " %-6s %-16s %-7s %-23s\n" "LINK" "IP_ADDR" "RSSI" "SSID"
    printf " %-6s %-16.16s %-7s %-23.23s\n" "$link" "$ip" "$rssi" "$ssid"
    printf "%s\n" "$DIV_SUB"

    # Strip 3: Allowlist Records (Fields -> Positional Values)
    printf " %-3s %-4s %-5s %-9s %-18s %-11s\n" \
        "ID" "PRI" "AUTO" "SECURITY" "BSSID" "SSID"
    if [[ "$rows" -eq 0 ]]; then
        printf " %s\n" "[0 rows - press [W] to scan & pick or [A] to add SSID]"
    fi

    printf "%s\n" "$DIV_MAIN"
    # Strip 4: 3-Column Action Grid (19 + 18 + 18 = 55 chars + leading space)
    printf " %-19s %-18s %-18s\n" "[W] Scan & Pick AP" "[A] Add Manual"   "[D] Delete Row"
    printf " %-19s %-18s %-18s\n" "[C] Connect Now"    "[X] Disconnect"   "[R] Priority Ord"
    printf " %-19s %-18s %-18s\n" "[F] Force GPS+Scan" "[S] Scan Timer"   "[G] GPS Interval"
    printf " %-19s %-18s %-18s\n" "[T] Auto-Connect"   "[P] PauseOnWeb"   "[M] Mode Cycle"
    printf " %-19s %-18s %-18s\n" "[B] Portal Probe"   "[E] Export 104a"  "[Q] Quit & Kill"
    printf "%s\n" "$DIV_MAIN"
}
```

---

## 5. Domain Completeness Checklist for Daemon Menus

When designing or auditing an interactive daemon menu, verify that the hotkey grid covers these five operational failure modes:

1. **Zero-Typing Discovery (`[W] Scan & Pick AP`)**: Never make manual string typing (`[A]`) the primary workflow on mobile terminals when the daemon can scan and present indexed numbered options (`1..9`) to choose from.
2. **State Lock Override (`[C] Connect Now`, `[X] Disconnect`, `[F] Force GPS+Scan`)**: Paused or timer-blocked daemons must allow manual execution of core routines without requiring timer adjustments or global flag toggles first.
3. **Captive Portal Verification (`[B] Portal Probe`)**: In network automation, local IP assignment occurs behind unauthenticated portals. An explicit HTTP 204 probe prevents entering false connected states when WAN access is blocked.
4. **Deterministic Contention Resolution (`[R] Priority Order`)**: Multi-entry allowlists require priority ranks (`PRI`) and optional `BSSID` locks so the daemon picks the highest-value AP when multiple known networks are in range.
5. **Clean Process Lifecycle (`[Q] Quit & Kill`, `[E] Export 104a`)**: Expose the active `PID` and `PORT` in top telemetry, and guarantee quitting reaps child processes while cleanly flushing `.104a.bejson` state to disk.
