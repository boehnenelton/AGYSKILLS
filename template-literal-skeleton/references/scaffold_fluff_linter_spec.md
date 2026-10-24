# Scaffold Fluff Linter Specification: Zero Filler & Invisible Architecture

**Status**: Canonical Standard Reference  
**Release Version**: 300  
**Format Creator**: Elton Boehnen  
**Location**: Roseburg, Oregon, United States  
**Policy Binding**: Global Policy §7.3 & §12.4  

---

## 1. Overview & Objective

The `scaffold_fluff_linter` enforces Elton Boehnen's **Zero-Filler Skeleton Law** (Policy §7.3 Negative Constraints). When generating templates, wireframes, scaffolds, or starter files across any language or markup (HTML, BEHTML, CSS, JSON, Python, Bash), output must consist strictly of functional, bare-bones structural scaffolding. Fabricated prose, Latin dummy copy, framework runtime telemetry, and external placeholder images are strictly prohibited.

---

## 2. Prohibited Content Categories

### 2.1 Banned Copy Filler Patterns
Templates must never contain Latin copy, marketing fluff, or generic mock text:
- `\blorem\b` / `\bipsum\b` / `\bdolor\s+sit\b` / `\bconsectetur\b`
- `\bsample\s+text\b` / `\bdummy\s+text\b` / `\bplaceholder\s+text\b`
- `\bwelcome\s+to\b` / `\bour\s+services\b` / `\btestimonials?\b`

### 2.2 Banned Framework & Telemetry Leaks
Templates must never render internal architectural debug markers or grid telemetry into user-facing markup:
- `grid space activated`
- `framework loaded`
- `lane \d+ to \d+ active`
- `container wrapper rendered`
- `breakpoint triggered`

### 2.3 Banned External Mock Image Hosts
Mock image services that introduce network dependencies, track user requests, or break in offline/local environments are forbidden:
- `via.placeholder.com`
- `placeholder.com`
- `picsum.photos`
- `unsplash.com`

---

## 3. Approved Zero-Filler Skeleton Tokens

When scaffolding structural containers, use strictly literal, semantic labels:

| Interface Element | Approved Literal Label | Prohibited Mock Example |
| :--- | :--- | :--- |
| **Headline / Title** | `'Title'` or `'Page Title'` | `'Welcome to Our Amazing Blog'` |
| **Body Content** | `'Content Body'` or `{{page_body_html}}` | `'Lorem ipsum dolor sit amet...'` |
| **Navigation Headers** | `'Menu Header'` or `'Navigation'` | `'Explore Our World'` |
| **Menu Items** | `'Menu Item 1'`, `'Menu Item 2'` | `'Services'`, `'Pricing'`, `'Contact Us'` |
| **Author Bylines** | `'Author Name'` | `'John Doe, Tech Enthusiast'` |
| **Category Badges**| `'Category Name'` | `'Gadgets & Gizmos'` |
| **Timestamps** | `'2026-01-01T00:00:00Z'` | `'Yesterday'`, `'5 minutes ago'` |
| **Metric Readouts** | `'0'` or `'Count'` | `'10,000+ Happy Users'` |
| **Media Placeholders**| Inlined transparent SVG or local file path | `https://picsum.photos/800/600` |

---

## 4. Black-Box Linter Interface

The companion audit script [`scaffold_fluff_linter.py`](file:///data/data/com.termux/files/home/.gemini/config/skills/template-literal-skeleton/scripts/scaffold_fluff_linter.py) provides automated stage-gate verification:

```bash
# Audit a single file
python3 scripts/scaffold_fluff_linter.py path/to/template.html

# Audit an entire template directory
python3 scripts/scaffold_fluff_linter.py resources/templates/
```

Exit Codes:
- `0`: Clean pass — template contains zero filler or telemetry leaks.
- `1`: Violation detected — one or more banned patterns were encountered.
