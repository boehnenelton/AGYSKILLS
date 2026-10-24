---
name: playwright-visual-testing
description: >-
  Execute automated multi-viewport screenshot captures, perceptual pixel diffing,
  horizontal layout overflow detection, and Policy §8.1 Tri-Color token compliance
  audits (#FFFFFF, #000000, #DE2626) on web applications, SPAs, and UI components
  using headless Chromium in Android Termux. Use when validating visual regressions,
  inspecting mobile/tablet/desktop responsive layouts (360px, 768px, 1280px),
  verifying color token adherence, or generating baseline visual regression reports.
  Do NOT use for low-level DOM error diagnostics and game engine load debugging
  (use playwright-debugger-auditor), anti-bot evasion and mouse physics (use
  playwright-stealth-agent), raw Chromium process lifecycle management (use
  playwright-termux-automation), or full end-to-end user scenario testing (use playwright-debugger-auditor).
---

# `playwright-visual-testing` (Layer 5 Visual Regression & Tri-Color Auditor)

- **Target Architecture**: Android Termux (aarch64 / ARM 64-bit, Android Bionic libc)
- **Architectural Tier**: Layer 5 (L5) UI & Visual Interface Testing Gatekeeper
- **Author Credit**: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
- **RELATIONAL_ID**: `102b6b50-0c49-413e-a8d8-fc1bcf7dd94d`
- **Version**: `1.0.0`

---

## Summary

`playwright-visual-testing` is the canonical Layer 5 visual regression and design system compliance auditor. It captures responsive multi-viewport screenshot matrices (Mobile Portrait 360x640, Tablet Portrait 768x1024, Desktop 1280x720), audits computed styles against Policy §8.1 Tri-Color tokens (`#FFFFFF`, `#000000`, `#DE2626`), flags horizontal layout overflows, and records visual evidence across UI builds.

---

## When to Use

- Capturing multi-viewport screenshot matrices for web applications, dashboards, or games.
- Auditing user interfaces for strict adherence to Policy §8.1 Tri-Color palette tokens.
- Detecting unintended horizontal page overflow (`scrollWidth > innerWidth`) on mobile screens.
- Performing visual regression tests comparing current UI states against baselines.
- Generating visual proof artifacts prior to packaging and release delivery.

---

## When NOT to Use

- Debugging why an app or game fails to load, canvas context errors, or 404 assets (use `playwright-debugger-auditor`).
- Injecting humanized Bézier mouse movements or evading anti-bot WAFs (use `playwright-stealth-agent`).
- Managing Termux Chromium process reaping and low-memory limits (use `playwright-termux-automation`).
- Running multi-step autonomous user login and transaction journeys (use `playwright-debugger-auditor`).

---

## 1. Visual Testing Matrix & Policy 8.1 Verification

### Multi-Viewport Execution Roster
1. **Mobile Portrait**: `360 x 640` (DPR: 2.0, touch-enabled) — verifies hamburger menus, drawer sidebars, and portrait quantization.
2. **Tablet Portrait**: `768 x 1024` (DPR: 2.0, touch-enabled) — verifies intermediate responsive reflow.
3. **Desktop Canvas**: `1280 x 720` (DPR: 1.0) — verifies 8-lane 16:9 full-canvas layouts.

### Policy §8.1 Tri-Color Tokens
- **Background**: `#FFFFFF` (White) or `#000000` (Black)
- **Text**: `#000000` (Black) or `#FFFFFF` (White)
- **Active / Hover Accent**: `#DE2626` (Red)

Compliance is calculated across computed CSS color declarations:
$$\text{Compliance} \ge 90.0\% \implies \text{PASS}$$

---

## 2. CLI Execution Reference

The skill includes an executable CLI at `scripts/visual_diff_auditor.py`:

```bash
# Execute visual testing on an HTML file or target directory
python3 ~/.gemini/config/skills/playwright-visual-testing/scripts/visual_diff_auditor.py /path/to/target_directory

# Override screenshot output directory
python3 ~/.gemini/config/skills/playwright-visual-testing/scripts/visual_diff_auditor.py \
  /path/to/target_directory \
  --output /custom/export/directory
```

---

## 3. Deterministic Exit Codes

- **`0`**: Clean visual pass; all viewports conform to Policy §8.1 Tri-Color tokens ($\ge 90\%$) with zero layout overflows.
- **`10`**: Minor warning (e.g., $75\% - 89\%$ color compliance due to photo assets).
- **`20`**: Critical visual failure (arbitrary foreign color palette drift $< 75\%$ or horizontal overflow).
- **`30`**: Target path or server launch failure.
