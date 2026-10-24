# Diagnostic Codes & Remediation Ledger

Author Credit: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Skill: `playwright-debugger-auditor` (Layer 2 Diagnostic Gatekeeper)

---

## 1. Code Ledger Table

| Verdict Code | Severity | Root Cause Trigger | Primary Remediation |
|---|---|---|---|
| `LOAD_ISSUE_MISSING_FIXTURE_PAYLOAD` | CRITICAL | Engine global present (`SwordSlasher`, `VanillaGame`, etc.), but `<canvas>` not mounted; awaiting fixture or database. | Pass fixture query string (e.g. `?mfdb=/path/to/fixture.json`), set `window.MFDB_DATA`, or send `sword:load` postMessage. |
| `LOAD_ISSUE_FILE_PROTOCOL_RESTRICTION` | CRITICAL | Loaded via `file://` scheme; browser blocks ES6 modules (`import/export`) or `fetch()` due to origin restrictions. | Serve target over local HTTP server daemon (`http://127.0.0.1:8089/`). Never use direct `file://` for module-based apps. |
| `LOAD_ISSUE_MISSING_ASSET_404` | CRITICAL | HTTP 404 response intercepted on critical dependency (`.js`, `.json`, `.wasm`, `.png`). | Correct relative path references or adjust server serving root so sibling/parent asset folders are reachable. |
| `LOAD_ISSUE_UNCAUGHT_JS_EXCEPTION` | CRITICAL | Unhandled runtime exception thrown on main JavaScript thread (`pageerror`). | Inspect call stack in debug report; add null checks or verify DOM elements exist before element access. |
| `LOAD_ISSUE_BLANK_CANVAS` | WARNING | `<canvas>` exists and has non-zero dimensions, but all sampled pixels are blank (`rgba(0,0,0,0)`) or black. | Verify that render loop (`requestAnimationFrame`) started and that 2D/WebGL context acquired without shader compilation errors. |
| `LOAD_ISSUE_AUDIO_AUTOPLAY_SUSPENDED` | WARNING | `AudioContext.state === 'suspended'` due to browser autoplay policy. | Bind audio initialization to a user gesture (pointerdown/click or keypress). |
| `STATUS_HEALTHY_EXECUTION` | INFO | Zero unhandled exceptions, zero 404s, populated canvas buffers, active interaction state. | No remediation required; application loaded cleanly. |

---

## 2. Component Inspection Protocol

1. **Protocol Check**: Ensure HTTP transport. Fail immediately if `file://` triggers module/CORS errors.
2. **Network Audit**: Intercept all outgoing asset requests. Flag any non-200 responses (excluding `/favicon.ico`).
3. **Console & Error Sniffing**: Categorize console stream into `log`, `warning`, and `error`. Intercept unhandled promise rejections.
4. **Canvas State Sampling**:
   - Query all `<canvas>` nodes in the DOM.
   - Verify buffer width/height ($W > 0, H > 0$).
   - Sample center and corner pixels using `getImageData`.
   - Test 2D and WebGL context availability.
5. **Interactive Stimulation**:
   - Dispatch click event to canvas center.
   - Dispatch standard game keys (`Space`, `Enter`, `ArrowRight`, `ArrowDown`, `KeyW`, `KeyA`, `KeyS`, `KeyD`).
   - Re-evaluate DOM and pixel buffer after interaction to capture state progression.
