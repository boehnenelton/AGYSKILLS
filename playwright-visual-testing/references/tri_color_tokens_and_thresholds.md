# Tri-Color Tokens, Viewport Matrix & Perceptual Diffing Thresholds

Author Credit: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
Skill: `playwright-visual-testing` (Layer 5 UI & Visual Regression Gatekeeper)
RELATIONAL_ID: `102b6b50-0c49-413e-a8d8-fc1bcf7dd94d`

---

## 1. Policy §8.1 Tri-Color Tokens

Mandatory palette across web apps, UI components, HTML pages, and generated creative assets:

| Token Role | Hex Code | RGB Value | CSS Representation | Tolerated Variance |
|---|---|---|---|---|
| Background Primary | `#FFFFFF` | `rgb(255, 255, 255)` | `var(--color-bg, #FFFFFF)` | Euclidean RGB Distance $\le 12$ |
| Background Dark / Contrast | `#000000` | `rgb(0, 0, 0)` | `var(--color-contrast, #000000)` | Euclidean RGB Distance $\le 12$ |
| Text Primary | `#000000` | `rgb(0, 0, 0)` | `var(--color-text, #000000)` | Euclidean RGB Distance $\le 12$ |
| Text Inverted | `#FFFFFF` | `rgb(255, 255, 255)` | `var(--color-text-inv, #FFFFFF)` | Euclidean RGB Distance $\le 12$ |
| Active / Hover Accent | `#DE2626` | `rgb(222, 38, 38)` | `var(--color-accent, #DE2626)` | Euclidean RGB Distance $\le 18$ |

### Compliance Scoring Formula
$$\text{Compliance Ratio} = \frac{\sum \text{Pixels Matching Authoritative Tri-Color Tokens}}{\text{Total Sampled Pixels}} \times 100\%$$
- **PASS**: $\ge 90.0\%$ conforming pixels.
- **WARN**: $75.0\% - 89.9\%$ conforming pixels (permitted for photo assets or syntax highlighting).
- **FAIL**: $< 75.0\%$ conforming pixels (arbitrary color drift detected).

---

## 2. Standard Viewport Testing Matrix

| Device Profile | Width | Height | Device Pixel Ratio | Touch Enabled | Primary Target |
|---|---|---|---|---|---|
| **Mobile Portrait** | 360px | 640px | 2.0 | True | Android Phone / Hamburger Menu |
| **Tablet Portrait** | 768px | 1024px | 2.0 | True | iPad / Android Tablet View |
| **Desktop High-Res** | 1280px | 720px | 1.0 | False | Desktop 16:9 8-Lane Layout Canvas |

---

## 3. Perceptual Diffing Thresholds

- **Exact Match**: $0.0\%$ pixel difference.
- **Micro Shift Tolerance**: $\le 0.15\%$ (font rendering antialiasing or scrollbar artifacts).
- **Regression Flag Threshold**: $> 0.50\%$ pixel divergence triggers visual regression warning.
- **Breaking Layout Threshold**: $> 2.50\%$ pixel divergence triggers automated failure exit code.
