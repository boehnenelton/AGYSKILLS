---
name: bejson-tui-menu-builder
description: >-
  Build high-density 57-column terminal user interfaces (TUIs) and daemon status menus enforcing the BEJSON Positional Telemetry Discipline: strict separation of schema Fields from positional Values, #DE2626 (RGB 222,38,38) or ANSI Red coloring on menu headers, field labels, and menu option numbers/hotkeys, zero JSON-style inline key repetition, single-source telemetry strips, decoupled 3-column action options (max 18 chars), and fixed-width printf rendering. Use when designing, auditing, or refactoring interactive Bash terminal menus, CLI daemon dashboards, or Termux portrait-mode TUIs. Do NOT use for rendering tabular BEHTML web views (use behtml-104-builder), instantiating full BEHTML web documents (use behtml-document-template), or mutating BEJSON data records on disk (use bejson-104-core).
---

# Skill: `bejson-tui-menu-builder` (Layer 4 Presentation)

- **Purpose**: High-density 57-column terminal interface and daemon status menu design enforcing the BEJSON Positional Telemetry Discipline and Policy §8.1 `#DE2626` / Red accent coloring.
- **Embedded Scripts**: `scripts/render_bejson_tui.sh` (Bash), `scripts/render_bejson_tui.py` (Python 3.10+)
- **Reference Spec**: `references/bejson_positional_telemetry_discipline.md`
- **Primary Runtime**: Bash (Termux / Linux POSIX) / Python 3.10+
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `53907437-ed56-437b-ad13-9100ac636d9b`
- **Version**: `1.1.0`

---

## Summary

`bejson-tui-menu-builder` eliminates visual entropy in terminal interfaces by applying the core architectural insight of BEJSON (104 / 104a) - the strict separation of schema `Fields` from positional `Values` - directly to terminal screens. It establishes a hard 57-column viewport ceiling tailored for mobile portrait Termux displays, clears the terminal console (`\033[2J\033[H`) before loading or refreshing any TUI menu, applies Policy §8.1 `#DE2626` (Truecolor RGB `222,38,38` or ANSI Red fallback) strictly to **menu headers**, **field/prompt labels**, and **numbers/keys in menu options**, strips away redundant multi-line prose, decouples dynamic runtime state from option labels, and formats telemetry into high-density positional strips via fixed-width `printf` engines.

## When to Use

- Designing new interactive CLI daemons, status dashboards, and terminal control menus.
- Ensuring TUI menus clear the console (`\033[2J\033[H`) before loading or re-rendering frames so previous terminal output never stacks or scrolls into the active dashboard.
- Styling terminal menu headers, uppercase `Fields` labels, and numbered/hotkey menu option selectors in `#DE2626` (`\033[38;2;222;38;38m`) or ANSI Red (`\033[1;31m`) without breaking fixed-width `printf` column alignment.
- Refactoring legacy menus that suffer from 70-110 column line wrapping on mobile portrait Termux.
- Eliminating repetitive `Key: Value |` inline serialization overhead across process and record tables.
- Building 3-column numbered (`[1]..[9]`) or hotkey (`[K]`) action grids with decoupled labels (max 18-19 chars per column).
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

The **BEJSON Separation Law** decouples the static **Field Header Strip** ($O(K)$ rendered once in `#DE2626` / Red) from compact **Positional Value Rows** ($O(1)$ overhead per row rendered in default White). Applying this law packs 8 daemon metrics and 4 network state attributes into under 56 columns with zero wrapping:

```text
 PID    PORT  STATE        MODE    SCAN  GPS   ROWS  FIX   <-- Colored #DE2626 / RED
 13319  8080  PAUSED(WEB)  termux  5s    30s   0     --    <-- Default / White
```

---

## 2. The Nine Pillars of the Discipline

| Pillar | Problem Eliminated | Architectural Rule |
| :--- | :--- | :--- |
| **1. BEJSON Key/Value Separation** | Repeating `Key: Value \|` labels on every line | Declare uppercase `Fields` once per strip; align `Values` positionally underneath via deterministic `printf` widths. |
| **2. 57-Column Viewport Ceiling** | 70-110 char lines wrapping jaggedly on mobile portrait screens | Cap all dividers (`===` / `---`), headers, and data rows at <= 57 columns (`70 - 13` reduction). |
| **3. Single-Source Telemetry** | Repeating connection state in headers, status banners, prose sentences, and buttons | Display each metric exactly once in dedicated top telemetry strips; eliminate explanatory prose paragraphs. |
| **4. Option Label Decoupling** | Stuffing `(5s)`, `(30s)`, `(true)`, `(termux)` into button text | Keep menu options strictly to concise `[#] Verb Noun` or `[K] Verb Noun` actions (max 18 chars) to unlock a balanced 3-column grid. |
| **5. Operational Control Parity** | Forcing manual typing or dropping to shell for common overrides | Ensure every daemon TUI covers Discovery (`[1]`/`[W]`), Override (`[4]`/`[C]`, `[5]`/`[X]`, `[7]`/`[F]`), Ordering (`[6]`/`[R]`), Probe (`[13]`/`[B]`), and Lifecycle (`[14]`/`[E]`, `[15]`/`[Q]`). |
| **6. `#DE2626` / Red Tri-Color Hierarchy** | Monotone text walls or misaligned ANSI escape padding in `printf` | Color **menu headers**, **field/prompt labels**, and **the number/key inside menu options** in `#DE2626` (`\033[38;2;222;38;38m`) or ANSI Red (`\033[1;31m`). Keep `Values`, dividers, and option action text uncolored/white. Inject ANSI codes inside the `printf` format string (never inside padded string arguments) so column widths never drift. |
| **7. Pre-Render Console Clear** | Stale menu frames and command output stacking vertically on screen | Always clear the terminal screen and home the cursor (`printf '\033[2J\033[H'` or `clear`) immediately before rendering any TUI menu frame. |
| **8. Terminal State Lifecycle & Traps** | Broken cursor visibility or non-echoing terminal state after SIGINT/SIGTERM | Bind POSIX signal handlers (`trap 'cleanup' EXIT INT TERM`) to guarantee cursor restoration (`\033[?25h`) and standard tty echo (`stty echo`). |
| **9. Clamped Status & Alert Strips** | Ad-hoc error messages breaking column boundaries or scrolling off-screen | Provide a single-line alert strip bounded at 57 columns displaying status levels (`[✓]`, `[!]`, `[✗]`, `[*]`) in `#DE2626`. |

---

## 3. Terminal Color & Console Clear Specification (`#DE2626` & ANSI Red Fallback)

To comply with Policy §8.1 Tri-Color branding in terminal environments without breaking fixed-width `printf` padding:

| Token | Escape Sequence | Target Elements |
| :--- | :--- | :--- |
| **Console Clear (`tui_console_clear_seq`)** | `\033[2J\033[H` | Executed at the start of every menu render (`clear_tui_console`) so the menu always loads on a clean screen at row 1, col 1. |
| **Primary Truecolor (`#DE2626`)** | `\033[38;2;222;38;38m` | Menu Headers (`WI-FI + GPS DAEMON [104a]`), Field Label Strips (`PID PORT ...`), Prompt Label (`Action >`), and Option Numbers/Keys (`1`..`15` or `W`, `A`, `D` inside `[...]`). |
| **Fallback ANSI Red** | `\033[1;31m` | Used when `TUI_COLOR_MODE=ansi` or on legacy 16-color terminals lacking 24-bit `truecolor`. |
| **Reset (`CLR_RESET`)** | `\033[0m` | Immediately follows every colored header, label strip, or option number so dividers, positional `Values`, brackets `[...]`, and option descriptions remain clean white/default. |

### The `printf` Zero-Drift Coloring Rule
Never concatenate ANSI color sequences into a variable before passing it to `printf "%-18s"`, because `printf` counts invisible escape bytes toward the field width and shifts subsequent columns out of alignment. Instead:
- **Menu Header**: `printf " ${tui_color_accent_red}%-27s${tui_color_style_reset} %27s\n" "$header_title" "$file_path"`
- **Field Label Row**: `printf "${tui_color_accent_red} %-6s %-5s ...${tui_color_style_reset}\n" "PID" "PORT" ...`
- **Menu Option Row (Colored Number / Key)**: Format the bracketed number/key separately from the text width specifier:
  `printf " [%b%s%b] %-15s [%b%s%b] %-14s [%b%s%b] %-13s\n" "$tui_color_accent_red" "1" "$tui_color_style_reset" "Scan & Pick AP" ...`

---

## 4. Standard Layout Blueprint (57 Columns)

```text
=========================================================
 WI-FI + GPS DAEMON [104a]   ~/.../wifi_allowlist.bejson   <-- Header Title in #DE2626 / RED
---------------------------------------------------------
 PID    PORT  STATE        MODE    SCAN  GPS   ROWS  FIX   <-- Field Labels in #DE2626 / RED
 13319  8080  PAUSED(WEB)  termux  5s    30s   0     --
---------------------------------------------------------
 LINK   IP_ADDR          RSSI    SSID                      <-- Field Labels in #DE2626 / RED
 UP     10.183.119.245   -58dBm  Lowes-Guest-WiFi
---------------------------------------------------------
 ID  PRI  AUTO  SECURITY  BSSID              SSID          <-- Field Labels in #DE2626 / RED
 01  1    Y     WPA2      a4:2b:8c:11:09:f0  Home-5G
 02  2    Y     OPEN      *                  Lowes-Guest
 03  3    N     WPA3      7c:10:c9:44:22:10  Phone-Hotsp
=========================================================
 [1] Scan & Pick AP   [2] Add Manual   [3] Delete Row      <-- Option Numbers/Keys (1..9 / A..Q)
 [4] Connect Now      [5] Disconnect   [6] Priority Ord        colored #DE2626 / RED; brackets
 [7] Force GPS+Scan   [8] Scan Timer   [9] GPS Interval        and option text remain default
 [T] Auto-Connect     [P] PauseOnWeb   [M] Mode Cycle
 [B] Portal Probe     [E] Export 104a  [Q] Quit & Kill
=========================================================
Action (5s refresh) >                                      <-- Prompt Label in #DE2626 / RED
```

---

## 5. Reference Implementation Pattern (printf Engine with Pre-Render Clear & `#DE2626` / Red)

Always clear the console before rendering and format strips using fixed-width `printf` formats with ANSI escapes placed outside width specifiers so columns never drift:

```bash
#!/usr/bin/env bash
VERSION="102"
tui_divider_main_line="========================================================="
tui_divider_sub_line="---------------------------------------------------------"

# Policy §8.1 Accent: #DE2626 (Truecolor RGB 222,38,38) with standard ANSI Red fallback
tui_color_accent_red_hex=$'\033[38;2;222;38;38m'
tui_color_accent_red_ansi=$'\033[1;31m'
if [[ "${TUI_COLOR_MODE:-truecolor}" == "ansi" ]]; then
    tui_color_accent_red="$tui_color_accent_red_ansi"
else
    tui_color_accent_red="$tui_color_accent_red_hex"
fi
tui_color_style_reset=$'\033[0m'
tui_console_clear_seq=$'\033[2J\033[H'

clear_tui_console() {
    if [[ "${TUI_NO_CLEAR:-0}" != "1" ]]; then
        printf "%b" "$tui_console_clear_seq"
    fi
}

render_bejson_tui_option_row() {
    local row_col1_option_key="$1"
    local row_col1_option_text="$2"
    local row_col2_option_key="$3"
    local row_col2_option_text="$4"
    local row_col3_option_key="$5"
    local row_col3_option_text="$6"

    # 3-Column Action Grid: [K] (3 visible chars) + space + padded text (15 / 14 / 13 chars) = 57 visible chars exact
    printf " [%b%s%b] %-15s [%b%s%b] %-14s [%b%s%b] %-13s\n" \
        "$tui_color_accent_red" "$row_col1_option_key" "$tui_color_style_reset" "$row_col1_option_text" \
        "$tui_color_accent_red" "$row_col2_option_key" "$tui_color_style_reset" "$row_col2_option_text" \
        "$tui_color_accent_red" "$row_col3_option_key" "$tui_color_style_reset" "$row_col3_option_text"
}

render_bejson_tui() {
    local daemon_telemetry_pid="${1:-13319}"
    local daemon_telemetry_port="${2:-8080}"
    local daemon_telemetry_state="${3:-PAUSED(WEB)}"
    local daemon_telemetry_mode="${4:-termux}"
    local daemon_telemetry_scan="${5:-5s}"
    local daemon_telemetry_gps="${6:-30s}"
    local daemon_telemetry_rows="${7:-0}"
    local daemon_telemetry_fix="${8:---}"
    local network_telemetry_link="${9:-UP}"
    local network_telemetry_ip="${10:-10.183.119.245}"
    local network_telemetry_rssi="${11:--58dBm}"
    local network_telemetry_ssid="${12:-Lowes-Guest-WiFi}"

    clear_tui_console
    printf "%s\n" "$tui_divider_main_line"
    # Menu Header colored #DE2626 / RED
    printf " %b%-27s%b %27s\n" \
        "$tui_color_accent_red" "WI-FI + GPS DAEMON [104a]" "$tui_color_style_reset" \
        "~/.../wifi_allowlist.bejson"
    printf "%s\n" "$tui_divider_sub_line"

    # Strip 1: Daemon Telemetry (Labels colored #DE2626 / RED -> Values default)
    printf "%b %-6s %-5s %-12s %-7s %-5s %-5s %-5s %-3s%b\n" \
        "$tui_color_accent_red" \
        "PID" "PORT" "STATE" "MODE" "SCAN" "GPS" "ROWS" "FIX" \
        "$tui_color_style_reset"
    printf " %-6s %-5s %-12.12s %-7.7s %-5s %-5s %-5s %-3s\n" \
        "$daemon_telemetry_pid" "$daemon_telemetry_port" "$daemon_telemetry_state" \
        "$daemon_telemetry_mode" "$daemon_telemetry_scan" "$daemon_telemetry_gps" \
        "$daemon_telemetry_rows" "$daemon_telemetry_fix"
    printf "%s\n" "$tui_divider_sub_line"

    # Strip 2: Active Network Telemetry (Labels colored #DE2626 / RED -> Values default)
    printf "%b %-6s %-16s %-7s %-23s%b\n" \
        "$tui_color_accent_red" "LINK" "IP_ADDR" "RSSI" "SSID" "$tui_color_style_reset"
    printf " %-6s %-16.16s %-7s %-23.23s\n" \
        "$network_telemetry_link" "$network_telemetry_ip" "$network_telemetry_rssi" "$network_telemetry_ssid"
    printf "%s\n" "$tui_divider_sub_line"

    # Strip 3: Allowlist Records (Labels colored #DE2626 / RED -> Positional Values default)
    printf "%b %-3s %-4s %-5s %-9s %-18s %-11s%b\n" \
        "$tui_color_accent_red" "ID" "PRI" "AUTO" "SECURITY" "BSSID" "SSID" "$tui_color_style_reset"
    if [[ "$daemon_telemetry_rows" -eq 0 ]]; then
        printf " [0 rows - press [%b1%b] to scan & pick or [%b2%b] to add SSID]\n" \
            "$tui_color_accent_red" "$tui_color_style_reset" \
            "$tui_color_accent_red" "$tui_color_style_reset"
    fi

    printf "%s\n" "$tui_divider_main_line"
    # Strip 4: 3-Column Action Grid (Option numbers/keys colored #DE2626 / RED)
    render_bejson_tui_option_row "1" "Scan & Pick AP" "2" "Add Manual"   "3" "Delete Row"
    render_bejson_tui_option_row "4" "Connect Now"    "5" "Disconnect"   "6" "Priority Ord"
    render_bejson_tui_option_row "7" "Force GPS+Scan" "8" "Scan Timer"   "9" "GPS Interval"
    render_bejson_tui_option_row "T" "Auto-Connect"   "P" "PauseOnWeb"   "M" "Mode Cycle"
    render_bejson_tui_option_row "B" "Portal Probe"   "E" "Export 104a"  "Q" "Quit & Kill"
    printf "%s\n" "$tui_divider_main_line"
    printf "%bAction (5s refresh) >%b " "$tui_color_accent_red" "$tui_color_style_reset"
}
```

---

## 6. Domain Completeness Checklist for Daemon Menus

When designing or auditing an interactive daemon menu, verify that the hotkey grid covers these five operational failure modes:

1. **Zero-Typing Discovery (`[1]` / `[W] Scan & Pick AP`)**: Never make manual string typing (`[2]` / `[A]`) the primary workflow on mobile terminals when the daemon can scan and present indexed numbered options (`1..9` with numbers colored `#DE2626` / Red) to choose from.
2. **State Lock Override (`[4]` / `[C] Connect Now`, `[5]` / `[X] Disconnect`, `[7]` / `[F] Force GPS+Scan`)**: Paused or timer-blocked daemons must allow manual execution of core routines without requiring timer adjustments or global flag toggles first.
3. **Captive Portal Verification (`[B] Portal Probe`)**: In network automation, local IP assignment occurs behind unauthenticated portals. An explicit HTTP 204 probe prevents entering false connected states when WAN access is blocked.
4. **Deterministic Contention Resolution (`[6]` / `[R] Priority Order`)**: Multi-entry allowlists require priority ranks (`PRI`) and optional `BSSID` locks so the daemon picks the highest-value AP when multiple known networks are in range.
5. **Clean Process Lifecycle (`[Q] Quit & Kill`, `[E] Export 104a`)**: Expose the active `PID` and `PORT` in top telemetry, and guarantee quitting reaps child processes while cleanly flushing `.104a.bejson` state to disk.
