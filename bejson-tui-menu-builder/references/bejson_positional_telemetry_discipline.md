# The BEJSON Positional Telemetry Discipline: Principles & Theory of High-Density Terminal Interfaces

Terminal User Interfaces (TUIs) and interactive CLI daemon menus frequently suffer from severe visual entropy. When built ad-hoc with inline `echo` statements, they repeat static labels on every line, narrate system states in multi-line prose, embed live state values inside action button labels, and overflow mobile viewports such as Termux in portrait mode.

The **BEJSON Positional Telemetry Discipline** applies the core data-engineering insight of **BEJSON (104 / 104a)** - the strict separation of schema `Fields` from positional `Values` - directly to human-readable terminal interfaces.

## 1. Case Study: Bad Menu Design vs. Good Menu Design

### Bad Menu Design Example (Legacy Inline Anti-Pattern)

```text
======================================================================
 WI-FI + GPS DAEMON | PID: 13319 | Scan: 5s | GPS: 30s | Mode: termux
 STATUS: PAUSED (WEB CONNECTED: Lowes-Guest-WiFi @ 10.183.119.245) | Last GPS: Never | Rows: 0
======================================================================
[PAUSED] Connected to web via SSID: Lowes-Guest-WiFi (10.183.119.245)
Background Wi-Fi scanning, auto-connect, and 30s GPS logging are paused.
Scanner will automatically resume if internet connection drops.
----------------------------------------------------------------------
 BEJSON 104a ALLOWLIST (/storage/emulated/0/Admin/Dev/Bash/Development/Wifi_Daemon/wifi_allowlist.104a.bejson)
----------------------------------------------------------------------
  [Allowlist is empty. Press A to add an acceptable Wi-Fi network]
======================================================================
 [A] Add Wi-Fi to Allowlist         [T] Toggle Auto-Connect Flag
 [D] Delete Entry from Allowlist    [S] Set Scan Delay Timer (5s)
 [G] Set GPS Log Interval (30s)     [P] Toggle Pause-On-Web (true)
 [E] Export Clean 104a Schemas      [M] Cycle Connect Mode (termux)
 [Q] Quit & Stop Background PID
======================================================================
Select action (refreshes in 5s):
```

#### Diagnostic Breakdown of the Bad Design:
- **Severe Viewport Overflow (70 to 110 Columns)**: While the `===` dividers are 70 characters wide, the `STATUS:` line reaches **95 characters** and the allowlist file path banner reaches **110 characters**, causing jagged double-wrapping on mobile Termux screens.
- **JSON-Style Key Repetition**: Inline `PID: 13319 | Scan: 5s | GPS: 30s | Mode: termux` wastes **68 characters** across the top two lines repeating static field names and pipe delimiters.
- **Four Lines of Redundant Status Prose**: Lines 3, 5, 6, and 7 state the exact same condition (`PAUSED` because `Lowes-Guest-WiFi` is connected at `10.183.119.245`) twice in full sentences and spend two additional lines explaining how pause-on-web works.
- **Inline State Pollution in Hotkeys**: Re-printing `(5s)`, `(30s)`, `(true)`, and `(termux)` inside the bottom hotkey labels bloats button widths to 35+ characters, limiting the menu to 2 wide columns.
- **Missing Operational Controls**: Lacks live AP discovery/selection, manual connect/disconnect overrides, captive portal WAN verification, immediate GPS+Wi-Fi sample capture, and allowlist priority ordering.

### Good Menu Design Example (57-Column BEJSON Positional Standard)

#### Empty State (All Lines Strictly <= 57 Characters):

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
 [0 rows - press [W] to scan & pick or [A] to add SSID]
=========================================================
 [W] Scan & Pick AP   [A] Add Manual   [D] Delete Row
 [C] Connect Now      [X] Disconnect   [R] Priority Ord
 [F] Force GPS+Scan   [S] Scan Timer   [G] GPS Interval
 [T] Auto-Connect     [P] PauseOnWeb   [M] Mode Cycle
 [B] Portal Probe     [E] Export 104a  [Q] Quit & Kill
=========================================================
Action (5s refresh) >
```

#### Populated Allowlist State (Positional `Values` Under One `Fields` Header):

```text
---------------------------------------------------------
 ID  PRI  AUTO  SECURITY  BSSID              SSID
 01  1    Y     WPA2      a4:2b:8c:11:09:f0  Home-5G
 02  2    Y     OPEN      *                  Lowes-Guest
 03  3    N     WPA3      7c:10:c9:44:22:10  Phone-Hotsp
---------------------------------------------------------
```

## 2. Core Theoretical Foundation: JSON Entropy vs. BEJSON Density in Text

In data serialization, standard JSON repeats every key name inside every object record, whereas BEJSON declares the `Fields` array once in the header and stores records as compact positional `Values` arrays.

When an allowlist or process table prints `SSID: Home | Auto: true | Mode: WPA2` on each row, key repetition scales linearly with row count $O(N \times K)$, where $N$ is the number of rows and $K$ is the number of fields. By transposing the **BEJSON Separation Law** to the terminal screen, we decouple the **Field Header Strip** ($O(K)$ once) from the **Positional Value Rows** ($O(1)$ label overhead per row). Eight distinct daemon metrics - including `PID` and `PORT` - fit inside **56 columns** with zero wrapping and instant vertical scanability.

## 3. The Five Pillars of the Discipline

| Pillar | Problem Eliminated | Architectural Rule |
| :--- | :--- | :--- |
| **1. BEJSON Key/Value Separation** | Repeating `Key: Value \|` labels on every status bar and table row | Declare uppercase `Fields` once per strip; align `Values` positionally underneath via deterministic `printf` widths. |
| **2. The 57-Column Viewport Ceiling** | 70-110 char lines wrapping unpredictably on Termux mobile portrait screens | Cap all dividers (`===` / `---`), headers, and data rows at <= 57 columns (`70 - 13` char reduction). |
| **3. Single-Source Telemetry** | Repeating connection state in the header, status banner, prose paragraphs, and menu buttons | Display every metric and state token exactly once in the top telemetry strips; eliminate explanatory prose sentences. |
| **4. Hotkey Label Decoupling** | Stuffing `(5s)`, `(30s)`, `(true)`, `(termux)` inside menu action labels | Keep hotkey labels strictly to concise `[K] Verb Noun` actions (`18 chars` max per column) to unlock a 3-column grid. |
| **5. Operational Control Parity** | Forcing the user to type SSIDs by hand or drop to a shell to force-connect, probe, or reorder | Ensure every daemon TUI covers Discovery (`[W]`), Override (`[C]`/`[X]`/`[F]`), Ordering (`[R]`), Probe (`[B]`), and Lifecycle (`[E]`/`[Q]`). |

## 4. Quantitative Before-and-After Comparison

| Metric | Bad Design (Legacy Inline) | Good Design (BEJSON Positional) | Delta / Improvement |
| :--- | :--- | :--- | :--- |
| **Divider Width** | 70 chars | 57 chars | **-13 chars** (zero wrap on mobile) |
| **Max Line Width** | 110 chars (wraps 2x) | 57 chars (hard ceiling) | **-53 chars** (eliminates all wrapping) |
| **Redundant Prose Lines** | 4 lines | 0 lines | **-4 vertical lines** |
| **Telemetry Metrics Shown** | 7 metrics | 12 metrics (adds `PORT`, `LINK`, `RSSI`, `PRI`, `BSSID`) | **+71% information density** |
| **Interactive Commands** | 9 commands (2 cols) | 15 commands (3 cols) | **+6 critical operational actions** |

## 5. Domain Completeness Checklist for Daemon Menus

Whenever designing or auditing an interactive daemon menu, verify that the hotkey grid addresses these five operational failure modes:

1. **Zero-Typing Discovery (`[W] Scan & Pick AP`)**: Never make manual string typing (`[A]`) the primary workflow on a mobile terminal when the hardware can scan and present an indexed list (`1..9`) to select from.
2. **State Lock Override (`[C] Connect Now`, `[X] Disconnect`, `[F] Force GPS+Scan`)**: A paused or timer-driven daemon must always allow immediate manual execution of its core loop without requiring the user to reconfigure timers or toggle global flags first.
3. **Captive Portal / Reachability Verification (`[B] Portal Probe`)**: In network automation, local IP assignment (`10.x.x.x` or `192.168.x.x`) frequently occurs behind unauthenticated captive portals. A dedicated HTTP `204` probe prevents the daemon from falsely entering `PAUSED(WEB)` when WAN traffic is blocked.
4. **Deterministic Contention Resolution (`[R] Priority Order`)**: Any allowlist with more than one entry requires a priority rank (`PRI`) and optional `BSSID` lock so the daemon deterministically selects the highest-value connection when multiple known networks are in range.
5. **Clean Process Lifecycle (`[Q] Quit & Kill`, `[E] Export 104a`)**: Always expose the active `PID` and `PORT` in the top telemetry strip and ensure quitting cleanly reaps background child processes while preserving valid `.104a.bejson` state on disk.
