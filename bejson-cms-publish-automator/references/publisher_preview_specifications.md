# BEJSON CMS Publisher, Preview Server & Screenshot Specifications

## 1. Unified Publishing & Preview Lifecycle

The `bejson-cms-publish-automator` automates the 4-stage deployment pipeline for BEJSON CMS:

```
[1. Static Build]     --> Executes BEJSON_CMS_Publisher._execute()
          |               Reads MFDB site master & compiles storage/builds/
          v
[2. Preview Server]   --> Starts socketserver/http.server on port 8000
          |               Binds with SO_REUSEADDR and isolates build directory
          v
[3. Browser Dispatch] --> Dispatches termux-open to launch Android system browser
          |               Points directly to http://localhost:8000/index.html
          v
[4. Visual Capture]   --> (Optional) Headless Playwright captures 6 surfaces
                          Saves 1280x720 and 375x812 PNG captures to images/
```

## 2. The 6 Canonical Capture Surfaces

When `--screenshots` is enabled, the pipeline captures 6 distinct viewports and routes:

| Index | Filename | Target Route | Viewport (W x H) | Content Inspected |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `01_published_home_desktop.png` | `/index.html` | 1280 x 720 px | Home feed, header navigation, hero banner |
| **02** | `02_published_home_mobile.png` | `/index.html` | 375 x 812 px | Mobile responsive drawer, card stacking |
| **03** | `03_published_article_newagent.png` | `/blog/.../newagent/` | 1280 x 720 px | Article body, featured image, related posts |
| **04** | `04_published_article_telemetry.png` | `/blog/.../telemetry/` | 1280 x 720 px | Code syntax blocks, monospace formatting |
| **05** | `05_published_apps_feed.png` | `/apps/index.html` | 1280 x 720 px | Standalone apps grid, launch cards |
| **06** | `06_published_category_bejson.png` | `/category/bejson/` | 1280 x 720 px | Filtered taxonomy archive feed |

## 3. Playwright Headless Automation

Under Android Termux:
- Uses `termux_playwright.async_playwright_termux` with fallback to `playwright.async_api`.
- Launches Chromium in headless mode.
- Waits for `domcontentloaded` and a 300ms settling pause before capturing.
