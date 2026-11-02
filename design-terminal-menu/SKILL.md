---
name: design-terminal-menu
description: >-
  Establish authoritative design principles, ergonomic standards, and interaction
  patterns for terminal user interface (TUI) menus and console daemons. Governs
  mandatory pre-render console clearing (\033[2J\033[H), the 57-column mobile viewport
  ceiling, Policy §8.1 #DE2626 Truecolor / ANSI Red accenting across headers, option
  labels (1, 2, 3, S, A, B), and alert strips, BEJSON positional key/value separation,
  and the Loaded Chamber stateful selection model. Houses two canonical showcase
  exemplars: the 57-column Tabular Telemetry Dashboard and the Stateful Selection
  Submenu Menu. Use when designing, auditing, or refactoring interactive terminal
  menus, daemon dashboards, or stateful selection flows. Do NOT use for headless
  CLI automation pipelines without visual menus (use design-terminal-cli), specific
  57-column BEJSON terminal menus (use bejson-tui-menu-builder), bare zero-filler
  template skeletons (use template-literal-skeleton), or browser HTML views (use behtml-104-builder).
---

# design-terminal-menu (Layer 4 Presentation & Design)

## Summary

`design-terminal-menu` establishes the canonical human-computer interaction principles, spatial mathematics, and behavioral mechanics for terminal user interface (TUI) menus. Part of the **Design Domain** (`design-*`), it is strictly decoupled from the **Template Domain** (`template-*`): design skills define the *governing laws, ergonomics, and preferred interaction paradigms*, whereas template skills stamp out bare mechanical skeletons.

`design-terminal-menu` eliminates visual entropy, broken column wrapping, and command history stacking across mobile portrait terminals (e.g. Android Termux) and desktop environments. It governs two showcase archetypes:
1. **Archetype 1: Tabular Telemetry Dashboard** (migrated and generalized from `bejson-tui-menu-builder`): High-density system/daemon monitoring, 57-column ceiling, static uppercase field headers rendered once in red, values aligned underneath in white, and decoupled 3-column action grids.
2. **Archetype 2: Stateful Selection & Submenu Menu**: The Loaded Chamber interaction model where application state is permanently displayed at the top (`[ Selected: <item> ]`), modes are clearly arranged (`- S) Select - A) Action - B) Back`), and an atomic drill-down submenu persistently locks user choices to disk.

---

## When to Use

- Designing or refactoring interactive terminal menus, CLI daemon dashboards, or console control interfaces.
- Enforcing mandatory console clearing (`\033[2J\033[H`) before every menu render so prior stdout never stacks into the active frame.
- Applying Policy §8.1 `#DE2626` / Red styling to menu headers, option labels (`1)`, `2)`, `3)`, `S)`, `A)`, `B)`, `[1]`, `[S]`), schema field labels, and status alerts (`[*] System operational. All metrics within tolerance`).
- Implementing the Loaded Chamber stateful selection pattern with persistent state headers and drill-down submenus.
- Eliminating line wrapping on mobile portrait screens by enforcing the 57-column viewport ceiling (or 30-46 columns for submenus).
- Decoupling static schema fields from dynamic positional values to eliminate repetitive inline key/value serialization.

## When NOT to Use

- Designing headless, scriptable command-line interfaces without interactive menus (use `design-terminal-cli`).
- Scaffolding bare zero-filler structural file templates without design preferences (use `template-literal-skeleton`).
- Rendering browser-based tabular HTML pages or web dashboards (use `behtml-104-builder`).
- Directly mutating or validating low-level `.104.bejson` data stores on disk (use `bejson-104-core`).

---

## 1. The Seven Absolute Laws of Terminal Menu Design

Every terminal menu MUST adhere to seven core design laws documented in [`references/terminal_menu_design_spec.md`](./references/terminal_menu_design_spec.md):

1. **Mandatory Pre-Render Console Clear**: Always emit `\033[2J\033[H` (or call `clear_screen()`) immediately before rendering any frame. Terminals must never stack frames or allow previous output to scroll into the dashboard.
2. **57-Column Mobile Viewport Ceiling**: Primary dashboards must fit within 57 columns (`70 - 13` safety margin); selection submenus clamp between 30 and 46 columns.
3. **Policy §8.1 `#DE2626` / Red Tri-Color Accenting & Feedback Rules**:
   - Headers: Top titles and banners (`STATEFUL MENU EXAMPLE`, `TELEMETRY DASHBOARD [104a]`).
   - Option Labels: Selector keys and parentheses (`1)`, `2)`, `3)`, `S)`, `A)`, `B)`, `[1]`, `[M]`, `[Q]`).
   - Field Header Strips: Uppercase table columns (`PID`, `PORT`, `STATE`, `MODE`).
   - Prompts: Input brackets and cues (`[ Choose an option: ]`, `Action >`).
   - Values & Descriptions: Clean neutral white (`\033[1;37m` or default text).
   - **Dynamic Feedback Messages (Input & Action Responses)**:
     - **Positive Feedback**: Bold White, ALL CAPS with `[✓]` (e.g. `[✓] PERSISTENTLY SELECTED 'EXECUTIVE FADE'`).
     - **Bad Feedback (Non-option characters / errors)**: Bold Red, lowercase with `[X]` (e.g. `[X] unknown command: 'z'. enter s, a, 1, 2, or 3.`).
     - **Neutral Feedback**: Normal standard rules with `[*]` (e.g. `[*] Info: Active Item='Executive Fade'`).
4. **Positional Telemetry Separation**: Header fields rendered once ($O(K)$ overhead); data rows aligned positionally underneath ($O(1)$ overhead). Never repeat `Key: Value |` inline.
5. **Decoupled State & Global Navigation Invariants (Loaded Chamber)**: Display active target at top; enforce global fast-jump hotkeys (`S` for Select, `A` for Action, `B` for Back, `X` for Exit on Main Menu) from any view or submenu depth.
6. **Zero-Drift `printf` Formatting**: Inject ANSI color escapes only in format string literals, never in padded text arguments.
7. **Clean Exit Traps**: Restore cursor visibility (`\033[?25h`) and echo via signal handlers (`atexit` / `trap`).

---

## 2. Showcase Archetype 1: Tabular Telemetry Dashboard

Designed for continuous monitoring, daemons, and system telemetry:

```text
=========================================================
 TELEMETRY DASHBOARD [104a]     ~/.../data_partition.bejson
---------------------------------------------------------
 PID    PORT  STATE      MODE    SCAN  GPS   ROWS  FIX
 13319  8080  ONLINE     termux  5s    30s   12    FIX
---------------------------------------------------------
 LINK   IP_ADDR          RSSI    SSID                   
 UP     10.183.119.245   -58dBm  Core-Mesh-Network      
---------------------------------------------------------
 [*] System operational. All metrics within tolerance  
=========================================================
 [1] Scan & Pick AP  [2] Add Manual     [3] Delete Row   
 [4] Connect Now     [5] Disconnect     [6] Priority Ord 
 [7] Force Probe     [8] Scan Interval  [9] Export 104a  
 [M] Mode Switch     [R] Refresh Now    [Q] Quit & Exit  
=========================================================
Action (Enter choice) > 
```

- **Runnable Implementation**: [`scripts/render_tabular_menu.py`](./scripts/render_tabular_menu.py)
- **Key Features**: High-density 57-column telemetry strips, `#DE2626` uppercase headers, red bracketed action options, single-line alert banner, non-scrolling clean updates.

---

## 3. Showcase Archetype 2: Stateful Selection & Submenu Menu

Designed for interactive workflows where users pick a target once and fire multiple actions against it:

```text
================= STATEFUL MENU EXAMPLE =================

   [   Selected:     Executive Fade    ]   

-   S) Select   -    A) Action   -   X) Exit
---------------------------------------------------------
  1) Info
  2) Configure
  3) Exit
-
-
 [   Choose an option: ]
```

- **Runnable Implementation**: [`scripts/render_stateful_menu.py`](./scripts/render_stateful_menu.py)
- **State Persistence**: Target stored atomically in `data/persistent_selection.json`.
- **Global Navigation Invariants**:
  - `S`: Global jump straight to Selection Submenu from anywhere, at any depth.
  - `A`: Global jump straight to Action Menu from anywhere, at any depth.
  - `B`: Global Back from any submenu straight to Main Menu.
  - `X`: Global Exit on Main Menu (where `B` is replaced by `X`).

---

## 4. Verification & Testing

To preview and verify both showcase archetypes:

```bash
# Preview Archetype 1: Tabular Telemetry Dashboard
python3 ~/.gemini/config/skills/design-terminal-menu/scripts/render_tabular_menu.py --preview

# Preview Archetype 2: Stateful Selection & Submenu Menu
python3 ~/.gemini/config/skills/design-terminal-menu/scripts/render_stateful_menu.py --preview

# Run interactive stateful menu loop
python3 ~/.gemini/config/skills/design-terminal-menu/scripts/render_stateful_menu.py
```
