# Terminal Menu Design Specification & Interaction Principles

- **Domain**: Design (`design-*`)
- **Author**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **Status**: Authoritative Canonical Specification
- **Version**: 1.0.0

---

## 1. Executive Summary & Design Domain Philosophy

The **Design Domain** (`design-*`) is strictly separated from the **Template Domain** (`template-*`). While template skills govern mechanical skeleton scaffolding, slot injection (`{{VAR}}`), and file stamping, design skills establish **ideal design principles, human-computer interaction laws, ergonomic standards, spatial layout mathematics, and behavioral mechanics**.

`design-terminal-menu` codifies the gold-standard design principles for terminal user interface (TUI) menus and interactive console daemons operating across mobile portrait screens (e.g. Android Termux) and desktop terminal emulators.

---

## 2. The Seven Absolute Laws of Terminal Menu Design

### Law 1: Mandatory Pre-Render Console Clear
A terminal menu MUST execute a console clear and cursor homing sequence (`\033[2J\033[H`) immediately before rendering every frame or view:
- Prevents stale terminal history, prior command stdout, and stacked frame artifacts from scrolling into the active dashboard.
- Guarantees the menu begins consistently at line 1, column 1.
- Honor `TUI_NO_CLEAR=1` solely when running in non-interactive batch test pipelines or headless CI pipes.

### Law 2: 57-Column Mobile Viewport Ceiling
All primary menu banners, dividers, and telemetry tables MUST be clamped strictly to $\le 57$ columns (`70 - 13` column safety margin):
- Prevents horizontal line wrapping on mobile portrait Termux screens.
- Compact drill-down selection submenus are clamped between 30 and 46 columns for focused visual hierarchy.
- Dividers use standard single-byte ASCII (`=` or `-`), never multi-byte unicode glyphs that drift column width calculations.

### Law 3: Policy §8.1 `#DE2626` / Red Tri-Color Accenting
To enforce clear visual hierarchy and brand identity without monotone walls of white or distracting rainbow colors, the terminal uses Policy §8.1 Tri-Color tokens:
- **Red Accents (`\033[38;2;222;38;38m` Truecolor or `\033[1;31m` ANSI Red fallback)**:
  1. **Menu Headers**: Top screen banners, titles, and section dividers.
  2. **Option Labels & Hotkeys**: Numbered or lettered selector keys (`1)`, `2)`, `3)`, `S)`, `A)`, `B)`, `[1]`, `[S]`).
  3. **Field Header Strips**: Uppercase schema labels (`PID`, `PORT`, `STATE`, `MODE`).
  4. **Status & Alert Banners**: Full alert notifications (`[*] System operational. All metrics within tolerance`, `[✓]`, `[!]`, `[✗]`).
  5. **Input Prompts**: Action prompts (`[ Choose an option: ]`, `Action (Enter choice) >`).
- **Neutral White / Default (`\033[1;37m` or `\033[0m`)**:
  - Dynamic runtime values, status attributes, and option descriptions.
  - Ensures high legibility and prevents black-on-red eye strain.

### 2.1 Dynamic Status Feedback Discipline (User Feedback Rules)
This discipline applies strictly to **dynamic feedback and alert messages** (e.g., responses to user input such as entering non-option characters, execution outcomes, or operational status updates), while the static structural UI elements (headers, options, field labels) adhere to their standard layout rules:

1. **Positive Status Feedback**:
   - **Color**: Bold White (`\033[1;37m`).
   - **Casing**: **ALL CAPS**.
   - **Tag**: `[✓]`.
   - **Example**: `[✓] PERSISTENTLY SELECTED 'EXECUTIVE FADE'`, `[✓] ACTION EXECUTED SUCCESSFULLY`.
2. **Bad / Error Feedback** (e.g. entering a non-option character, missing selection, failure):
   - **Color**: Bold Red (`\033[1;38;2;222;38;38m` or ANSI Red).
   - **Casing**: **lowercase**.
   - **Tag**: `[X]`.
   - **Example**: `[X] unknown command: 'z'. enter s, a, 1, 2, or 3.`, `[X] action failed: no item currently selected. press 's' first.`
3. **Neutral Status Feedback**:
   - **Color / Casing**: **Normal standard rules** (standard sentence case, red accent tag with standard text).
   - **Tag**: `[*]`.
   - **Example**: `[*] Info: Active Item='Executive Fade', Path='...'`.

### Law 4: Positional Telemetry Separation (BEJSON Text Discipline)
Repeating inline `Key: Value |` labels on every line creates $O(N \times K)$ visual clutter and wastes precious horizontal terminal space:
- **Rule**: Declare the uppercase **Field Header Strip** once in `#DE2626` / Red ($O(K)$ overhead).
- Align positional **Value Rows** directly underneath in default white ($O(1)$ overhead).
- Enables 8 daemon metrics and 4 network attributes to fit cleanly within 56 columns with zero line wraps.

### Law 5: Decoupled State & Global Navigation Invariants (Loaded Chamber Selection Model)
Menus dedicate their top screen real estate to active state and enforce global fast-jump hotkeys:
- **Persistent State Display**: The top rows permanently display active application state (`[ Selected: <item> ]`).
- **Global Navigation Strip**:
  - **Main Menu**: `- S) Select - A) Action - X) Exit` (B is replaced by X to exit at the root).
  - **Submenus**:  `- S) Select - A) Action - B) Back` (B jumps back to Main Menu).
- **Global Fast-Jump Invariants (`S`, `A`, `B`, `X`)**:
  - **`S` (Select)**: Global invariant. Jumping straight to the Selection Submenu from anywhere, at any depth.
  - **`A` (Action)**: Global invariant. Jumping straight to the Action Menu from anywhere, at any depth.
  - **`B` (Back)**: Global invariant in all submenus jumping back to the Main Menu.
  - **`X` (Exit)**: Bound to the Main Menu navigation strip to exit cleanly with terminal cursor and echo restored.
- **Atomic State Persistence**: Selecting a new target from the selection catalog persistently locks it to disk (`data/persistent_selection.json`) using atomic temporary file replacement (`.tmp` -> rename).
- **Decoupled Verbs**: Actions in the Action Menu execute against the currently locked target without asking the user to re-select it.

### Law 6: Zero-Drift `printf` Padding
Never concatenate ANSI escape codes into variable arguments before passing them into padded format specifiers (`%-18s`). Standard `printf` counts unprintable escape bytes toward column width, causing subsequent columns to drift out of alignment:
- Inject ANSI color codes directly into the format string literal.
- Pad only uncolored, raw text strings.

### Law 7: Clean Exit Traps & Cursor Lifecycle
Interactive menus must never leave the terminal in a broken state:
- Bind signal traps (`trap cleanup EXIT INT TERM` in Bash, `atexit.register` in Python).
- Guarantee cursor restoration (`\033[?25h`) and terminal echo restoration (`stty echo`).

---

## 3. Two Canonical Menu Archetypes

### Archetype 1: Tabular Telemetry Dashboard
Designed for live process daemons, background monitors, network scanners, and system inspectors:
- **Geometry**: 57-column fixed width.
- **Top Header**: Screen title in `#DE2626` / Red left-aligned, file path or timestamp right-aligned.
- **Telemetry Strips**: Field names rendered once in `#DE2626`; values rendered underneath in white.
- **Alert Strip**: Single-line status banner in `#DE2626`: `[*] System operational. All metrics within tolerance`.
- **Action Grid**: 3-column action matrix with red bracketed keys: `[1]`, `[2]`, `[3]`, ..., `[Q]`.

### Archetype 2: Stateful Selection & Submenu Menu
Designed for multi-step tools, management consoles, and target-based workflows:
- **Geometry**: 30 to 46 columns clamped.
- **Header**: Centered title banner in `#DE2626`.
- **State Box**: Top-level dedicated row: `[   Selected:     <item>    ]`.
- **Mode Strip**: Inline navigation: `-   S) Select   -    A) Action   -   B) Back`.
- **Main Actions**: Numbered action list with red option labels: `1) Info`, `2) Configure`, `3) Exit`.
- **Submenu Mechanics**: Pressing `S` opens a clean-screen list of options; choosing an option atomically writes to persistent storage and re-renders the main frame with the new item locked in.
- **Prompt**: Centered prompt box: `[   Choose an option: ]`.
